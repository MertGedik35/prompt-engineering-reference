from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from .check_freshness import utc_today
    from .provider_quality import provider_record_errors
    from .template_taxonomy import (
        TEMPLATE_ALLOWED_RELATED_LESSONS,
        TEMPLATE_ALLOWED_SUPPORTING_PATTERNS,
        TEMPLATE_PRIMARY_LESSONS,
        TEMPLATE_PRIMARY_PATTERNS,
    )
    from .validate_schemas import validate_all
except ImportError:  # pragma: no cover - used when run as a script
    from check_freshness import utc_today  # type: ignore[import-not-found,no-redef]
    from provider_quality import (  # type: ignore[import-not-found,no-redef]
        provider_record_errors,
    )
    from template_taxonomy import (  # type: ignore[import-not-found,no-redef]
        TEMPLATE_ALLOWED_RELATED_LESSONS,
        TEMPLATE_ALLOWED_SUPPORTING_PATTERNS,
        TEMPLATE_PRIMARY_LESSONS,
        TEMPLATE_PRIMARY_PATTERNS,
    )
    from validate_schemas import validate_all  # type: ignore[import-not-found,no-redef]

ROOT = Path(__file__).resolve().parents[1]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BANNED_MARKERS = [
    "TO" + "DO",
    "FIX" + "ME",
    "T" + "BD",
    "coming " + "soon",
    "lorem " + "ipsum",
    "place" + "holder",
]
RESOURCE_FILES = [
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
PATTERN_PRIMARY_LESSONS = {
    "pattern-objective-contract": "02-prompt-anatomy",
    "pattern-context-boundary": "08-context-engineering",
    "pattern-source-hierarchy": "04-grounding-and-long-context",
    "pattern-evidence-table": "04-grounding-and-long-context",
    "pattern-output-schema": "05-structured-outputs",
    "pattern-few-shot-boundary-cases": "03-core-techniques",
    "pattern-counterexample-guard": "03-core-techniques",
    "pattern-clarify-or-proceed": "03-core-techniques",
    "pattern-abstention-rule": "03-core-techniques",
    "pattern-long-context-map-reduce": "04-grounding-and-long-context",
    "pattern-context-compression": "08-context-engineering",
    "pattern-tool-selection": "07-agents-and-tools",
    "pattern-tool-provenance": "07-agents-and-tools",
    "pattern-human-approval": "07-agents-and-tools",
    "pattern-retry-with-diagnosis": "07-agents-and-tools",
    "pattern-rubric-first-evaluation": "06-evaluation",
    "pattern-regression-case": "06-evaluation",
    "pattern-agent-state-ledger": "07-agents-and-tools",
    "pattern-delegation-contract": "07-agents-and-tools",
    "pattern-defensive-injection-check": "09-security",
    "pattern-multimodal-observation-first": "10-multimodal",
    "pattern-accessible-visual-brief": "10-multimodal",
    "pattern-production-change-log": "11-production-operations",
    "pattern-cost-latency-budget": "11-production-operations",
    "pattern-cross-model-eval": "06-evaluation",
    "pattern-secure-output-validation": "09-security",
}
PATTERN_ALLOWED_RELATED_LESSONS = {
    "pattern-objective-contract": set(),
    "pattern-context-boundary": {"09-security"},
    "pattern-source-hierarchy": set(),
    "pattern-evidence-table": {"06-evaluation"},
    "pattern-output-schema": set(),
    "pattern-few-shot-boundary-cases": set(),
    "pattern-counterexample-guard": set(),
    "pattern-clarify-or-proceed": {"02-prompt-anatomy"},
    "pattern-abstention-rule": {"04-grounding-and-long-context"},
    "pattern-long-context-map-reduce": set(),
    "pattern-context-compression": set(),
    "pattern-tool-selection": set(),
    "pattern-tool-provenance": {"08-context-engineering"},
    "pattern-human-approval": {"09-security"},
    "pattern-retry-with-diagnosis": {"11-production-operations"},
    "pattern-rubric-first-evaluation": set(),
    "pattern-regression-case": {"11-production-operations"},
    "pattern-agent-state-ledger": {"08-context-engineering"},
    "pattern-delegation-contract": set(),
    "pattern-defensive-injection-check": {"08-context-engineering"},
    "pattern-multimodal-observation-first": set(),
    "pattern-accessible-visual-brief": set(),
    "pattern-production-change-log": set(),
    "pattern-cost-latency-budget": set(),
    "pattern-cross-model-eval": {"11-production-operations"},
    "pattern-secure-output-validation": {"05-structured-outputs"},
}
TEMPLATE_PLACEHOLDER_RE = re.compile(r"\{\{([a-z][a-z0-9_]*)\}\}")


def pattern_reference_errors(patterns: list[dict[str, Any]], lesson_ids: set[str]) -> list[str]:
    errors: list[str] = []
    pattern_ids = {record["id"] for record in patterns}
    if pattern_ids != set(PATTERN_PRIMARY_LESSONS):
        missing = sorted(pattern_ids - set(PATTERN_PRIMARY_LESSONS))
        stale = sorted(set(PATTERN_PRIMARY_LESSONS) - pattern_ids)
        errors.append(f"pattern lesson taxonomy coverage mismatch: missing={missing} stale={stale}")
    for record in patterns:
        pattern_id = record["id"]
        if record.get("slug") != pattern_id.removeprefix("pattern-"):
            errors.append(f"pattern slug does not match id: {record['id']}")
        expected_primary = PATTERN_PRIMARY_LESSONS.get(pattern_id)
        primary_lesson = record.get("primary_lesson")
        if primary_lesson != expected_primary:
            errors.append(
                f"wrong pattern primary lesson: {pattern_id} -> {primary_lesson}; "
                f"expected {expected_primary}"
            )
        if primary_lesson not in lesson_ids:
            errors.append(f"broken pattern primary lesson: {pattern_id} -> {primary_lesson}")
        for related_pattern in record.get("related_patterns", []):
            if related_pattern not in pattern_ids:
                errors.append(
                    f"broken related pattern reference: {pattern_id} -> {related_pattern}"
                )
            elif related_pattern == pattern_id:
                errors.append(f"self-related pattern reference: {pattern_id}")
        related_lessons = set(record.get("related_lessons", []))
        unexpected_lessons = related_lessons - PATTERN_ALLOWED_RELATED_LESSONS.get(
            pattern_id, set()
        )
        if unexpected_lessons:
            errors.append(
                f"unapproved related lessons: {pattern_id} -> {sorted(unexpected_lessons)}"
            )
        if primary_lesson in related_lessons:
            errors.append(f"primary lesson repeated as related lesson: {pattern_id}")
        for related_lesson in record.get("related_lessons", []):
            if related_lesson not in lesson_ids:
                errors.append(f"broken pattern lesson reference: {pattern_id} -> {related_lesson}")
    return errors


def template_reference_errors(
    templates: list[dict[str, Any]],
    pattern_ids: set[str],
    lesson_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    template_ids = {str(record.get("id", "")) for record in templates}
    approved_ids = set(TEMPLATE_PRIMARY_PATTERNS)
    if len(templates) != 28:
        errors.append(f"template inventory count {len(templates)} != 28")
    if template_ids != approved_ids:
        missing = sorted(approved_ids - template_ids)
        unexpected = sorted(template_ids - approved_ids)
        errors.append(
            f"template taxonomy coverage mismatch: missing={missing} unexpected={unexpected}"
        )

    for record in templates:
        template_id = str(record.get("id", "<missing-id>"))
        if record.get("slug") != template_id.removeprefix("template-"):
            errors.append(f"template slug does not match id: {template_id}")

        for removed_field in ("required_inputs", "expected_outputs", "production_prompt"):
            if removed_field in record:
                errors.append(f"deprecated template field present: {template_id}.{removed_field}")

        primary_pattern = record.get("related_pattern")
        expected_pattern = TEMPLATE_PRIMARY_PATTERNS.get(template_id)
        if primary_pattern != expected_pattern:
            errors.append(
                f"wrong template primary pattern: {template_id} -> {primary_pattern}; "
                f"expected {expected_pattern}"
            )
        if primary_pattern not in pattern_ids:
            errors.append(f"broken template pattern reference: {template_id} -> {primary_pattern}")

        supporting_patterns = record.get("supporting_patterns", [])
        supporting_set = (
            set(supporting_patterns) if isinstance(supporting_patterns, list) else set()
        )
        allowed_supporting = TEMPLATE_ALLOWED_SUPPORTING_PATTERNS.get(template_id, set())
        unsupported_patterns = supporting_set - allowed_supporting
        if unsupported_patterns:
            errors.append(
                f"unapproved supporting template patterns: "
                f"{template_id} -> {sorted(unsupported_patterns)}"
            )
        if primary_pattern in supporting_set:
            errors.append(f"template primary pattern repeated as supporting: {template_id}")
        for pattern_id in supporting_set:
            if pattern_id not in pattern_ids:
                errors.append(f"broken supporting template pattern: {template_id} -> {pattern_id}")

        primary_lesson = record.get("primary_lesson")
        expected_lesson = TEMPLATE_PRIMARY_LESSONS.get(template_id)
        if primary_lesson != expected_lesson:
            errors.append(
                f"wrong template primary lesson: {template_id} -> {primary_lesson}; "
                f"expected {expected_lesson}"
            )
        if primary_lesson not in lesson_ids:
            errors.append(f"broken template primary lesson: {template_id} -> {primary_lesson}")
        related_lessons = record.get("related_lessons", [])
        related_set = set(related_lessons) if isinstance(related_lessons, list) else set()
        unexpected_lessons = related_set - TEMPLATE_ALLOWED_RELATED_LESSONS.get(template_id, set())
        if unexpected_lessons:
            errors.append(
                f"unapproved template related lessons: "
                f"{template_id} -> {sorted(unexpected_lessons)}"
            )
        if primary_lesson in related_set:
            errors.append(f"template primary lesson repeated as related: {template_id}")
        for lesson_id in related_set:
            if lesson_id not in lesson_ids:
                errors.append(f"broken template lesson reference: {template_id} -> {lesson_id}")

        variables = record.get("variables", [])
        variable_names = [
            str(variable.get("name", "")) for variable in variables if isinstance(variable, dict)
        ]
        duplicates = sorted(
            name for name, count in Counter(variable_names).items() if name and count > 1
        )
        if duplicates:
            errors.append(f"duplicate template variable names: {template_id} -> {duplicates}")
        prompt_text = "\n".join(
            str(record.get(field_name, "")) for field_name in ("minimal_prompt", "prompt")
        )
        placeholders = set(TEMPLATE_PLACEHOLDER_RE.findall(prompt_text))
        declared = set(variable_names)
        undefined = sorted(placeholders - declared)
        unused = sorted(declared - placeholders)
        if undefined:
            errors.append(f"undefined template placeholders: {template_id} -> {undefined}")
        if unused:
            errors.append(f"unused template variables: {template_id} -> {unused}")

        output_contract = record.get("output_contract", {})
        sections = output_contract.get("sections", []) if isinstance(output_contract, dict) else []
        section_names = [
            str(section.get("name", "")) for section in sections if isinstance(section, dict)
        ]
        duplicate_sections = sorted(
            name for name, count in Counter(section_names).items() if name and count > 1
        )
        if duplicate_sections:
            errors.append(
                f"duplicate template output sections: {template_id} -> {duplicate_sections}"
            )
    return errors


def load(path: str) -> list[dict[str, Any]]:
    data = json.loads((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise TypeError(f"{path} must contain a list")
    return [record for record in data if isinstance(record, dict)]


def scan_banned_markers() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if path.is_dir() or any(part in {".git", ".venv", "site"} for part in path.parts):
            continue
        if path.suffix.lower() not in {".md", ".json", ".yml", ".yaml", ".toml", ".cff"}:
            continue
        text = path.read_text(encoding="utf-8").lower()
        for marker in BANNED_MARKERS:
            if marker.lower() in text:
                errors.append(f"{path.relative_to(ROOT)} contains {marker}")
    return errors


def validate() -> tuple[dict[str, int], list[str]]:
    schema_counts, errors = validate_all()
    patterns = load("catalog/patterns.json")
    templates = load("catalog/templates.json")
    doctors = load("catalog/prompt_doctor.json")
    providers = load("catalog/provider-guides.json")
    resources = [record for file in RESOURCE_FILES for record in load(file)]
    pattern_ids = {record["id"] for record in patterns}
    lesson_ids = {path.parent.name for path in (ROOT / "curriculum").glob("*/README.md")}
    resources_by_id = {record["id"]: record for record in resources}
    ids = [record["id"] for record in patterns + templates + doctors + providers + resources]
    urls = [record["canonical_url"] for record in resources if "canonical_url" in record]
    for item, count in Counter(ids).items():
        if count > 1:
            errors.append(f"duplicate id: {item}")
    for item, count in Counter(urls).items():
        if count > 1:
            errors.append(f"duplicate canonical_url: {item}")
    errors.extend(template_reference_errors(templates, pattern_ids, lesson_ids))
    errors.extend(pattern_reference_errors(patterns, lesson_ids))
    for record in doctors:
        if record.get("relevant_pattern") not in pattern_ids:
            errors.append(f"broken doctor pattern reference: {record['id']}")
    errors.extend(provider_record_errors(providers, resources_by_id, as_of=utc_today()))
    for record in resources + patterns + templates:
        for field in ("last_verified", "last_reviewed"):
            if field in record and not DATE_RE.match(str(record[field])):
                errors.append(f"invalid date {field}: {record['id']}")
    errors.extend(scan_banned_markers())
    counts = dict(schema_counts)
    counts["resource_total"] = len(resources)
    counts["duplicate_ids"] = sum(1 for count in Counter(ids).values() if count > 1)
    counts["duplicate_canonical_urls"] = sum(1 for count in Counter(urls).values() if count > 1)
    counts["errors"] = len(errors)
    return counts, errors


def main() -> int:
    counts, errors = validate()
    if errors:
        print("Catalog validation failed")
        for error in errors:
            print(f"- {error}")
        print(json.dumps(counts, indent=2, sort_keys=True))
        return 1
    print("Catalog validation passed")
    print(json.dumps(counts, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
