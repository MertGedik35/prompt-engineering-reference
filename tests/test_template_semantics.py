from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from scripts.check_content_quality import (
    TEMPLATE_SIMILARITY_LIMITS,
    QualityReport,
    check_template_quality,
    template_similarity_pairs,
)
from scripts.generate_docs_indexes import template_index
from scripts.template_taxonomy import (
    TEMPLATE_ALLOWED_SUPPORTING_PATTERNS,
    TEMPLATE_PRIMARY_LESSONS,
    TEMPLATE_PRIMARY_PATTERNS,
)
from scripts.validate_catalog import template_reference_errors

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES: list[dict[str, Any]] = json.loads(
    (ROOT / "catalog/templates.json").read_text(encoding="utf-8")
)
PATTERN_IDS = {
    record["id"]
    for record in json.loads((ROOT / "catalog/patterns.json").read_text(encoding="utf-8"))
}
LESSON_IDS = {path.parent.name for path in (ROOT / "curriculum").glob("*/README.md")}


def report_for(records: list[dict[str, Any]]) -> QualityReport:
    report = QualityReport()
    check_template_quality(records, report)
    return report


def pair() -> list[dict[str, Any]]:
    return copy.deepcopy(TEMPLATES[:2])


def test_catalog_contains_exactly_the_stable_twenty_eight_ids() -> None:
    assert len(TEMPLATES) == 28
    assert {record["id"] for record in TEMPLATES} == set(TEMPLATE_PRIMARY_PATTERNS)


def test_duplicate_minimal_prompts_are_rejected() -> None:
    records = pair()
    records[1]["minimal_prompt"] = records[0]["minimal_prompt"]
    assert any(
        "field=minimal_prompt" in error or "duplicate template field" in error
        for error in report_for(records).errors
    )


def test_duplicate_production_prompts_are_rejected() -> None:
    records = pair()
    records[1]["prompt"] = records[0]["prompt"]
    assert any(
        "field=prompt" in error or "duplicate template field" in error
        for error in report_for(records).errors
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "output_contract",
        "acceptance_criteria",
        "failure_modes",
        "worked_example",
        "adaptation_notes",
    ],
)
def test_duplicate_semantic_template_blocks_are_rejected(field_name: str) -> None:
    records = pair()
    records[1][field_name] = copy.deepcopy(records[0][field_name])
    assert any(f"field={field_name}" in error for error in report_for(records).errors)


def test_title_substituted_production_prompts_are_rejected() -> None:
    records = pair()
    shared = (
        "Inspect the supplied evidence in declared order. Record each observation before "
        "synthesis. Preserve every conflict and missing input. Return a bounded decision with "
        "source locations. "
        "Stop when a required source is absent and request the exact missing material. "
    ) * 5
    for record in records:
        record["prompt"] = f"Prepare {record['title']}. {shared}"
    assert any("field=prompt" in error for error in report_for(records).errors)


def test_variable_substituted_prompt_skeletons_are_rejected() -> None:
    records = pair()
    shared = (
        "Read {{input_name}} and inventory the evidence. Apply the same ordered decision sequence. "
        "Return observations, analysis, unresolved gaps, and an explicit terminal response. "
        "Do not continue when the required boundary cannot be verified. "
    ) * 5
    for index, record in enumerate(records):
        name = f"input_{index}"
        record["variables"] = [
            {
                "name": name,
                "description": "The task input used to exercise the substituted skeleton.",
                "required": True,
                "type": "string",
                "example": "Synthetic input value",
                "constraints": ["Must be supplied for the regression fixture."],
            }
        ]
        record["minimal_prompt"] = shared.replace("input_name", name)
        record["prompt"] = (shared * 2).replace("input_name", name)
    assert any(
        "identity-normalized prompt skeleton" in error for error in report_for(records).errors
    )


def test_repeated_four_step_legacy_skeleton_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["prompt"] = (
        "Restate the task boundary in one sentence. "
        "Use only the supplied inputs unless a tool or source is explicitly authorized. "
        "Separate verified facts from assumptions. "
        "Apply the requested internal workflow and return an acceptance check. "
    ) * 5
    assert any(
        "legacy four-step template skeleton" in error for error in report_for(records).errors
    )


