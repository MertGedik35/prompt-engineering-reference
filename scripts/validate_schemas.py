from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

MAPPINGS = {
    "patterns": ("catalog/patterns.json", "schemas/pattern.schema.json"),
    "templates": ("catalog/templates.json", "schemas/template.schema.json"),
    "contracts": ("catalog/prompt_contracts.json", "schemas/contract.schema.json"),
    "doctor": ("catalog/prompt_doctor.json", "schemas/doctor.schema.json"),
    "evaluations": ("catalog/evaluations.json", "schemas/evaluation.schema.json"),
    "providers": ("catalog/provider-guides.json", "schemas/provider.schema.json"),
    "official_resources": ("catalog/official-resources.json", "schemas/resource.schema.json"),
    "repositories": ("catalog/repositories.json", "schemas/resource.schema.json"),
    "courses": ("catalog/courses.json", "schemas/resource.schema.json"),
    "credentials": ("catalog/credentials.json", "schemas/resource.schema.json"),
    "videos": ("catalog/videos.json", "schemas/resource.schema.json"),
    "papers": ("catalog/papers.json", "schemas/resource.schema.json"),
    "books": ("catalog/books.json", "schemas/resource.schema.json"),
    "tools": ("catalog/tools.json", "schemas/resource.schema.json"),
    "communities": ("catalog/communities.json", "schemas/resource.schema.json"),
}


def load_json(path: str) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def validate_all() -> tuple[dict[str, int], list[str]]:
    counts: dict[str, int] = {}
    errors: list[str] = []
    for name, (catalog_path, schema_path) in MAPPINGS.items():
        records = load_json(catalog_path)
        schema = load_json(schema_path)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        if not isinstance(records, list):
            errors.append(f"{catalog_path}: expected a list")
            continue
        counts[name] = len(records)
        for index, record in enumerate(records):
            for error in sorted(validator.iter_errors(record), key=lambda item: item.path):
                location = ".".join(str(part) for part in error.path) or "<record>"
                errors.append(f"{catalog_path}[{index}].{location}: {error.message}")
    return counts, errors


def main() -> int:
    counts, errors = validate_all()
    if errors:
        print("JSON Schema validation failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("JSON Schema validation passed")
    for name, count in sorted(counts.items()):
        print(f"{name}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
