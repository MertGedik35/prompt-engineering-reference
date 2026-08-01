from __future__ import annotations

import copy
import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from scripts.course_credential_quality import check_course_credential_quality
from scripts.generate_docs_indexes import format_breakdown, write_outputs
from scripts.validate_schemas import validate_all

ROOT = Path(__file__).resolve().parents[1]
COURSE_SCHEMA = json.loads((ROOT / "schemas/course.schema.json").read_text(encoding="utf-8"))
CREDENTIAL_SCHEMA = json.loads(
    (ROOT / "schemas/credential.schema.json").read_text(encoding="utf-8")
)
COURSE_VALIDATOR = Draft202012Validator(COURSE_SCHEMA, format_checker=FormatChecker())
CREDENTIAL_VALIDATOR = Draft202012Validator(CREDENTIAL_SCHEMA, format_checker=FormatChecker())


def load(name: str) -> list[dict[str, Any]]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def mutate_course(course_id: str, **updates: Any) -> list[dict[str, Any]]:
    records = load("catalog/courses.json")
    for record in records:
        if record["id"] == course_id:
            record.update(updates)
            return records
    raise AssertionError(f"missing course {course_id}")


def mutate_credential(credential_id: str, **updates: Any) -> list[dict[str, Any]]:
    records = load("catalog/credentials.json")
    for record in records:
        if record["id"] == credential_id:
            record.update(updates)
            return records
    raise AssertionError(f"missing credential {credential_id}")


def write_catalogs(
    tmp_path: Path,
    courses: list[dict[str, Any]] | None = None,
    credentials: list[dict[str, Any]] | None = None,
) -> Path:
    root = tmp_path
    (root / "catalog").mkdir(parents=True, exist_ok=True)
    for lesson in (
        "00-orientation",
        "02-prompt-anatomy",
        "03-core-techniques",
        "04-grounding-and-long-context",
        "06-evaluation",
        "07-agents-and-tools",
        "09-security",
        "10-multimodal",
    ):
        lesson_dir = root / "curriculum" / lesson
        lesson_dir.mkdir(parents=True, exist_ok=True)
        (lesson_dir / "README.md").write_text("# lesson\n", encoding="utf-8")
    (root / "catalog" / "courses.json").write_text(
        json.dumps(courses if courses is not None else load("catalog/courses.json"), indent=2),
        encoding="utf-8",
    )
    (root / "catalog" / "credentials.json").write_text(
        json.dumps(
            credentials if credentials is not None else load("catalog/credentials.json"),
            indent=2,
        ),
        encoding="utf-8",
    )
    return root


def schema_errors(record: dict[str, Any], *, kind: str) -> list[str]:
    validator = COURSE_VALIDATOR if kind == "course" else CREDENTIAL_VALIDATOR
    return [error.message for error in sorted(validator.iter_errors(record), key=lambda e: e.path)]


def test_current_course_credential_quality_passes() -> None:
    errors, details = check_course_credential_quality(ROOT)
    assert errors == []
    assert any(item.startswith("learning_resources=") for item in details)


def test_schema_validation_includes_course_and_credential_schemas() -> None:
    counts, errors = validate_all()
    assert errors == []
    assert counts["courses"] == 8
    assert counts["credentials"] == 5


def test_schema_rejects_course_formal_certification() -> None:
    record = copy.deepcopy(load("catalog/courses.json")[0])
    record["credential_outcome"] = "formal_certification"
    assert any(
        "formal_certification" in message for message in schema_errors(record, kind="course")
    )


def test_schema_rejects_example_collection() -> None:
    record = copy.deepcopy(load("catalog/courses.json")[0])
    record["resource_type"] = "example_collection"
    assert any("example_collection" in message for message in schema_errors(record, kind="course"))


def test_schema_rejects_documentation_series() -> None:
    record = copy.deepcopy(load("catalog/courses.json")[0])
    record["resource_type"] = "documentation_series"
    assert any(
        "documentation_series" in message for message in schema_errors(record, kind="course")
    )