def test_internal_pattern_instruction_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["prompt"] += "\nApply the pattern-source-hierarchy pattern."
    assert any(
        "internal pattern id in copyable template prompt" in error
        for error in report_for(records).errors
    )


def test_undefined_placeholder_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["prompt"] += "\nUse {{undeclared_input}} for the final decision."
    assert any("undefined template placeholder" in error for error in report_for(records).errors)


def test_unused_declared_variable_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["variables"].append(
        {
            "name": "unused_input",
            "description": "A deliberately unused required variable for regression coverage.",
            "required": True,
            "type": "string",
            "example": "Unused fixture value",
            "constraints": ["Must be rejected when absent from both prompts."],
        }
    )
    assert any("unused declared template variable" in error for error in report_for(records).errors)


def test_duplicate_variable_name_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["variables"].append(copy.deepcopy(records[0]["variables"][0]))
    assert any("duplicate template variable names" in error for error in report_for(records).errors)


def test_missing_required_variable_description_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["variables"][0]["description"] = ""
    assert any(
        "required template variable lacks description" in error
        for error in report_for(records).errors
    )


@pytest.mark.parametrize(
    "field_name",
    ["name", "description", "required", "type", "example", "constraints"],
)
def test_missing_required_variable_metadata_is_rejected(field_name: str) -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["variables"][0].pop(field_name)
    assert any(
        "template variable missing metadata" in error for error in report_for(records).errors
    )


def test_unstructured_variable_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["variables"][0] = "question"
    assert any(
        "template variable is not structured" in error for error in report_for(records).errors
    )


def test_missing_output_failure_behavior_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["output_contract"]["failure_response"] = ""
    assert any(
        "output contract lacks failure behavior" in error for error in report_for(records).errors
    )


def test_production_prompt_that_delegates_core_workflow_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["prompt"] += "\nDesign the core workflow before completing the request."
    assert any("delegates core workflow design" in error for error in report_for(records).errors)


@pytest.mark.parametrize("case_type", ["normal", "edge", "failure"])
def test_missing_required_test_case_is_rejected(case_type: str) -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["test_cases"] = [
        case for case in records[0]["test_cases"] if case["type"] != case_type
    ]
    assert any(f"missing unique {case_type}" in error for error in report_for(records).errors)


def test_duplicate_test_scenario_is_rejected() -> None:
    records = pair()
    records[1]["test_cases"][0]["scenario"] = records[0]["test_cases"][0]["scenario"]
    assert any("duplicate template test scenario" in error for error in report_for(records).errors)


def test_missing_test_pass_signal_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["test_cases"][0]["pass_signals"] = []
    assert any("missing pass signals" in error for error in report_for(records).errors)


def test_missing_test_failure_signal_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["test_cases"][0]["failure_signals"] = []
    assert any("missing failure signals" in error for error in report_for(records).errors)


def test_fewer_than_four_acceptance_criteria_are_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["acceptance_criteria"] = records[0]["acceptance_criteria"][:3]
    assert any("acceptance criteria < 4" in error for error in report_for(records).errors)


def test_generic_acceptance_block_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["acceptance_criteria"][0] = "The output is clear professional and useful."
    assert any(
        "generic template acceptance criterion" in error for error in report_for(records).errors
    )


def test_fewer_than_three_failure_modes_are_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["failure_modes"] = records[0]["failure_modes"][:2]
    assert any("failure modes < 3" in error for error in report_for(records).errors)


def test_generic_failure_block_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["failure_modes"][0]["why_it_failed"] = (
        "The model uses outside facts without authorization."
    )
    assert any("generic template failure mode" in error for error in report_for(records).errors)


def test_missing_worked_example_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0].pop("worked_example")
    assert any("template worked example missing" in error for error in report_for(records).errors)


def test_production_prompt_identical_to_minimal_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["prompt"] = records[0]["minimal_prompt"]
    assert any(
        "production prompt repeats minimal prompt" in error for error in report_for(records).errors
    )


