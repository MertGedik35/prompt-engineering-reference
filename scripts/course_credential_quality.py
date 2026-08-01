from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    from .check_freshness import utc_today
except ImportError:  # pragma: no cover
    from check_freshness import utc_today  # type: ignore[import-not-found,no-redef]

ROOT = Path(__file__).resolve().parents[1]
COURSE_PATH = "catalog/courses.json"
CREDENTIAL_PATH = "catalog/credentials.json"
RELATIONSHIP_VALUES = {
    "produces",
    "official_preparation",
    "recommended_learning",
    "part_of",
    "overview_of",
}
PRODUCES_COMPATIBLE_OUTCOMES = {
    "completion_record",
    "completion_certificate",
    "digital_badge",
    "skill_badge",
    "assessed_skill_credential",
    "applied_skill_credential",
    "professional_certificate_program",
}
BANNED_MARKETING = (
    "best course",
    "guaranteed job",
    "guaranteed certification",
    "world-class",
    "number one",
    "#1",
)
TRACKING_QUERY_MARKERS = ("utm_", "ref=", "affiliate", "coupon", "referral")
INACTIVE_URL_MARKERS = (
    "showredirectnotfoundbanner",
    "searchtext=",
    "/search?",
)
KNOWN_INACTIVE_AWS_COURSE_FRAGMENTS = ("/course/17763/foundations-of-prompt-engineering",)
GENERIC_MICROSOFT_VERIFICATION_URLS = {
    "https://learn.microsoft.com/en-us/credentials",
    "https://learn.microsoft.com/en-us/credentials/",
    "https://learn.microsoft.com/credentials",
    "https://learn.microsoft.com/credentials/",
}
GENERIC_LEARN_ROOTS = {
    "https://learn.microsoft.com/",
    "https://learn.microsoft.com",
    "https://learn.microsoft.com/en-us/",
    "https://learn.microsoft.com/en-us",
}
EVIDENCE_KINDS = {
    "issuer_verification_tool",
    "issuer_authorized_badge_directory",
    "issuer_verification_process_documentation",
}
ISSUER_CREDLY_ORG_SLUGS: dict[str, set[str]] = {
    "google cloud": {"google-cloud"},
    "nvidia": {"nvidia"},
}
CREDLY_HOSTS = {"www.credly.com"}
CREDLY_ORG_SLUG_RE = re.compile(r"^[a-z0-9-]+$")
DOCUMENTATION_PATH_HINTS = (
    "share",
    "validat",
    "verif",
    "transcript",
    "credential",
)
BADGE_DIRECTORY_METHOD_HINTS = (
    "badge",
    "credly",
    "badge directory",
    "organization badge",
    "digital badge directory",
)
BADGE_DIRECTORY_METHOD_CONTRADICTIONS = (
    "verification tool",
    "verify tool",
    "direct verification",
    "direct credential verification",
    "direct exam verification",
    "exam verification tool",
    "certificate verification tool",
    "certificate verification endpoint",
    "validation endpoint",
    "credential lookup tool",
    "certificate lookup tool",
    "credential lookup endpoint",
    "lookup endpoint",
)
VERIFICATION_TOOL_METHOD_HINTS = (
    "verification tool",
    "verification service",
    "verification endpoint",
    "credential verification",
    "certificate verification",
)
VERIFICATION_TOOL_METHOD_CONTRADICTIONS = (
    "badge directory",
    "organization badge directory",
    "sharing documentation",
    "verification process documentation",
    "help article",
    "share-link process",
    "credential-sharing documentation",
)
PROCESS_DOCUMENTATION_METHOD_HINTS = (
    "process",
    "documentation",
    "sharing",
    "share-link",
    "share link",
    "online verifiable",
    "validation process",
    "credential profile",
)
PROCESS_DOCUMENTATION_METHOD_CONTRADICTIONS = (
    "verification tool",
    "verify tool",
    "direct verification tool",
    "exam verification endpoint",
    "certificate lookup tool",
    "credential lookup endpoint",
    "direct exam verification tool",
    "exam verification tool",
    "certificate verification tool",
)
GENERIC_RATIONALES = {
    "covers generative ai topics",
    "relevant to prompt engineering",
    "useful for learners",
    "official provider training",
}
GENERIC_VALIDITY = (
    "confirm current terms",
    "check issuer page",
    "see official website",
    "confirm terms on the issuer",
    "verify current",
    "confirm current nvidia",
    "confirm current aws",
    "confirm current google",
)


