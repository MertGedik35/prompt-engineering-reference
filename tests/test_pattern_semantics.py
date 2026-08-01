from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from scripts.check_content_quality import QualityReport, check_pattern_quality
from scripts.generate_docs_indexes import pattern_index
from scripts.validate_catalog import (
    PATTERN_ALLOWED_RELATED_LESSONS,
    PATTERN_PRIMARY_LESSONS,
    pattern_reference_errors,
)

ROOT = Path(__file__).resolve().parents[1]
PATTERNS: list[dict[str, Any]] = json.loads(
    (ROOT / "catalog/patterns.json").read_text(encoding="utf-8")
)
LESSON_IDS = {path.parent.name for path in (ROOT / "curriculum").glob("*/README.md")}


def report_for(records: list[dict[str, Any]]) -> QualityReport:
    report = QualityReport()
    check_pattern_quality(records, report)
    return report


def pair() -> list[dict[str, Any]]:
    return copy.deepcopy(PATTERNS[:2])


@pytest.mark.parametrize(
    ("field_name", "message"),
    [
        ("mechanism", "field=mechanism"),
        ("use_when", "field=use_when"),
        ("avoid_when", "field=avoid_when"),
        ("acceptance_criteria", "field=acceptance_criteria"),
        ("failure_modes", "field=failure_modes"),
    ],
)
def test_duplicate_semantic_blocks_are_rejected(field_name: str, message: str) -> None:
    records = pair()
    records[1][field_name] = copy.deepcopy(records[0][field_name])
    assert any(message in error for error in report_for(records).errors)


def test_title_substitution_mechanisms_are_rejected() -> None:
    records = pair()
    records[0].update(id="pattern-alpha", slug="alpha", name="Alpha", title="Alpha")
    records[1].update(id="pattern-beta", slug="beta", name="Beta", title="Beta")
    records[0]["mechanism"] = (
        "Alpha pattern routes input through a signed authority boundary before external "
        "execution and records proof for later deterministic validation."
    )
    records[1]["mechanism"] = (
        "Beta pattern routes input through a signed authority boundary before external "
        "execution and records proof for later deterministic validation."
    )
    assert any("field=mechanism" in error for error in report_for(records).errors)


def test_known_artificial_bad_prompt_is_rejected() -> None:
    records = pair()
    records[0]["bad_prompt"] = "Handle this with objective contract and make it good."
    assert any("artificial pattern bad prompt" in error for error in report_for(records).errors)


@pytest.mark.parametrize("case_type", ["normal", "edge", "failure"])
def test_missing_verification_case_type_is_rejected(case_type: str) -> None:
    records = pair()
    records[0]["verification_cases"] = [
        case for case in records[0]["verification_cases"] if case["type"] != case_type
    ]
    assert any(f"missing unique {case_type} case" in error for error in report_for(records).errors)


@pytest.mark.parametrize("signal", ["pass_signal", "failure_signal"])
def test_verification_requires_both_signals(signal: str) -> None:
    records = pair()
    records[0]["verification_cases"][0][signal] = ""
    assert any(f"missing {signal}" in error for error in report_for(records).errors)


def test_circular_mechanism_is_rejected() -> None:
    records = pair()
    records[0]["mechanism"] = (
        "Use the Objective Contract pattern to apply this pattern mechanism and implement "
        "the Objective Contract pattern by applying the pattern."
    )
    assert any("circular pattern mechanism" in error for error in report_for(records).errors)


def test_fewer_than_three_acceptance_criteria_are_rejected() -> None:
    records = pair()
    records[0]["acceptance_criteria"] = records[0]["acceptance_criteria"][:2]
    assert any("acceptance criteria < 3" in error for error in report_for(records).errors)


def test_fewer_than_three_failure_modes_are_rejected() -> None:
    records = pair()
    records[0]["failure_modes"] = records[0]["failure_modes"][:2]
    assert any("failure modes < 3" in error for error in report_for(records).errors)


def test_duplicate_verification_scenarios_are_rejected() -> None:
    records = pair()
    records[1]["verification_cases"][0]["scenario"] = records[0]["verification_cases"][0][
        "scenario"
    ]
    assert any(
        "duplicate pattern verification scenario" in error for error in report_for(records).errors
    )


def test_invalid_related_lesson_reference_is_rejected() -> None:
    records = pair()
    records[0]["related_lessons"] = ["99-missing-lesson"]
    errors = pattern_reference_errors(records, LESSON_IDS)
    assert any("broken pattern lesson reference" in error for error in errors)


def test_high_similarity_pair_reports_score_and_threshold() -> None:
    records = pair()
    shared = (
        "The prompt assigns every supplied claim to a declared authority tier before "
        "synthesis and preserves conflicts so lower-ranked repetition cannot override evidence."
    )
    records[0]["mechanism"] = shared + " Alpha."
    records[1]["mechanism"] = shared + " Beta."
    error = next(error for error in report_for(records).errors if "field=mechanism" in error)
    assert "score=" in error
    assert "threshold=0.82" in error


def test_legitimately_adjacent_patterns_pass_with_shared_vocabulary() -> None:
    ids = {"pattern-context-boundary", "pattern-source-hierarchy", "pattern-evidence-table"}
    records = [copy.deepcopy(record) for record in PATTERNS if record["id"] in ids]
    assert report_for(records).errors == []


def test_valid_twenty_six_record_catalog_passes_pattern_checks() -> None:
    assert len(PATTERNS) == 26
    assert report_for(copy.deepcopy(PATTERNS)).errors == []