def test_schema_rejects_namespace_invalid_related_credential_id() -> None:
    record = copy.deepcopy(load("catalog/courses.json")[0])
    record["related_credentials"] = [
        {"credential_id": "course-anthropic-prompt-engineering", "relationship": "produces"}
    ]
    assert schema_errors(record, kind="course")


def test_schema_rejects_namespace_invalid_related_course_id() -> None:
    record = copy.deepcopy(load("catalog/credentials.json")[0])
    record["related_courses"] = [
        {"course_id": "credential-aws-ai-practitioner", "relationship": "official_preparation"}
    ]
    assert schema_errors(record, kind="credential")


def test_rejects_search_result_canonical_url(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-aws-foundations-of-prompt-engineering",
        canonical_url=(
            "https://skillbuilder.aws/search?searchText=foundations-of-prompt-engineering"
            "&showRedirectNotFoundBanner=true"
        ),
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("search/inactive redirect" in error for error in errors)


def test_rejects_google_path_skill_badge_without_produces(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-google-generative-ai-learning",
        credential_outcome="skill_badge",
        related_credentials=[],
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("cannot claim skill_badge" in error for error in errors)


def test_rejects_deeplearning_certificate_access_for_accomplishment(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-deeplearning-ai-chatgpt-prompt-engineering",
        access_model="free_audit_paid_certificate",
        credential_outcome="completion_record",
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("certificate terminology" in error for error in errors)


def test_rejects_microsoft_module_as_structured_course(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-microsoft-generative-ai-solutions",
        resource_type="structured_course",
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("learning_module" in error for error in errors)


def test_rejects_family_counted_without_family_entity_type(tmp_path: Path) -> None:
    credentials = mutate_credential(
        "credential-microsoft-applied-skills",
        entity_type="individual_credential",
        title="Microsoft Applied Skills family",
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, credentials=credentials))
    assert any("family" in error for error in errors)


def test_rejects_missing_related_credential_target(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-deeplearning-ai-chatgpt-prompt-engineering",
        credential_outcome="completion_record",
        related_credentials=[
            {"credential_id": "credential-does-not-exist", "relationship": "recommended_learning"}
        ],
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("missing related credential" in error for error in errors)


def test_rejects_missing_related_course_target(tmp_path: Path) -> None:
    credentials = mutate_credential(
        "credential-aws-ai-practitioner",
        related_courses=[
            {"course_id": "course-does-not-exist", "relationship": "recommended_learning"}
        ],
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, credentials=credentials))
    assert any("missing related course" in error for error in errors)


def test_rejects_invalid_relationship_enum(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-anthropic-prompt-engineering",
        related_credentials=[
            {
                "credential_id": "credential-aws-ai-practitioner",
                "relationship": "related",
            }
        ],
    )
    # schema would also reject; quality catches when used outside schema
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("invalid relationship" in error for error in errors)


def test_rejects_duplicate_typed_relationship(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-anthropic-prompt-engineering",
        credential_outcome="completion_record",
        related_credentials=[
            {
                "credential_id": "credential-aws-ai-practitioner",
                "relationship": "recommended_learning",
            },
            {
                "credential_id": "credential-aws-ai-practitioner",
                "relationship": "recommended_learning",
            },
        ],
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("duplicate relationship" in error for error in errors)


def test_rejects_conflicting_relationships(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-anthropic-prompt-engineering",
        credential_outcome="completion_record",
        related_credentials=[
            {"credential_id": "credential-aws-ai-practitioner", "relationship": "produces"},
            {
                "credential_id": "credential-aws-ai-practitioner",
                "relationship": "official_preparation",
            },
        ],
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("conflicting relationships" in error for error in errors)


def test_rejects_produces_without_compatible_outcome(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-anthropic-prompt-engineering",
        credential_outcome="no_credential",
        related_credentials=[
            {"credential_id": "credential-aws-ai-practitioner", "relationship": "produces"}
        ],
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any(
        "cannot use produces" in error or "compatible completion" in error for error in errors
    )


def test_rejects_one_way_produces_without_reciprocal(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-anthropic-prompt-engineering",
        credential_outcome="completion_record",
        related_credentials=[
            {"credential_id": "credential-aws-ai-practitioner", "relationship": "produces"}
        ],
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("lacks reciprocal produces" in error for error in errors)


def test_rejects_verification_true_without_method(tmp_path: Path) -> None:
    credentials = mutate_credential(
        "credential-aws-ai-practitioner",
        verification={"available": True},
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, credentials=credentials))
    assert any("requires a method" in error for error in errors)


def test_rejects_verification_url_tracking(tmp_path: Path) -> None:
    credentials = mutate_credential(
        "credential-aws-ai-practitioner",
        verification={
            "available": True,
            "method": "AWS Certification verification tool",
            "url": "https://aws.amazon.com/verification/?utm_source=affiliate",
        },
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, credentials=credentials))
    assert any("tracking/affiliate" in error for error in errors)


def test_rejects_generic_validity_disclaimer(tmp_path: Path) -> None:
    credentials = mutate_credential(
        "credential-aws-ai-practitioner",
        validity_summary="Confirm current terms on the issuer page before relying on this summary.",
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, credentials=credentials))
    assert any("generic disclaimer" in error for error in errors)


def test_rejects_completion_certificate_described_as_certification(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-microsoft-generative-ai-solutions",
        credential_outcome="completion_certificate",
        description="This module grants a certification for every learner who finishes the units.",
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("must not be described as certifications" in error for error in errors)


def test_rejects_duplicate_canonical_url(tmp_path: Path) -> None:
    courses = load("catalog/courses.json")
    courses[1]["canonical_url"] = courses[0]["canonical_url"]
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("duplicate canonical_url" in error for error in errors)


def test_rejects_future_last_verified(tmp_path: Path) -> None:
    future = (date(2026, 8, 1) + timedelta(days=14)).isoformat()
    courses = mutate_course("course-anthropic-prompt-engineering", last_verified=future)
    errors, _ = check_course_credential_quality(
        write_catalogs(tmp_path, courses=courses), as_of=date(2026, 8, 1)
    )
    assert any("future last_verified" in error for error in errors)


def test_rejects_expired_high_risk_claim(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-google-generative-ai-learning",
        last_verified="2025-01-01",
        stale_after_days=30,
        stale_risk="high",
    )
    errors, _ = check_course_credential_quality(
        write_catalogs(tmp_path, courses=courses), as_of=date(2026, 8, 1)
    )
    assert any("expired high-risk claim" in error for error in errors)


def test_rejects_missing_prompt_relevance(tmp_path: Path) -> None:
    courses = mutate_course("course-anthropic-prompt-engineering", prompt_engineering_relevance="")
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("missing prompt_engineering_relevance" in error for error in errors)


def test_rejects_direct_relevance_without_rationale(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-anthropic-prompt-engineering",
        prompt_engineering_relevance="direct",
        relevance_rationale="too short",
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("direct relevance requires a rationale" in error for error in errors)


def test_rejects_broad_ai_cert_labeled_direct(tmp_path: Path) -> None:
    credentials = mutate_credential(
        "credential-google-generative-ai-leader",
        prompt_engineering_relevance="direct",
        relevance_rationale="Includes some prompt topics inside a leadership certification.",
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, credentials=credentials))
    assert any("should not be labeled direct" in error for error in errors)


def test_rejects_duplicate_provider_neutral_description(tmp_path: Path) -> None:
    courses = load("catalog/courses.json")
    courses[1]["description"] = courses[0]["description"]
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("duplicate description" in error for error in errors)


def test_format_breakdown_tracks_catalog_changes() -> None:
    courses = load("catalog/courses.json")
    before = format_breakdown(courses)
    reduced = [record for record in courses if record["id"] != "course-anthropic-prompt-evals"]
    after = format_breakdown(reduced)
    assert before != after
    assert "exercise repository" in before
    assert "exercise repository" not in after


def test_positive_aws_durable_url_and_no_unsupported_prep() -> None:
    record = next(
        item
        for item in load("catalog/courses.json")
        if item["id"] == "course-aws-foundations-of-prompt-engineering"
    )
    assert "VF6H4SZ1BU" in record["canonical_url"]
    assert "17763" not in record["canonical_url"]
    assert record["access_model"] == "free_with_account"
    assert record["credential_outcome"] == "no_credential"
    credential = next(
        item
        for item in load("catalog/credentials.json")
        if item["id"] == "credential-aws-ai-practitioner"
    )
    assert credential["related_courses"] == []


def test_positive_deeplearning_access_and_outcome() -> None:
    record = next(
        item
        for item in load("catalog/courses.json")
        if item["id"] == "course-deeplearning-ai-chatgpt-prompt-engineering"
    )
    assert record["access_model"] == "free_with_optional_paid_completion"
    assert record["credential_outcome"] == "completion_record"
    assert "certificate" not in record["access_model"]


def test_positive_google_path_no_path_level_skill_badge() -> None:
    record = next(
        item
        for item in load("catalog/courses.json")
        if item["id"] == "course-google-generative-ai-learning"
    )
    assert record["title"] == "Beginner: Introduction to Generative AI"
    assert record["credential_outcome"] == "no_credential"
    assert record["related_credentials"] == []


def test_positive_microsoft_learning_module() -> None:
    record = next(
        item
        for item in load("catalog/courses.json")
        if item["id"] == "course-microsoft-generative-ai-solutions"
    )
    assert record["resource_type"] == "learning_module"
    assert record["credential_outcome"] == "completion_record"
    assert "not a formal certification" in record["description"].lower()


def test_positive_applied_skill_and_family_separation() -> None:
    credentials = {item["id"]: item for item in load("catalog/credentials.json")}
    assert credentials["credential-microsoft-applied-skills"]["entity_type"] == "credential_family"
    assert credentials["credential-microsoft-agent-tools"]["entity_type"] == "individual_credential"
    assert (
        credentials["credential-microsoft-agent-tools"]["credential_type"]
        == "applied_skill_credential"
    )


def test_positive_verification_and_validity_evidence() -> None:
    for record in load("catalog/credentials.json"):
        verification = record["verification"]
        assert verification["available"] is True
        assert len(verification["method"]) >= 8
        assert str(verification["url"]).startswith("https://")
        assert "confirm current terms" not in record["validity_summary"].lower()


def test_positive_nvidia_and_google_relationships_empty() -> None:
    credentials = {item["id"]: item for item in load("catalog/credentials.json")}
    assert credentials["credential-nvidia-genai-llm-associate"]["related_courses"] == []
    assert credentials["credential-google-generative-ai-leader"]["related_courses"] == []


def test_generated_course_and_credential_indexes_are_current() -> None:
    assert write_outputs(check=True) == []


def test_generated_course_index_mutation_fails_check() -> None:
    from scripts import generate_docs_indexes as generator

    target = ROOT / "docs/generated/course-index.md"
    original = target.read_text(encoding="utf-8")
    try:
        target.write_text(original + "\n<!-- mutated -->\n", encoding="utf-8")
        assert "docs/generated/course-index.md" in generator.write_outputs(check=True)
    finally:
        target.write_text(original, encoding="utf-8")


def test_generated_credential_index_mutation_fails_check() -> None:
    from scripts import generate_docs_indexes as generator

    target = ROOT / "docs/generated/credential-index.md"
    original = target.read_text(encoding="utf-8")
    try:
        target.write_text(
            original.replace("# Credentials", "# Credentials mutated"), encoding="utf-8"
        )
        assert "docs/generated/credential-index.md" in generator.write_outputs(check=True)
    finally:
        target.write_text(original, encoding="utf-8")


def test_openai_cookbook_is_not_in_course_catalog() -> None:
    ids = {record["id"] for record in load("catalog/courses.json")}
    assert "course-openai-cookbook-evals" not in ids
    repo_ids = {record["id"] for record in load("catalog/repositories.json")}
    assert "repo-openai-cookbook" in repo_ids


def test_openai_cookbook_human_readable_discovery() -> None:
    resources = (ROOT / "docs/resources/index.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "OpenAI Cookbook" in resources
    assert "OpenAI Cookbook" in readme
    assert "docs/generated/repository-index.md" in readme
