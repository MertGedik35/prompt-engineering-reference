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