def test_existing_but_semantically_wrong_lesson_mapping_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["primary_lesson"] = "01-llm-foundations"
    assert any(
        "semantically wrong template lesson mapping" in error
        for error in report_for(records).errors
    )


def test_existing_but_semantically_wrong_pattern_mapping_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    records[0]["related_pattern"] = "pattern-output-schema"
    assert any(
        "semantically wrong template pattern mapping" in error
        for error in report_for(records).errors
    )


def test_missing_taxonomy_entry_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    missing_id = TEMPLATES[0]["id"]
    monkeypatch.delitem(TEMPLATE_PRIMARY_PATTERNS, missing_id)
    errors = template_reference_errors(copy.deepcopy(TEMPLATES), PATTERN_IDS, LESSON_IDS)
    assert any("template taxonomy coverage mismatch" in error for error in errors)


def test_unapproved_supporting_pattern_is_rejected() -> None:
    records = [copy.deepcopy(TEMPLATES[0])]
    unsupported = next(
        pattern_id
        for pattern_id in PATTERN_IDS
        if pattern_id
        not in TEMPLATE_ALLOWED_SUPPORTING_PATTERNS[records[0]["id"]]
        | {records[0]["related_pattern"]}
    )
    records[0]["supporting_patterns"].append(unsupported)
    assert any(
        "semantically unsupported template patterns" in error
        for error in report_for(records).errors
    )


def test_generated_template_reference_is_current() -> None:
    assert (ROOT / "docs/generated/template-index.md").read_text(
        encoding="utf-8"
    ) == template_index()


def test_legitimately_adjacent_templates_with_shared_vocabulary_pass() -> None:
    selected = {
        "template-multimodal-image-inspection",
        "template-multimodal-chart-qa",
        "template-research-source-grounded-brief",
        "template-research-competing-claims",
    }
    records = [copy.deepcopy(record) for record in TEMPLATES if record["id"] in selected]
    assert report_for(records).errors == []


@pytest.mark.parametrize("field_name", ["minimal_prompt", "prompt"])
def test_high_similarity_error_reports_score_threshold_and_reason(field_name: str) -> None:
    records = pair()
    shared = (
        "Inventory every supplied item before analysis, preserve conflicts, record missing "
        "evidence, apply the declared authority boundary, and return a measurable terminal state. "
    ) * 5
    records[0][field_name] = shared + " First."
    records[1][field_name] = shared + " Second."
    error = next(error for error in report_for(records).errors if f"field={field_name}" in error)
    assert "score=" in error
    assert f"threshold={TEMPLATE_SIMILARITY_LIMITS[field_name]:.2f}" in error
    assert "reason=identity-normalized prompt skeleton" in error


def test_legitimate_similarity_just_below_threshold_passes() -> None:
    records = pair()
    shared = (
        "inventory supplied evidence preserve conflicts record missing inputs authority boundary "
        "measurable terminal state "
    ) * 10
    records[0]["prompt"] = shared + ("alpha evidence condition outcome " * 8)
    records[1]["prompt"] = shared + ("bravo workflow response control " * 8)
    score = template_similarity_pairs(records, "prompt")[0][2]

    assert 0.80 < score < TEMPLATE_SIMILARITY_LIMITS["prompt"]
    assert not any(
        error.startswith("template similarity:") and "field=prompt" in error
        for error in report_for(records).errors
    )


def test_minimal_and_production_variants_from_one_record_pass() -> None:
    record = copy.deepcopy(TEMPLATES[0])
    assert record["minimal_prompt"] != record["prompt"]
    assert report_for([record]).errors == []


def test_complete_rewritten_catalog_passes_template_quality() -> None:
    assert report_for(copy.deepcopy(TEMPLATES)).errors == []
    assert template_reference_errors(TEMPLATES, PATTERN_IDS, LESSON_IDS) == []
    assert all(
        record["primary_lesson"] == TEMPLATE_PRIMARY_LESSONS[record["id"]] for record in TEMPLATES
    )
