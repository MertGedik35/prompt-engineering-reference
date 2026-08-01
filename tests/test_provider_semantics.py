from __future__ import annotations

import copy
import json
import re
import shutil
from datetime import date
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from scripts.provider_quality import (
    EXPECTED_PROVIDERS,
    SECTION_NEAR_COPY_LIMIT,
    check_provider_quality,
    curriculum_lesson_ids,
    provider_cross_document_errors,
    provider_document_errors,
    provider_record_errors,
    section,
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


def documents_for(records: list[dict[str, Any]]) -> dict[str, str]:
    return {
        str(record["slug"]): (ROOT / "docs" / "providers" / f"{record['slug']}.md").read_text(
            encoding="utf-8"
        )
        for record in records
    }


def test_provider_quality_passes_at_research_date() -> None:
    errors, details = check_provider_quality(as_of=AS_OF)
    assert errors == []
    assert any("seven-token-shingle similarity" in detail for detail in details)


def test_provider_inventory_preserves_eight_stable_id_slug_pairs() -> None:
    actual = {record["id"]: record["slug"] for record in providers()}
    assert actual == EXPECTED_PROVIDERS


def test_schema_accepts_structurally_valid_ninth_provider() -> None:
    schema = load("schemas/provider.schema.json")
    record = copy.deepcopy(providers()[0])
    record["id"] = "provider-cohere"
    record["slug"] = "cohere"
    record["name"] = "Cohere"
    record["provider"] = "Cohere"
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
    assert errors == []


def test_ninth_provider_triggers_inventory_mismatch_by_default() -> None:
    records = copy.deepcopy(providers())
    ninth = copy.deepcopy(records[0])
    ninth["id"] = "provider-cohere"
    ninth["slug"] = "cohere"
    ninth["name"] = "Cohere"
    ninth["provider"] = "Cohere"
    records.append(ninth)
    errors = provider_record_errors(records, resources(), as_of=AS_OF)
    assert any("provider inventory mismatch" in error for error in errors)


def test_enforce_inventory_false_allows_extensibility_without_inventory_block() -> None:
    records = copy.deepcopy(providers())
    ninth = copy.deepcopy(records[0])
    ninth["id"] = "provider-cohere"
    ninth["slug"] = "cohere"
    ninth["name"] = "Cohere"
    ninth["provider"] = "Cohere"
    records.append(ninth)
    errors = provider_record_errors(
        records,
        resources(),
        as_of=AS_OF,
        enforce_inventory=False,
    )
    assert not any("provider inventory mismatch" in error for error in errors)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("status", "experimental"),
        ("last_verified", "2026-02-30"),
        ("stale_after_days", 0),
        ("stale_risk", "urgent"),
        ("unexpected_field", "not allowed"),
        ("id", "not-a-provider"),
        ("slug", "Bad_Slug"),
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


def test_provider_source_related_lessons_come_from_catalog() -> None:
    source_records = resources()
    lessons = curriculum_lesson_ids(ROOT)
    used_ids = {
        source_id
        for record in providers()
        for field in ("official_source_ids", "supporting_source_ids")
        for source_id in record[field]
    }
    for source_id in used_ids:
        related = source_records[source_id]["related_lessons"]
        assert isinstance(related, list)
        assert related
        assert len(related) == len(set(related))
        assert set(related) <= lessons


def test_new_valid_official_source_is_accepted_without_python_allowlist() -> None:
    records = copy.deepcopy(providers())
    catalog = resources()
    source_id = "official-openai-new-prompting-guide"
    catalog[source_id] = {
        "id": source_id,
        "official": True,
        "related_lessons": ["02-prompt-anatomy"],
        "canonical_url": "https://example.invalid/openai-new",
    }
    records[0]["official_source_ids"].append(source_id)
    errors = provider_record_errors(
        records,
        catalog,
        as_of=AS_OF,
        lesson_ids=curriculum_lesson_ids(ROOT),
    )
    assert not any("lacks approved lesson mapping" in error for error in errors)
    assert not any(source_id in error and "related_lessons" in error for error in errors)


def test_empty_related_lessons_are_rejected() -> None:
    records = copy.deepcopy(providers())
    catalog = resources()
    source_id = records[0]["official_source_ids"][0]
    catalog[source_id] = copy.deepcopy(catalog[source_id])
    catalog[source_id]["related_lessons"] = []
    errors = provider_record_errors(records, catalog, as_of=AS_OF)
    assert any("related_lessons is empty" in error for error in errors)


def test_unresolved_related_lesson_is_rejected() -> None:
    records = copy.deepcopy(providers())
    catalog = resources()
    source_id = records[0]["official_source_ids"][0]
    catalog[source_id] = copy.deepcopy(catalog[source_id])
    catalog[source_id]["related_lessons"] = ["99-does-not-exist"]
    errors = provider_record_errors(records, catalog, as_of=AS_OF)
    assert any("related_lessons unresolved" in error for error in errors)


def test_duplicate_related_lessons_are_rejected() -> None:
    records = copy.deepcopy(providers())
    catalog = resources()
    source_id = records[0]["official_source_ids"][0]
    catalog[source_id] = copy.deepcopy(catalog[source_id])
    catalog[source_id]["related_lessons"] = ["02-prompt-anatomy", "02-prompt-anatomy"]
    errors = provider_record_errors(records, catalog, as_of=AS_OF)
    assert any("related_lessons has duplicates" in error for error in errors)


def test_renamed_unresolved_source_is_clear_failure() -> None:
    records = copy.deepcopy(providers())
    records[0]["official_source_ids"][0] = "official-renamed-missing-source"
    errors = provider_record_errors(records, resources(), as_of=AS_OF)
    assert any(
        "unresolved official provider source" in error
        and "official-renamed-missing-source" in error
        for error in errors
    )


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
    assert "openai" in " ".join(errors) and "anthropic" in " ".join(errors)


def _replace_section(text: str, heading: str, replacement: str) -> str:
    pattern = rf"(^##\s+{re.escape(heading)}\s*$\n)(.*?)(?=^##\s+|\Z)"
    updated, count = re.subn(
        pattern,
        rf"\1{replacement.rstrip()}\n\n",
        text,
        count=1,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert count == 1
    return updated


def test_minimal_example_exact_copy_is_rejected() -> None:
    records = providers()[:2]
    documents = documents_for(records)
    openai_minimal = section(documents["openai"], "Minimal provider-aware example")
    documents["anthropic"] = _replace_section(
        documents["anthropic"],
        "Minimal provider-aware example",
        openai_minimal,
    )
    errors, _ = provider_cross_document_errors(records, documents)
    assert any(
        "duplicate provider example" in error and "openai" in error and "anthropic" in error
        for error in errors
    )


def test_minimal_example_provider_name_swap_is_rejected() -> None:
    records = providers()[:2]
    documents = documents_for(records)
    openai_minimal = section(documents["openai"], "Minimal provider-aware example")
    swapped = re.sub(r"(?i)openai", "Anthropic", openai_minimal)
    documents["anthropic"] = _replace_section(
        documents["anthropic"],
        "Minimal provider-aware example",
        swapped,
    )
    errors, _ = provider_cross_document_errors(records, documents)
    assert any(
        "duplicate provider example" in error and "openai" in error and "anthropic" in error
        for error in errors
    )


def test_production_example_exact_copy_is_rejected() -> None:
    records = providers()[:2]
    documents = documents_for(records)
    openai_production = section(documents["openai"], "Production-oriented example")
    documents["anthropic"] = _replace_section(
        documents["anthropic"],
        "Production-oriented example",
        openai_production,
    )
    errors, _ = provider_cross_document_errors(records, documents)
    assert any(
        "duplicate provider example" in error and "Production-oriented example" in error
        for error in errors
    )


def test_production_example_identity_swap_is_rejected() -> None:
    records = providers()[:2]
    documents = documents_for(records)
    openai_production = section(documents["openai"], "Production-oriented example")
    swapped = re.sub(r"(?i)openai", "Anthropic", openai_production)
    swapped = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", "2026-06-15", swapped)
    swapped = re.sub(r"https://\S+", "https://example.invalid/source", swapped)
    documents["anthropic"] = _replace_section(
        documents["anthropic"],
        "Production-oriented example",
        swapped,
    )
    errors, _ = provider_cross_document_errors(records, documents)
    assert any(
        "duplicate provider example" in error and "openai" in error and "anthropic" in error
        for error in errors
    )


def test_provider_name_swapped_long_paragraph_is_rejected() -> None:
    records = providers()[:2]
    documents = documents_for(records)
    donor = None
    for paragraph in re.split(r"\n\s*\n", documents["openai"]):
        if len(re.findall(r"\b[\w'-]+\b", paragraph)) >= 66:
            donor = paragraph
            break
    assert donor is not None
    swapped = re.sub(r"(?i)openai", "Anthropic", donor)
    documents["anthropic"] = documents["anthropic"] + "\n\n" + swapped + "\n"
    errors, _ = provider_cross_document_errors(records, documents)
    assert any(
        "reused long provider paragraph" in error and "openai" in error and "anthropic" in error
        for error in errors
    )


def test_near_paraphrase_example_one_is_rejected() -> None:
    records = providers()[:2]
    documents = documents_for(records)
    base = (
        "For production workflows the provider must validate structured outputs against a "
        "declared schema before tools are called. Reject incomplete fields, require provenance "
        "for retrieved evidence, and keep evaluation fixtures frozen when model routing "
        "changes. Do not invent citations and do not skip human approval for irreversible "
        "actions. Record failure modes for schema drift, tool timeout, and unsupported "
        "modalities so operators can detect regressions quickly during rollout."
    )
    near = (
        "In production flows this vendor should verify structured responses against an "
        "explicit structure ahead of invoking functions. Discard incomplete fields, demand "
        "provenance for retrieved evidence, and retain evaluation fixtures frozen when model "
        "routing changes. Never fabricate citations and never bypass human approval for "
        "irreversible actions. Capture failure modes for structure drift, function timeout, "
        "and unsupported modalities so operators can notice regressions quickly during rollout."
    )
    documents["openai"] = _replace_section(documents["openai"], "Production-oriented example", base)
    documents["anthropic"] = _replace_section(
        documents["anthropic"],
        "Production-oriented example",
        near,
    )
    errors, _ = provider_cross_document_errors(records, documents)
    assert any(
        "near-copy provider prose" in error
        and "openai" in error
        and "anthropic" in error
        and f">= {SECTION_NEAR_COPY_LIMIT:.2f}" in error
        for error in errors
    )


def test_near_paraphrase_example_two_is_rejected() -> None:
    records = providers()[:2]
    documents = documents_for(records)
    base = (
        "Keep provider-specific tool contracts narrow, freeze acceptance fixtures before "
        "shipping, and require evidence tags on every retrieved claim. Route multimodal "
        "inputs through an observation-first checklist, refuse speculative citations, and "
        "escalate irreversible actions to a human reviewer. Capture timeouts, schema "
        "mismatches, and unsupported file types as explicit failure modes so production "
        "operators can compare releases safely."
    )
    near = (
        "Maintain vendor-specific function contracts narrow, lock acceptance fixtures before "
        "shipping, and demand evidence tags on every retrieved claim. Send multimodal inputs "
        "through an observation-first checklist, reject speculative citations, and escalate "
        "irreversible actions to a human reviewer. Log timeouts, structure mismatches, and "
        "unsupported file types as explicit failure modes so production operators can compare "
        "releases safely."
    )
    documents["openai"] = _replace_section(documents["openai"], "Production-oriented example", base)
    documents["anthropic"] = _replace_section(
        documents["anthropic"],
        "Production-oriented example",
        near,
    )
    errors, _ = provider_cross_document_errors(records, documents)
    assert any("near-copy provider prose" in error for error in errors)


def test_shared_terminology_negative_control_is_not_flagged() -> None:
    records = providers()[:2]
    documents = documents_for(records)
    openai_note = (
        "Shared vocabulary such as schema validation, tool calling, and provenance tags may "
        "appear in many guides, but this OpenAI note describes overnight batch scoring only."
    )
    anthropic_note = (
        "Shared vocabulary such as schema validation, tool calling, and provenance tags may "
        "appear in many guides, but this Anthropic note describes interactive refund approvals."
    )
    documents["openai"] = documents["openai"] + "\n\n" + openai_note + "\n"
    documents["anthropic"] = documents["anthropic"] + "\n\n" + anthropic_note + "\n"
    errors, _ = provider_cross_document_errors(records, documents)
    assert not any("near-copy provider prose" in error for error in errors)
    assert not any("reused long provider paragraph" in error for error in errors)


def test_different_workflow_production_negative_control_is_not_flagged() -> None:
    records = providers()[:2]
    documents = documents_for(records)
    openai_flow = (
        "Batch overnight evaluation jobs freeze prompts, score grounded answers against a held-out "
        "set, and publish only aggregate regression deltas to the release board without invoking "
        "customer-facing tools during the measurement window."
    )
    anthropic_flow = (
        "Interactive support agents stream tool results into a short ticket summary, ask the user "
        "to confirm irreversible refunds, and store evidence links beside each cited policy clause "
        "before closing the conversation."
    )
    documents["openai"] = _replace_section(
        documents["openai"],
        "Production-oriented example",
        openai_flow,
    )
    documents["anthropic"] = _replace_section(
        documents["anthropic"],
        "Production-oriented example",
        anthropic_flow,
    )
    errors, _ = provider_cross_document_errors(records, documents)
    assert not any("duplicate provider example" in error for error in errors)
    assert not any("near-copy provider prose" in error for error in errors)


def test_missing_provider_page_is_rejected(tmp_path: Path) -> None:
    (tmp_path / "catalog").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "curriculum" / "02-prompt-anatomy").mkdir(parents=True)
    (tmp_path / "curriculum" / "02-prompt-anatomy" / "README.md").write_text(
        "# lesson\n",
        encoding="utf-8",
    )
    for name in ("provider-guides.json", "official-resources.json", "repositories.json"):
        shutil.copy2(ROOT / "catalog" / name, tmp_path / "catalog" / name)
    shutil.copytree(ROOT / "docs" / "providers", tmp_path / "docs" / "providers")
    # Copy remaining curriculum inventory so lesson resolution still works for other sources.
    for path in (ROOT / "curriculum").glob("*/README.md"):
        target = tmp_path / "curriculum" / path.parent.name
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target / "README.md")
    (tmp_path / "docs" / "providers" / "openai.md").unlink()
    errors, _ = check_provider_quality(tmp_path, as_of=AS_OF)
    assert "missing provider page: docs/providers/openai.md" in errors
