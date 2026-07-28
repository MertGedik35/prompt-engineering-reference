from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID_RE = re.compile(
    r"^(pattern|template|res|provider|contract|doctor|eval|context|security)-[a-z0-9-]+$"
)
TEXT_EXTENSIONS = {".md", ".json", ".yml", ".yaml", ".toml", ".cff"}
DRAFT_MARKERS = [
    "TO" + "DO",
    "FIX" + "ME",
    "T" + "BD",
    "coming " + "soon",
    "lorem " + "ipsum",
    "place" + "holder",
]

FILES = {
    "patterns": "catalog/patterns.json",
    "templates": "catalog/templates.json",
    "contracts": "catalog/prompt_contracts.json",
    "doctor": "catalog/prompt_doctor.json",
    "evaluations": "catalog/evaluations.json",
    "providers": "catalog/provider_guides.json",
    "resources": "catalog/resources.json",
    "context": "catalog/context_engineering.json",
    "security": "catalog/security_controls.json",
}

REQUIRED_FIELDS = {
    "patterns": ["id", "slug", "name", "status", "last_reviewed", "acceptance_criteria"],
    "templates": [
        "id",
        "slug",
        "title",
        "category",
        "variables",
        "required_inputs",
        "expected_outputs",
        "acceptance_criteria",
        "failure_modes",
        "version",
        "last_reviewed",
    ],
    "contracts": ["id", "name", "dimensions", "acceptance_criteria"],
    "doctor": [
        "id",
        "symptom",
        "likely_causes",
        "quick_diagnostic",
        "minimal_fix",
        "robust_fix",
        "relevant_pattern",
        "verification_method",
    ],
    "evaluations": [
        "id",
        "before_prompt",
        "after_prompt",
        "rubric_scores_before",
        "rubric_scores_after",
        "acceptance_criteria",
    ],
    "providers": ["id", "name", "last_verified", "official_source_ids"],
    "resources": ["id", "slug", "canonical_url", "status", "last_verified"],
    "context": ["id", "topic", "acceptance_criteria"],
    "security": ["id", "topic", "controls", "acceptance_criteria"],
}


def load_records(key: str) -> list[dict[str, Any]]:
    path = ROOT / FILES[key]
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise TypeError(f"{FILES[key]} must contain a list")
    return [record for record in data if isinstance(record, dict)]


def has_text(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value)
    return value is not None


def scan_markers() -> list[str]:
    matches: list[str] = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or ".venv" in path.parts or path.is_dir():
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8")
        lower_text = text.lower()
        for marker in DRAFT_MARKERS:
            if marker.lower() in lower_text:
                matches.append(f"{path.relative_to(ROOT)} contains {marker}")
    return matches


def validate() -> tuple[dict[str, int], list[str]]:
    records = {key: load_records(key) for key in FILES}
    errors: list[str] = []
    all_ids: list[str] = []
    all_slugs: list[str] = []
    urls: list[str] = []

    pattern_ids = {record["id"] for record in records["patterns"]}
    resource_ids = {record["id"] for record in records["resources"]}

    for key, values in records.items():
        for record in values:
            rid = str(record.get("id", ""))
            all_ids.append(rid)
            if not ID_RE.match(rid):
                errors.append(f"{FILES[key]} invalid id: {rid}")
            slug = record.get("slug")
            if isinstance(slug, str):
                all_slugs.append(slug)
            for field in REQUIRED_FIELDS[key]:
                if not has_text(record.get(field)):
                    errors.append(f"{FILES[key]} missing {field}: {rid}")
            for date_field in ("last_reviewed", "last_verified"):
                value = record.get(date_field)
                if isinstance(value, str) and not DATE_RE.match(value):
                    errors.append(f"{FILES[key]} invalid date {date_field}: {rid}")
            status = record.get("status")
            if status is not None and status not in {"stable", "active", "verified"}:
                errors.append(f"{FILES[key]} invalid status {status}: {rid}")
            if key == "resources":
                url = str(record.get("canonical_url", ""))
                urls.append(url)
                if not url.startswith(("https://", "http://")):
                    errors.append(f"{FILES[key]} invalid URL: {rid}")

    duplicate_ids = [item for item, count in Counter(all_ids).items() if count > 1]
    duplicate_slugs = [item for item, count in Counter(all_slugs).items() if count > 1]
    duplicate_urls = [item for item, count in Counter(urls).items() if count > 1]
    errors.extend(f"duplicate id: {item}" for item in duplicate_ids)
    errors.extend(f"duplicate slug: {item}" for item in duplicate_slugs)
    errors.extend(f"duplicate canonical_url: {item}" for item in duplicate_urls)

    for record in records["patterns"]:
        for related in record.get("related_patterns", []):
            if related not in pattern_ids:
                errors.append(f"broken pattern reference: {record['id']} -> {related}")
    for record in records["templates"]:
        related = record.get("related_pattern")
        if related not in pattern_ids:
            errors.append(f"broken template reference: {record['id']} -> {related}")
    for record in records["doctor"]:
        related = record.get("relevant_pattern")
        if related not in pattern_ids:
            errors.append(f"broken doctor reference: {record['id']} -> {related}")
    for record in records["providers"]:
        for source_id in record.get("official_source_ids", []):
            if source_id not in resource_ids:
                errors.append(f"broken provider resource reference: {record['id']} -> {source_id}")
    for record in records["evaluations"]:
        for related in record.get("related_patterns", []):
            if related not in pattern_ids:
                errors.append(f"broken evaluation reference: {record['id']} -> {related}")

    errors.extend(scan_markers())

    summary = {key: len(values) for key, values in records.items()}
    summary["duplicate_ids"] = len(duplicate_ids)
    summary["duplicate_slugs"] = len(duplicate_slugs)
    summary["duplicate_canonical_urls"] = len(duplicate_urls)
    summary["errors"] = len(errors)
    return summary, errors


def main() -> int:
    summary, errors = validate()
    if errors:
        print("Catalog validation failed")
        for error in errors:
            print(f"- {error}")
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 1
    print("Catalog validation passed")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