def load_json(root: Path, relative: str) -> Any:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def curriculum_lesson_ids(root: Path) -> set[str]:
    return {path.parent.name for path in (root / "curriculum").glob("*/README.md")}


def parse_day(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def related_credential_pairs(record: dict[str, Any]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in record.get("related_credentials", []):
        if not isinstance(item, dict):
            continue
        pairs.append((str(item.get("credential_id", "")), str(item.get("relationship", ""))))
    return pairs


def related_course_pairs(record: dict[str, Any]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in record.get("related_courses", []):
        if not isinstance(item, dict):
            continue
        pairs.append((str(item.get("course_id", "")), str(item.get("relationship", ""))))
    return pairs


def check_course_credential_quality(
    root: Path = ROOT, *, as_of: date | None = None
) -> tuple[list[str], list[str]]:
    today = as_of or utc_today()
    errors: list[str] = []
    details: list[str] = []
    courses = load_json(root, COURSE_PATH)
    credentials = load_json(root, CREDENTIAL_PATH)
    if not isinstance(courses, list) or not isinstance(credentials, list):
        return ([f"{COURSE_PATH}/{CREDENTIAL_PATH}: expected lists"], details)

    course_ids = {str(record.get("id", "")) for record in courses}
    credential_ids = {str(record.get("id", "")) for record in credentials}
    lesson_ids = curriculum_lesson_ids(root)
    individual_credentials = [
        record for record in credentials if record.get("entity_type") == "individual_credential"
    ]
    family_credentials = [
        record for record in credentials if record.get("entity_type") == "credential_family"
    ]
    type_counts = Counter(str(record.get("resource_type", "")) for record in courses)

    details.append(f"learning_resources={len(courses)}")
    details.append(f"credentials_total={len(credentials)}")
    details.append(f"credentials_individual={len(individual_credentials)}")
    details.append(f"credentials_family={len(family_credentials)}")
    for resource_type, count in sorted(type_counts.items()):
        details.append(f"format_{resource_type}={count}")

    _check_identity(courses, COURSE_PATH, errors)
    _check_identity(credentials, CREDENTIAL_PATH, errors)
    _check_course_semantics(courses, credential_ids, lesson_ids, today, errors)
    _check_credential_semantics(credentials, course_ids, today, errors)
    _check_relationship_agreement(courses, credentials, errors)
    _check_description_quality(courses, credentials, errors)

    return errors, details


def _check_identity(records: list[dict[str, Any]], label: str, errors: list[str]) -> None:
    ids = [str(record.get("id", "")) for record in records]
    urls = [str(record.get("canonical_url", "")) for record in records]
    titles = [normalize(str(record.get("title", ""))) for record in records]
    for value, counts in (
        ("id", Counter(ids)),
        ("canonical_url", Counter(urls)),
        ("title", Counter(titles)),
    ):
        for item, count in counts.items():
            if item and count > 1:
                errors.append(f"{label}: duplicate {value}: {item}")


def _check_course_semantics(
    courses: list[dict[str, Any]],
    credential_ids: set[str],
    lesson_ids: set[str],
    today: date,
    errors: list[str],
) -> None:
    for record in courses:
        course_id = str(record.get("id", "<missing>"))
        resource_type = str(record.get("resource_type", ""))
        outcome = str(record.get("credential_outcome", ""))
        access_model = str(record.get("access_model", ""))
        canonical_url = str(record.get("canonical_url", ""))

        if "/training/modules/" in canonical_url.lower() and resource_type == "structured_course":
            errors.append(
                f"{course_id}: Microsoft Learn modules must use learning_module, "
                "not structured_course"
            )

        if "certificate" in access_model and outcome == "completion_record":
            errors.append(
                f"{course_id}: access_model must not use certificate terminology when the "
                "outcome is only a completion/accomplishment record"
            )

        if resource_type == "learning_path" and outcome == "skill_badge":
            produces = [
                credential_id
                for credential_id, relationship in related_credential_pairs(record)
                if relationship == "produces"
            ]
            if not produces:
                errors.append(
                    f"{course_id}: learning_path cannot claim skill_badge without an explicit "
                    "produces relationship to a skill-badge credential"
                )

        pairs = related_credential_pairs(record)
        seen_pairs: set[tuple[str, str]] = set()
        targets: dict[str, set[str]] = {}
        for credential_id, relationship in pairs:
            if relationship not in RELATIONSHIP_VALUES:
                errors.append(f"{course_id}: invalid relationship {relationship}")
            if credential_id not in credential_ids:
                errors.append(f"{course_id}: missing related credential {credential_id}")
            pair = (credential_id, relationship)
            if pair in seen_pairs:
                errors.append(
                    f"{course_id}: duplicate relationship {relationship} -> {credential_id}"
                )
            seen_pairs.add(pair)
            targets.setdefault(credential_id, set()).add(relationship)
        for credential_id, relationships in targets.items():
            if "produces" in relationships and "official_preparation" in relationships:
                errors.append(
                    f"{course_id}: conflicting relationships for {credential_id}: "
                    "produces vs official_preparation"
                )

        if outcome == "no_credential" and any(
            relationship == "produces" for _, relationship in pairs
        ):
            errors.append(f"{course_id}: no_credential cannot use produces relationships")
        if (
            any(relationship == "produces" for _, relationship in pairs)
            and outcome not in PRODUCES_COMPATIBLE_OUTCOMES
        ):
            errors.append(
                f"{course_id}: produces relationship requires a compatible completion outcome"
            )

        relevance = str(record.get("prompt_engineering_relevance", ""))
        rationale = str(record.get("relevance_rationale", "")).strip()
        if not relevance:
            errors.append(f"{course_id}: missing prompt_engineering_relevance")
        if relevance == "direct" and len(rationale) < 24:
            errors.append(f"{course_id}: direct relevance requires a rationale")
        if normalize(rationale) in GENERIC_RATIONALES:
            errors.append(f"{course_id}: relevance rationale is generic")

        for lesson in record.get("related_lessons", []):
            if str(lesson) not in lesson_ids:
                errors.append(f"{course_id}: unknown related lesson {lesson}")

        _check_freshness_fields(course_id, record, today, errors)
        _check_url_hygiene(course_id, canonical_url, errors)


def _check_credential_semantics(
    credentials: list[dict[str, Any]],
    course_ids: set[str],
    today: date,
    errors: list[str],
) -> None:
    for record in credentials:
        credential_id = str(record.get("id", "<missing>"))
        credential_type = str(record.get("credential_type", ""))
        entity_type = str(record.get("entity_type", ""))
        assessment_required = bool(record.get("assessment_required"))
        assessment_type = str(record.get("assessment_type", ""))

        if credential_type == "formal_certification" and not assessment_required:
            errors.append(
                f"{credential_id}: formal_certification requires assessment_required=true"
            )
        if credential_type == "formal_certification" and assessment_type in {"none", "quiz"}:
            errors.append(
                f"{credential_id}: formal_certification needs an exam-grade assessment_type"
            )
        if entity_type == "credential_family" and credential_type == "formal_certification":
            errors.append(
                f"{credential_id}: credential families cannot be typed as formal_certification"
            )
        if entity_type == "individual_credential" and "family" in normalize(
            str(record.get("title", ""))
        ):
            errors.append(
                f"{credential_id}: individual credentials should not be titled as a family"
            )

        pairs = related_course_pairs(record)
        seen_pairs: set[tuple[str, str]] = set()
        targets: dict[str, set[str]] = {}
        for course_id, relationship in pairs:
            if relationship not in RELATIONSHIP_VALUES:
                errors.append(f"{credential_id}: invalid relationship {relationship}")
            if course_id not in course_ids:
                errors.append(f"{credential_id}: missing related course {course_id}")
            pair = (course_id, relationship)
            if pair in seen_pairs:
                errors.append(
                    f"{credential_id}: duplicate relationship {relationship} -> {course_id}"
                )
            seen_pairs.add(pair)
            targets.setdefault(course_id, set()).add(relationship)
        for course_id, relationships in targets.items():
            if "produces" in relationships and "official_preparation" in relationships:
                errors.append(
                    f"{credential_id}: conflicting relationships for {course_id}: "
                    "produces vs official_preparation"
                )

        if entity_type == "credential_family":
            verification = record.get("verification")
            if isinstance(verification, dict) and verification.get("available") is not False:
                errors.append(
                    f"{credential_id}: credential families must set verification.available=false"
                )

        _check_verification_fields(
            credential_id=credential_id,
            issuer=str(record.get("issuer", "")),
            verification=record.get("verification"),
            errors=errors,
        )

        validity = normalize(str(record.get("validity_summary", "")))
        if not validity:
            errors.append(f"{credential_id}: missing validity_summary")
        elif any(phrase in validity for phrase in GENERIC_VALIDITY):
            errors.append(f"{credential_id}: validity_summary is a generic disclaimer")

        relevance = str(record.get("prompt_engineering_relevance", ""))
        rationale = str(record.get("relevance_rationale", "")).strip()
        rationale_norm = normalize(rationale)
        if not relevance:
            errors.append(f"{credential_id}: missing prompt_engineering_relevance")
        if relevance == "direct" and "prompt" not in rationale_norm:
            errors.append(f"{credential_id}: direct relevance requires prompt-focused rationale")
        broad_direct = (
            relevance == "direct"
            and credential_type == "formal_certification"
            and "prompt-only" not in rationale_norm
            and "dedicated prompt" not in rationale_norm
        )
        if broad_direct:
            errors.append(
                f"{credential_id}: broad formal certifications should not be labeled direct"
            )
        if rationale_norm in GENERIC_RATIONALES:
            errors.append(f"{credential_id}: relevance rationale is generic")

        _check_freshness_fields(credential_id, record, today, errors)
        _check_url_hygiene(credential_id, str(record.get("canonical_url", "")), errors)


def _check_relationship_agreement(
    courses: list[dict[str, Any]],
    credentials: list[dict[str, Any]],
    errors: list[str],
) -> None:
    credential_by_id = {str(record["id"]): record for record in credentials if "id" in record}
    for course in courses:
        course_id = str(course.get("id", ""))
        for credential_id, relationship in related_credential_pairs(course):
            if relationship != "produces":
                continue
            credential = credential_by_id.get(credential_id)
            if credential is None:
                continue
            if credential.get("entity_type") == "credential_family":
                errors.append(
                    f"{course_id}: produces cannot target credential family {credential_id}"
                )
                continue
            reciprocal = related_course_pairs(credential)
            if (course_id, "produces") not in reciprocal:
                errors.append(
                    f"{course_id}: produces relationship to {credential_id} lacks reciprocal "
                    "produces link on the credential"
                )


def _check_description_quality(
    courses: list[dict[str, Any]],
    credentials: list[dict[str, Any]],
    errors: list[str],
) -> None:
    descriptions = []
    for record in courses + credentials:
        record_id = str(record.get("id", "<missing>"))
        description = str(record.get("description", ""))
        lowered = normalize(description)
        descriptions.append((record_id, lowered))
        for phrase in BANNED_MARKETING:
            if phrase in lowered:
                errors.append(f"{record_id}: marketing language detected ({phrase})")
        completion_outcomes = {
            "completion_certificate",
            "completion_record",
            "skill_badge",
            "digital_badge",
        }
        outcome = str(record.get("credential_outcome", ""))
        denies_cert = "not a formal certification" in lowered or "not a certification" in lowered
        if "certification" in lowered and outcome in completion_outcomes and not denies_cert:
            errors.append(
                f"{record_id}: completion-style outcomes must not be described as certifications"
            )
    for index, (left_id, left) in enumerate(descriptions):
        for right_id, right in descriptions[index + 1 :]:
            if left and left == right:
                errors.append(f"duplicate description: {left_id} ~ {right_id}")


def _check_freshness_fields(
    record_id: str, record: dict[str, Any], today: date, errors: list[str]
) -> None:
    raw = str(record.get("last_verified", ""))
    try:
        verified = parse_day(raw)
    except ValueError:
        errors.append(f"{record_id}: malformed last_verified")
        return
    if verified > today:
        errors.append(f"{record_id}: future last_verified {raw}")
    stale_after = record.get("stale_after_days")
    if not isinstance(stale_after, int) or stale_after < 1:
        errors.append(f"{record_id}: stale_after_days must be a positive integer")
        return
    age = (today - verified).days
    risk = str(record.get("stale_risk", ""))
    if risk == "high" and age > stale_after:
        errors.append(f"{record_id}: expired high-risk claim (age={age})")


def _check_verification_fields(
    *,
    credential_id: str,
    issuer: str,
    verification: Any,
    errors: list[str],
) -> None:
    if not isinstance(verification, dict):
        errors.append(f"{credential_id}: verification object is required")
        return

    available = verification.get("available")
    method = verification.get("method")
    evidence_kind = verification.get("evidence_kind")
    evidence_url = verification.get("evidence_url")

    if available is True:
        if not isinstance(method, str) or len(method.strip()) < 8:
            errors.append(f"{credential_id}: verification.available=true requires a method")
        if evidence_kind not in EVIDENCE_KINDS:
            errors.append(f"{credential_id}: verification.available=true requires evidence_kind")
        if not isinstance(evidence_url, str) or not evidence_url.strip():
            errors.append(f"{credential_id}: verification.available=true requires evidence_url")
        else:
            _check_evidence_url(
                credential_id=credential_id,
                issuer=issuer,
                evidence_kind=str(evidence_kind),
                evidence_url=evidence_url,
                method=method,
                errors=errors,
            )
    elif available in {False, "unknown"}:
        leftover = []
        if method is not None:
            leftover.append("method")
        if evidence_kind is not None:
            leftover.append("evidence_kind")
        if evidence_url is not None:
            leftover.append("evidence_url")
        if leftover:
            errors.append(
                f"{credential_id}: verification available=false/unknown must not invent "
                + ", ".join(leftover)
            )
    else:
        errors.append(f"{credential_id}: verification.available must be true/false/unknown")


def _normalize_issuer(value: str) -> str:
    return normalize(value)


def _normalize_evidence_url(url: str) -> str:
    parsed = urlparse(url.strip())
    path = parsed.path.rstrip("/") or "/"
    return f"{parsed.scheme.lower()}://{parsed.netloc.lower()}{path}"


def _is_microsoft_credentials_hub(url: str) -> bool:
    normalized = _normalize_evidence_url(url)
    if normalized in GENERIC_MICROSOFT_VERIFICATION_URLS:
        return True
    parsed = urlparse(normalized)
    if parsed.netloc != "learn.microsoft.com":
        return False
    parts = [part for part in parsed.path.split("/") if part]
    return parts == ["credentials"] or (len(parts) == 2 and parts[1] == "credentials")


def _credly_organization_slug(url: str) -> str | None:
    parsed = urlparse(url.strip())
    if parsed.scheme.lower() != "https":
        return None
    if parsed.netloc.lower() not in CREDLY_HOSTS:
        return None
    query = parsed.query.lower()
    if query:
        if "search" in query or any(marker in query for marker in TRACKING_QUERY_MARKERS):
            return None
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) != 3:
        return None
    if parts[0].lower() != "organizations" or parts[2].lower() != "badges":
        return None
    slug = parts[1].lower()
    if not CREDLY_ORG_SLUG_RE.fullmatch(slug):
        return None
    return slug


def _check_credly_issuer_compatibility(
    credential_id: str,
    issuer: str,
    evidence_url: str,
    errors: list[str],
) -> None:
    slug = _credly_organization_slug(evidence_url)
    if slug is None:
        errors.append(
            f"{credential_id}: badge-directory evidence_url must be an issuer-specific "
            "Credly organization badges path"
        )
        return

    issuer_key = _normalize_issuer(issuer)
    allowed = ISSUER_CREDLY_ORG_SLUGS.get(issuer_key)
    if allowed is None:
        errors.append(
            f"{credential_id}: no authorized Credly organization mapping exists for issuer "
            f"'{issuer}'"
        )
        return
    if slug not in allowed:
        errors.append(
            f"{credential_id}: Credly organization slug '{slug}' is not authorized for issuer "
            f"'{issuer}'"
        )


def _method_contains_any(method_norm: str, phrases: tuple[str, ...]) -> bool:
    return any(phrase in method_norm for phrase in phrases)


def _check_method_kind_consistency(
    credential_id: str,
    evidence_kind: str,
    method: str,
    errors: list[str],
) -> None:
    method_norm = normalize(method)
    if not method_norm:
        return

    if evidence_kind == "issuer_authorized_badge_directory":
        if _method_contains_any(method_norm, BADGE_DIRECTORY_METHOD_CONTRADICTIONS):
            errors.append(
                f"{credential_id}: method claims a direct verification or exam-verification "
                "tool but evidence_kind is badge directory"
            )
        elif not _method_contains_any(method_norm, BADGE_DIRECTORY_METHOD_HINTS):
            errors.append(
                f"{credential_id}: badge-directory method must describe a badge directory "
                "or Credly organization directory"
            )
    elif evidence_kind == "issuer_verification_tool":
        if _method_contains_any(method_norm, VERIFICATION_TOOL_METHOD_CONTRADICTIONS):
            errors.append(
                f"{credential_id}: method describes badge-directory or documentation evidence "
                "but evidence_kind is verification tool"
            )
        elif not _method_contains_any(method_norm, VERIFICATION_TOOL_METHOD_HINTS):
            errors.append(
                f"{credential_id}: verification-tool method must describe an issuer "
                "verification tool or endpoint"
            )
    elif evidence_kind == "issuer_verification_process_documentation":
        if _method_contains_any(method_norm, PROCESS_DOCUMENTATION_METHOD_CONTRADICTIONS):
            errors.append(
                f"{credential_id}: method claims a direct lookup or exam-verification tool "
                "but evidence_kind is process documentation"
            )
        elif not _method_contains_any(method_norm, PROCESS_DOCUMENTATION_METHOD_HINTS):
            errors.append(
                f"{credential_id}: process-documentation method must describe sharing, "
                "validation, or verification process documentation"
            )


def _check_evidence_url(
    *,
    credential_id: str,
    issuer: str,
    evidence_kind: str,
    evidence_url: str,
    method: Any,
    errors: list[str],
) -> None:
    lowered = evidence_url.lower().strip()
    if not lowered.startswith("https://"):
        errors.append(f"{credential_id}: verification evidence_url must use https")
        return

    _check_url_hygiene(f"{credential_id}.verification.evidence_url", evidence_url, errors)
    normalized = _normalize_evidence_url(evidence_url)

    if _is_microsoft_credentials_hub(evidence_url):
        errors.append(
            f"{credential_id}: Microsoft Credentials marketing hub is not verification evidence"
        )
    if normalized in GENERIC_LEARN_ROOTS:
        errors.append(f"{credential_id}: generic Microsoft Learn root is not verification evidence")
    if normalized in {"https://www.credly.com", "https://www.credly.com/"}:
        errors.append(f"{credential_id}: generic Credly homepage is not verification evidence")
    if "credly.com/search" in lowered or re.search(r"credly\.com/\?.*search", lowered):
        errors.append(f"{credential_id}: generic Credly search is not verification evidence")

    if evidence_kind == "issuer_authorized_badge_directory":
        _check_credly_issuer_compatibility(credential_id, issuer, evidence_url, errors)
    elif evidence_kind == "issuer_verification_tool":
        if (
            "verification" not in lowered
            and "verify" not in lowered
            and "certmetrics" not in lowered
        ):
            errors.append(
                f"{credential_id}: verification-tool evidence_url must point to an issuer "
                "verification endpoint"
            )
    elif evidence_kind == "issuer_verification_process_documentation" and not any(
        hint in lowered for hint in DOCUMENTATION_PATH_HINTS
    ):
        errors.append(
            f"{credential_id}: verification-process documentation URL must describe "
            "sharing, validation, verification, transcripts, or credentials"
        )

    if isinstance(method, str) and evidence_kind in EVIDENCE_KINDS:
        _check_method_kind_consistency(credential_id, evidence_kind, method, errors)


def _check_url_hygiene(record_id: str, url: str, errors: list[str]) -> None:
    lowered = url.lower()
    if not lowered.startswith("https://"):
        errors.append(f"{record_id}: canonical_url must use https")
        return
    parsed = urlparse(url)
    if not parsed.netloc:
        errors.append(f"{record_id}: canonical_url is incomplete")
    for marker in TRACKING_QUERY_MARKERS:
        if marker in lowered:
            errors.append(f"{record_id}: canonical_url contains tracking/affiliate marker {marker}")
    for marker in INACTIVE_URL_MARKERS:
        if marker in lowered:
            errors.append(
                f"{record_id}: canonical_url looks like a search/inactive redirect page ({marker})"
            )
    for fragment in KNOWN_INACTIVE_AWS_COURSE_FRAGMENTS:
        if fragment in lowered:
            errors.append(f"{record_id}: known inactive AWS Skill Builder URL fragment {fragment}")


def main() -> int:
    errors, details = check_course_credential_quality()
    for line in details:
        print(line)
    if errors:
        print("Course/credential quality check failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Course/credential quality check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