def test_generated_pattern_documentation_is_current() -> None:
    assert (ROOT / "docs/generated/pattern-index.md").read_text(encoding="utf-8") == pattern_index()


def test_all_stable_patterns_use_the_approved_primary_lesson() -> None:
    assert set(PATTERN_PRIMARY_LESSONS) == {record["id"] for record in PATTERNS}
    assert len(PATTERN_PRIMARY_LESSONS) == 26
    for record in PATTERNS:
        assert record["primary_lesson"] == PATTERN_PRIMARY_LESSONS[record["id"]]
        assert set(record["related_lessons"]).issubset(
            PATTERN_ALLOWED_RELATED_LESSONS[record["id"]]
        )


@pytest.mark.parametrize(
    ("pattern_id", "wrong_lesson"),
    [
        ("pattern-output-schema", "01-llm-foundations"),
        ("pattern-tool-selection", "04-grounding-and-long-context"),
        ("pattern-defensive-injection-check", "06-evaluation"),
        ("pattern-multimodal-observation-first", "07-agents-and-tools"),
        ("pattern-objective-contract", "00-orientation"),
    ],
)
def test_existing_but_semantically_wrong_primary_lesson_is_rejected(
    pattern_id: str, wrong_lesson: str
) -> None:
    records = copy.deepcopy(PATTERNS)
    record = next(item for item in records if item["id"] == pattern_id)
    record["primary_lesson"] = wrong_lesson
    assert any(
        "wrong pattern primary lesson" in error
        for error in pattern_reference_errors(records, LESSON_IDS)
    )


def test_missing_primary_lesson_is_rejected() -> None:
    records = copy.deepcopy(PATTERNS)
    record = records[0]
    record.pop("primary_lesson")
    assert any(
        "wrong pattern primary lesson" in error
        for error in pattern_reference_errors(records, LESSON_IDS)
    )


def test_missing_approved_mapping_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delitem(PATTERN_PRIMARY_LESSONS, PATTERNS[0]["id"])
    assert any(
        "pattern lesson taxonomy coverage mismatch" in error
        for error in pattern_reference_errors(copy.deepcopy(PATTERNS), LESSON_IDS)
    )


def test_valid_multi_lesson_mapping_passes() -> None:
    records = copy.deepcopy(PATTERNS)
    context_boundary = next(
        record for record in records if record["id"] == "pattern-context-boundary"
    )
    assert context_boundary["primary_lesson"] == "08-context-engineering"
    assert context_boundary["related_lessons"] == ["09-security"]
    assert pattern_reference_errors(records, LESSON_IDS) == []


def test_structured_verification_is_the_only_catalog_source() -> None:
    schema = json.loads((ROOT / "schemas/pattern.schema.json").read_text(encoding="utf-8"))
    assert "verification_cases" in schema["required"]
    assert "verification" not in schema["required"]
    assert "verification" not in schema["properties"]
    for record in PATTERNS:
        assert "verification_cases" in record
        assert "verification" not in record


def test_generator_reads_canonical_verification_cases(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records = copy.deepcopy(PATTERNS)
    record = records[0]
    record["verification"] = ["LEGACY PROJECTION MUST NOT RENDER"]
    monkeypatch.setattr(
        "scripts.generate_docs_indexes.load",
        lambda path: records if path == "catalog/patterns.json" else [],
    )
    rendered = pattern_index()
    assert record["verification_cases"][0]["scenario"] in rendered
    assert "LEGACY PROJECTION MUST NOT RENDER" not in rendered


def test_pattern_consumers_do_not_read_legacy_verification() -> None:
    import inspect

    from scripts import generate_docs_indexes as generator

    # Pattern indexes must keep reading verification_cases, never the removed
    # legacy pattern field named verification. Credential verification objects are
    # intentionally out of scope for this guard.
    pattern_index_source = inspect.getsource(generator.pattern_index)
    assert 'record["verification_cases"]' in pattern_index_source
    assert 'record["verification"]' not in pattern_index_source
    assert 'record.get("verification"' not in pattern_index_source

    quality = (ROOT / "scripts/check_content_quality.py").read_text(encoding="utf-8")
    assert 'record.get("verification_cases"' in quality
    assert 'record.get("verification"' not in quality
    assert 'record["verification"]' not in quality

    catalog = (ROOT / "scripts/validate_catalog.py").read_text(encoding="utf-8")
    assert 'record["verification"]' not in catalog
    assert 'record.get("verification"' not in catalog


def test_name_is_the_single_pattern_display_label() -> None:
    schema = json.loads((ROOT / "schemas/pattern.schema.json").read_text(encoding="utf-8"))
    assert "name" in schema["required"]
    assert "title" not in schema["properties"]
    assert all("name" in record and "title" not in record for record in PATTERNS)


def test_prompt_contract_fields_are_catalog_level_policy() -> None:
    rendered = pattern_index()
    assert all("prompt_contract_fields" not in record for record in PATTERNS)
    assert "Objective, Context, Inputs, Instructions, Constraints" in rendered


def test_title_substituted_prompt_contract_metadata_is_rejected() -> None:
    records = pair()
    records[0]["prompt_contract_fields"] = [
        f"{records[0]['name']} objective",
        f"{records[0]['name']} context",
        f"{records[0]['name']} output",
        f"{records[0]['name']} evaluation",
    ]
    assert any(
        f"deprecated pattern field present: {records[0]['id']}.prompt_contract_fields" in error
        for error in report_for(records).errors
    )
