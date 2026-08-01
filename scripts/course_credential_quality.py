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

        verification = record.get("verification")
        if not isinstance(verification, dict):
            errors.append(f"{credential_id}: verification object is required")
        else:
            available = verification.get("available")
            method = verification.get("method")
            url = verification.get("url")
            if available is True:
                if not isinstance(method, str) or len(method.strip()) < 8:
                    errors.append(f"{credential_id}: verification.available=true requires a method")
                if url is not None:
                    _check_url_hygiene(f"{credential_id}.verification", str(url), errors)
            elif available in {False, "unknown"}:
                if method is not None or url is not None:
                    errors.append(
                        f"{credential_id}: verification unavailable/unknown must not invent "
                        "method or url fields"
                    )
            else:
                errors.append(f"{credential_id}: verification.available must be true/false/unknown")

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
