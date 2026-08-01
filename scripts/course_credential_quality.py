from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any

try:
    from .check_freshness import utc_today
except ImportError:  # pragma: no cover
    from check_freshness import utc_today  # type: ignore[import-not-found,no-redef]

ROOT = Path(__file__).resolve().parents[1]
COURSE_PATH = "catalog/courses.json"
CREDENTIAL_PATH = "catalog/credentials.json"
BANNED_MARKETING = (
    "best course",
    "guaranteed job",
    "guaranteed certification",
    "world-class",
    "number one",
    "#1",
)
TRACKING_QUERY_MARKERS = ("utm_", "ref=", "affiliate", "coupon", "referral")
GENERIC_RATIONALES = {
    "covers generative ai topics",
    "relevant to prompt engineering",
    "useful for learners",
    "official provider training",
}


def load_json(root: Path, relative: str) -> Any:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def curriculum_lesson_ids(root: Path) -> set[str]:
    return {path.parent.name for path in (root / "curriculum").glob("*/README.md")}


def parse_day(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


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

    details.append(f"courses={len(courses)}")
    details.append(f"credentials_total={len(credentials)}")
    details.append(f"credentials_individual={len(individual_credentials)}")
    details.append(f"credentials_family={len(family_credentials)}")

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
    disallowed_types = {"example_collection", "documentation_series"}
    for record in courses:
        course_id = str(record.get("id", "<missing>"))
        resource_type = str(record.get("resource_type", ""))
        if resource_type in disallowed_types:
            errors.append(
                f"{course_id}: resource_type {resource_type} is not allowed in the course catalog"
            )
        if resource_type == "example_collection":
            errors.append(f"{course_id}: example collections must not be classified as courses")

        outcome = str(record.get("credential_outcome", ""))
        related = [str(item) for item in record.get("related_credential_ids", [])]
        if course_id in related:
            errors.append(f"{course_id}: self-referencing related_credential_ids")
        for credential_id in related:
            if credential_id not in credential_ids:
                errors.append(f"{course_id}: missing related credential {credential_id}")
        if outcome == "no_credential" and related:
            errors.append(f"{course_id}: no_credential courses cannot link related credentials")
        if outcome == "formal_certification":
            errors.append(
                f"{course_id}: courses cannot claim formal_certification as a course outcome"
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
        _check_url_hygiene(course_id, str(record.get("canonical_url", "")), errors)


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

        related = [str(item) for item in record.get("related_course_ids", [])]
        if credential_id in related:
            errors.append(f"{credential_id}: self-referencing related_course_ids")
        for course_id in related:
            if course_id not in course_ids:
                errors.append(f"{credential_id}: missing related course {course_id}")

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
    course_by_id = {str(record["id"]): record for record in courses if "id" in record}
    credential_by_id = {str(record["id"]): record for record in credentials if "id" in record}
    for course in courses:
        course_id = str(course.get("id", ""))
        for credential_id in course.get("related_credential_ids", []):
            credential = credential_by_id.get(str(credential_id))
            if credential is None:
                continue
            if course_id not in [str(item) for item in credential.get("related_course_ids", [])]:
                errors.append(
                    f"{course_id}: related credential {credential_id} lacks reciprocal course link"
                )
    for credential in credentials:
        for course_id in credential.get("related_course_ids", []):
            if str(course_id) not in course_by_id:
                # Missing IDs are already reported in credential semantics.
                continue
            # Prep-only credential→course links may omit reciprocity.


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
    for marker in TRACKING_QUERY_MARKERS:
        if marker in lowered:
            errors.append(f"{record_id}: canonical_url contains tracking/affiliate marker {marker}")


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
