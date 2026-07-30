from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from scripts.check_content_quality import QualityReport, check_pattern_quality
from scripts.generate_docs_indexes import pattern_index
from scripts.validate_catalog import pattern_reference_errors

ROOT = Path(__file__).resolve().parents[1]
PATTERNS: list[dict[str, Any]] = json.loads(
    (ROOT / "catalog/patterns.json").read_text(encoding="utf-8")
)


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
    records[0]["verification"] = [
        case for case in records[0]["verification"] if case["type"] != case_type
    ]
    assert any(f"missing unique {case_type} case" in error for error in report_for(records).errors)


@pytest.mark.parametrize("signal", ["pass_signal", "failure_signal"])
def test_verification_requires_both_signals(signal: str) -> None:
    records = pair()
    records[0]["verification"][0][signal] = ""
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
    records[1]["verification"][0]["scenario"] = records[0]["verification"][0]["scenario"]
    assert any(
        "duplicate pattern verification scenario" in error for error in report_for(records).errors
    )


def test_invalid_related_lesson_reference_is_rejected() -> None:
    records = pair()
    records[0]["related_lessons"] = ["99-missing-lesson"]
    errors = pattern_reference_errors(records, {"00-orientation"})
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
