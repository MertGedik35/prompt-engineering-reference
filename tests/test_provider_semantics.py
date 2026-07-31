from __future__ import annotations

import copy
import json
import shutil
from datetime import date
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from scripts.provider_quality import (
    EXPECTED_PROVIDERS,
    PROVIDER_SOURCE_LESSONS,
    check_provider_quality,
    provider_cross_document_errors,
    provider_document_errors,
    provider_record_errors,
)

ROOT = Path(__file__).resolve().parents[1]
AS_OF = date(2026, 7, 31)


def load(path: str) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def providers() -> list[dict[str, Any]]:
    return load("catalog/provider-guides.json")


def resources() -> dict[str, dict[str, Any]]:
    return {
        record["id"]: record
        for path in ("catalog/official-resources.json", "catalog/repositories.json")
        for record in load(path)
    }


def openai_fixture() -> tuple[dict[str, Any], str]:
    record = next(record for record in providers() if record["id"] == "provider-openai")
    text = (ROOT / "docs" / "providers" / "openai.md").read_text(encoding="utf-8")
    return record, text


def test_provider_quality_passes_at_research_date() -> None:
    errors, details = check_provider_quality(as_of=AS_OF)
    assert errors == []
    assert any("seven-token-shingle similarity" in detail for detail in details)


def test_provider_inventory_preserves_eight_stable_id_slug_pairs() -> None:
    actual = {record["id"]: record["slug"] for record in providers()}
    assert actual == EXPECTED_PROVIDERS


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("status", "experimental"),
        ("last_verified", "2026-02-30"),
        ("stale_after_days", 0),
        ("stale_risk", "urgent"),
        ("unexpected_field", "not allowed"),
    ],
)
def test_provider_schema_rejects_invalid_contract(field: str, value: object) -> None:
    schema = load("schemas/provider.schema.json")
    record = copy.deepcopy(providers()[0])
    record[field] = value
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
    assert errors


def test_non_official_source_cannot_be_official_provider_source() -> None:
    records = copy.deepcopy(providers())
    records[0]["official_source_ids"][0] = "repo-llamaindex"
    errors = provider_record_errors(records, resources(), as_of=AS_OF)
    assert any("non-official source used as official" in error for error in errors)


def test_official_source_cannot_be_supporting_provider_source() -> None:
    records = copy.deepcopy(providers())
    records[0]["supporting_source_ids"] = ["official-openai-evals"]
    errors = provider_record_errors(records, resources(), as_of=AS_OF)
    assert any("official source misclassified as supporting" in error for error in errors)


def test_unresolved_and_overlapping_sources_are_rejected() -> None:
    records = copy.deepcopy(providers())
    records[0]["official_source_ids"].append("official-does-not-exist")
    records[0]["supporting_source_ids"] = ["official-does-not-exist"]
    errors = provider_record_errors(records, resources(), as_of=AS_OF)
    assert any("unresolved official provider source" in error for error in errors)
    assert any("unresolved supporting provider source" in error for error in errors)
    assert any("duplicate official/supporting source" in error for error in errors)


@pytest.mark.parametrize("field", ["acceptance_criteria", "remaining_gaps"])
def test_reused_provider_semantic_blocks_are_rejected(field: str) -> None:
    records = copy.deepcopy(providers())
    records[1][field] = records[0][field]
    errors = provider_record_errors(records, resources(), as_of=AS_OF)
    assert any(f"duplicate provider {field}" in error for error in errors)


def test_future_provider_and_fast_stale_dates_are_rejected() -> None:
    records = copy.deepcopy(providers())
    records[0]["last_verified"] = "2026-08-01"
    records[0]["fast_stale_areas"][0]["last_verified"] = "2026-08-01"
    errors = provider_record_errors(records, resources(), as_of=AS_OF)
    assert any("future provider verification date" in error for error in errors)
    assert any("future fast-stale verification date" in error for error in errors)


def test_fast_stale_claim_must_use_declared_source() -> None:
    records = copy.deepcopy(providers())
    records[0]["fast_stale_areas"][0]["source_id"] = "official-gemini-prompting"
    errors = provider_record_errors(records, resources(), as_of=AS_OF)
    assert any("fast-stale source is not declared" in error for error in errors)


def test_provider_source_lesson_taxonomy_is_exact() -> None:
    source_records = resources()
    for source_id, expected_lessons in PROVIDER_SOURCE_LESSONS.items():
        assert set(source_records[source_id]["related_lessons"]) == expected_lessons


@pytest.mark.parametrize(
    ("old", "new", "expected"),
    [
        ("Catalog ID: `provider-openai`", "Catalog ID: `provider-wrong`", "catalog ID"),
        ("## Scope", "## Applicability", "missing heading `Scope`"),
        ("\n2026-07-31\n", "\n2026-07-30\n", "last-verified mismatch"),
        (
            "https://developers.openai.com/api/docs/guides/evals",
            "https://example.invalid/evals",
            "canonical source URL is missing",
        ),
        (
            "Supported Structured Outputs schema surface",
            "Schema feature surface",
            "fast-stale claim lacks area",
        ),
    ],
)
def test_provider_document_sync_errors_are_detected(
    old: str,
    new: str,
    expected: str,
) -> None:
    record, text = openai_fixture()
    assert old in text
    errors = provider_document_errors(record, resources(), text.replace(old, new, 1))
    assert any(expected in error for error in errors)


def test_generic_provider_filler_is_rejected() -> None:
    record, text = openai_fixture()
    errors = provider_document_errors(
        record,
        resources(),
        text + "\nProvider guidance goes here.\n",
    )
    assert any("generic provider filler" in error for error in errors)


def test_duplicate_examples_and_long_provider_copy_are_rejected() -> None:
    records = providers()[:2]
    _, text = openai_fixture()
    documents = {records[0]["slug"]: text, records[1]["slug"]: text}
    errors, _ = provider_cross_document_errors(records, documents)
    assert any("duplicate provider example" in error for error in errors)
    assert any("high-similarity provider guides" in error for error in errors)


def test_missing_provider_page_is_rejected(tmp_path: Path) -> None:
    (tmp_path / "catalog").mkdir()
    (tmp_path / "docs").mkdir()
    for name in ("provider-guides.json", "official-resources.json", "repositories.json"):
        shutil.copy2(ROOT / "catalog" / name, tmp_path / "catalog" / name)
    shutil.copytree(ROOT / "docs" / "providers", tmp_path / "docs" / "providers")
    (tmp_path / "docs" / "providers" / "openai.md").unlink()
    errors, _ = check_provider_quality(tmp_path, as_of=AS_OF)
    assert "missing provider page: docs/providers/openai.md" in errors
