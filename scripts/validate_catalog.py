from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from .validate_schemas import validate_all
except ImportError:  # pragma: no cover - used when run as a script
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
    resource_ids = {record["id"] for record in resources}
    ids = [record["id"] for record in patterns + templates + doctors + providers + resources]
    urls = [record["canonical_url"] for record in resources if "canonical_url" in record]
    for item, count in Counter(ids).items():
        if count > 1:
            errors.append(f"duplicate id: {item}")
    for item, count in Counter(urls).items():
        if count > 1:
            errors.append(f"duplicate canonical_url: {item}")
    for record in templates:
        if record.get("related_pattern") not in pattern_ids:
            errors.append(f"broken template pattern reference: {record['id']}")
    errors.extend(pattern_reference_errors(patterns, lesson_ids))
    for record in doctors:
        if record.get("relevant_pattern") not in pattern_ids:
            errors.append(f"broken doctor pattern reference: {record['id']}")
    for record in providers:
        for source_id in record.get("official_source_ids", []):
            if source_id not in resource_ids:
                errors.append(f"broken provider source reference: {record['id']} -> {source_id}")
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
