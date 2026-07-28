from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from scripts.check_content_quality import run_checks
from scripts.validate_catalog import validate

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> list[dict[str, Any]]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_catalog_validation_passes() -> None:
    _, errors = validate()
    assert errors == []


def test_content_quality_passes() -> None:
    _, errors = run_checks()
    assert errors == []


def test_template_prompts_are_task_specific() -> None:
    prompts = [record["prompt"] for record in load("catalog/templates.json")]
    assert len(prompts) == len(set(prompts))


def test_template_acceptance_blocks_are_not_reused() -> None:
    blocks = [
        json.dumps(record["acceptance_criteria"], sort_keys=True)
        for record in load("catalog/templates.json")
    ]
    assert len(blocks) == len(set(blocks))


def test_template_failure_blocks_are_not_reused() -> None:
    blocks = [
        json.dumps(record["failure_modes"], sort_keys=True)
        for record in load("catalog/templates.json")
    ]
    assert len(blocks) == len(set(blocks))


def test_pattern_mechanisms_are_unique() -> None:
    mechanisms = [record["mechanism"] for record in load("catalog/patterns.json")]
    assert len(mechanisms) == len(set(mechanisms))


def test_patterns_have_bad_and_good_examples() -> None:
    for record in load("catalog/patterns.json"):
        assert record["example_prompt"]
        assert record["bad_prompt"]


def test_prompt_contracts_are_copyable() -> None:
    for record in load("catalog/prompt_contracts.json"):
        assert "Required sections" in str(record["copyable_prompt"])


def test_doctor_references_valid_patterns() -> None:
    pattern_ids = {record["id"] for record in load("catalog/patterns.json")}
    for record in load("catalog/prompt_doctor.json"):
        assert record["relevant_pattern"] in pattern_ids


def test_templates_reference_valid_patterns() -> None:
    pattern_ids = {record["id"] for record in load("catalog/patterns.json")}
    for record in load("catalog/templates.json"):
        assert record["related_pattern"] in pattern_ids


def test_provider_sources_exist() -> None:
    resources = {
        record["id"]
        for file in ["catalog/official-resources.json", "catalog/repositories.json"]
        for record in load(file)
    }
    for record in load("catalog/provider-guides.json"):
        assert set(record["official_source_ids"]).issubset(resources)


def test_courses_have_pricing_classification() -> None:
    for record in load("catalog/courses.json"):
        assert record["pricing_type"] in {
            "free",
            "paid",
            "freemium",
            "subscription",
            "lab_credits",
            "unknown",
        }


def test_credentials_have_credential_classification() -> None:
    for record in load("catalog/credentials.json"):
        assert record["credential_type"] in {
            "formal_certification",
            "applied_skill_badge",
            "course_completion_certificate",
            "professional_certificate_program",
            "skill_badge",
            "no_credential",
        }


def test_resource_urls_are_unique() -> None:
    files = [
        "catalog/official-resources.json",
        "catalog/repositories.json",
        "catalog/courses.json",
        "catalog/credentials.json",
        "catalog/videos.json",
        "catalog/papers.json",
        "catalog/books.json",
        "catalog/tools.json",
        "catalog/communities.json",
    ]
    urls = [record["canonical_url"] for file in files for record in load(file)]
    assert len(urls) == len(set(urls))


def test_time_sensitive_records_have_freshness() -> None:
    files = [
        "catalog/official-resources.json",
        "catalog/courses.json",
        "catalog/credentials.json",
        "catalog/provider-guides.json",
    ]
    for file in files:
        for record in load(file):
            assert record["last_verified"]
            assert record["stale_after_days"]
            assert record["stale_risk"]
