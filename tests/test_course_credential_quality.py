from __future__ import annotations

import copy
import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import pytest

from scripts.course_credential_quality import check_course_credential_quality
from scripts.generate_docs_indexes import write_outputs
from scripts.validate_schemas import validate_all

ROOT = Path(__file__).resolve().parents[1]


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
    (root / "curriculum" / "02-prompt-anatomy").mkdir(parents=True, exist_ok=True)
    (root / "curriculum" / "02-prompt-anatomy" / "README.md").write_text(
        "# lesson\n", encoding="utf-8"
    )
    for lesson in (
        "00-orientation",
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


def test_current_course_credential_quality_passes() -> None:
    errors, _ = check_course_credential_quality(ROOT)
    assert errors == []


def test_schema_validation_includes_course_and_credential_schemas() -> None:
    counts, errors = validate_all()
    assert errors == []
    assert counts["courses"] == 8
    assert counts["credentials"] == 5


def test_rejects_anthropic_tutorial_as_formal_certification(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-anthropic-prompt-engineering",
        credential_outcome="formal_certification",
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("formal_certification" in error for error in errors)


def test_rejects_microsoft_module_as_formal_certification(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-microsoft-generative-ai-solutions",
        credential_outcome="formal_certification",
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("formal_certification" in error for error in errors)


def test_rejects_example_collection_classified_as_course(tmp_path: Path) -> None:
    courses = load("catalog/courses.json")
    courses.append(
        {
            **copy.deepcopy(courses[0]),
            "id": "course-openai-cookbook-evals",
            "title": "OpenAI Cookbook evaluation examples",
            "canonical_url": "https://github.com/openai/openai-cookbook/tree/main/examples/evaluation",
            "resource_type": "example_collection",
            "description": (
                "Evaluation examples relocated incorrectly back into the course catalog."
            ),
            "relevance_rationale": "Example notebooks are not a structured learner journey.",
        }
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("example collections" in error or "example_collection" in error for error in errors)


def test_rejects_formal_certification_without_assessment(tmp_path: Path) -> None:
    credentials = mutate_credential(
        "credential-aws-ai-practitioner",
        assessment_required=False,
        assessment_type="none",
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, credentials=credentials))
    assert any("assessment_required=true" in error for error in errors)


def test_rejects_completion_certificate_described_as_certification(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-microsoft-generative-ai-solutions",
        credential_outcome="completion_certificate",
        description="This module grants a certification for every learner who finishes the units.",
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("must not be described as certifications" in error for error in errors)


def test_rejects_family_counted_without_family_entity_type(tmp_path: Path) -> None:
    credentials = mutate_credential(
        "credential-microsoft-applied-skills",
        entity_type="individual_credential",
        title="Microsoft Applied Skills family",
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, credentials=credentials))
    assert any("family" in error for error in errors)


def test_rejects_missing_related_credential(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-deeplearning-ai-chatgpt-prompt-engineering",
        credential_outcome="completion_record",
        related_credential_ids=["credential-does-not-exist"],
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("missing related credential" in error for error in errors)


def test_rejects_missing_related_course(tmp_path: Path) -> None:
    credentials = mutate_credential(
        "credential-aws-ai-practitioner",
        related_course_ids=["course-does-not-exist"],
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, credentials=credentials))
    assert any("missing related course" in error for error in errors)


def test_rejects_self_referencing_course_relationship(tmp_path: Path) -> None:
    credentials = load("catalog/credentials.json")
    for record in credentials:
        if record["id"] == "credential-aws-ai-practitioner":
            record["related_course_ids"] = ["credential-aws-ai-practitioner"]
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, credentials=credentials))
    assert any("self-referencing" in error for error in errors)


def test_rejects_duplicate_canonical_url(tmp_path: Path) -> None:
    courses = load("catalog/courses.json")
    courses[1]["canonical_url"] = courses[0]["canonical_url"]
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("duplicate canonical_url" in error for error in errors)


def test_rejects_no_credential_linked_to_produced_credential(tmp_path: Path) -> None:
    courses = mutate_course(
        "course-anthropic-prompt-engineering",
        credential_outcome="no_credential",
        related_credential_ids=["credential-aws-ai-practitioner"],
    )
    errors, _ = check_course_credential_quality(write_catalogs(tmp_path, courses=courses))
    assert any("no_credential courses cannot link related credentials" in error for error in errors)


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


def test_positive_free_structured_course_with_no_credential() -> None:
    record = next(
        item
        for item in load("catalog/courses.json")
        if item["id"] == "course-aws-foundations-of-prompt-engineering"
    )
    assert record["access_model"] == "free_with_account"
    assert record["credential_outcome"] == "no_credential"


def test_positive_free_course_with_optional_paid_certificate_path() -> None:
    record = next(
        item
        for item in load("catalog/courses.json")
        if item["id"] == "course-deeplearning-ai-chatgpt-prompt-engineering"
    )
    assert record["access_model"] == "free_audit_paid_certificate"
    assert record["credential_outcome"] == "completion_record"


def test_positive_learning_path_with_lab_credits() -> None:
    record = next(
        item
        for item in load("catalog/courses.json")
        if item["id"] == "course-google-generative-ai-learning"
    )
    assert record["resource_type"] == "learning_path"
    assert record["access_model"] == "lab_credits"


def test_positive_completion_record_distinct_from_certification() -> None:
    record = next(
        item
        for item in load("catalog/courses.json")
        if item["id"] == "course-microsoft-generative-ai-solutions"
    )
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


def test_positive_formal_certification_with_exam_evidence() -> None:
    record = next(
        item
        for item in load("catalog/credentials.json")
        if item["id"] == "credential-aws-ai-practitioner"
    )
    assert record["credential_type"] == "formal_certification"
    assert record["assessment_required"] is True
    assert record["assessment_type"] == "exam"


def test_positive_broad_ai_classification() -> None:
    record = next(
        item
        for item in load("catalog/credentials.json")
        if item["id"] == "credential-google-generative-ai-leader"
    )
    assert record["prompt_engineering_relevance"] == "broad_ai"


def test_generated_course_and_credential_indexes_are_current() -> None:
    assert write_outputs(check=True) == []


def test_generated_course_index_mutation_fails_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
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
