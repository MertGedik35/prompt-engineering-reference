from __future__ import annotations

import json
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> list[dict[str, Any]]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def normalize(value: object) -> str:
    text = json.dumps(value, sort_keys=True) if not isinstance(value, str) else value
    text = re.sub(r"\{[^}]+\}", "{var}", text.lower())
    text = re.sub(r"template-[a-z0-9-]+|pattern-[a-z0-9-]+", "id", text)
    text = re.sub(r"[^a-z0-9{}]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def duplicate_blocks(records: list[dict[str, Any]], field: str) -> list[str]:
    counter = Counter(normalize(record.get(field, "")) for record in records)
    return [value for value, count in counter.items() if count > 1 and value]


def high_similarity(records: list[dict[str, Any]], field: str, threshold: float) -> list[str]:
    pairs: list[str] = []
    normalized = [(record["id"], normalize(record.get(field, ""))) for record in records]
    for left_index, (left_id, left_text) in enumerate(normalized):
        for right_id, right_text in normalized[left_index + 1 :]:
            if not left_text or not right_text:
                continue
            score = SequenceMatcher(None, left_text, right_text).ratio()
            if score >= threshold:
                pairs.append(f"{left_id} ~ {right_id}: {score:.3f}")
    return pairs


def run_checks() -> tuple[dict[str, int], list[str]]:
    errors: list[str] = []
    patterns = load("catalog/patterns.json")
    templates = load("catalog/templates.json")
    summary: dict[str, int] = {}
    for field in ("acceptance_criteria", "failure_modes"):
        duplicates = duplicate_blocks(templates, field)
        summary[f"template_duplicate_{field}"] = len(duplicates)
        errors.extend(f"duplicate template {field}: {item[:80]}" for item in duplicates)
    for field in ("use_when", "acceptance_criteria", "failure_modes", "verification"):
        duplicates = duplicate_blocks(patterns, field)
        summary[f"pattern_duplicate_{field}"] = len(duplicates)
        errors.extend(f"duplicate pattern {field}: {item[:80]}" for item in duplicates)
    prompt_pairs = high_similarity(templates, "prompt", 0.94)
    pattern_pairs = high_similarity(patterns, "example_prompt", 0.96)
    summary["high_similarity_templates"] = len(prompt_pairs)
    summary["high_similarity_patterns"] = len(pattern_pairs)
    errors.extend(f"high similarity template prompt: {item}" for item in prompt_pairs)
    errors.extend(f"high similarity pattern example: {item}" for item in pattern_pairs)
    short_templates = [record["id"] for record in templates if len(record.get("prompt", "")) < 250]
    summary["short_templates"] = len(short_templates)
    errors.extend(f"short template prompt: {item}" for item in short_templates)
    summary["errors"] = len(errors)
    return summary, errors


def main() -> int:
    summary, errors = run_checks()
    if errors:
        print("Content quality check failed")
        for error in errors:
            print(f"- {error}")
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 1
    print("Content quality check passed")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
