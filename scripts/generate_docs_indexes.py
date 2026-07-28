from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> list[dict[str, Any]]:
    data = json.loads((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise TypeError(f"{path} must contain a list")
    return [record for record in data if isinstance(record, dict)]


def render_pattern_index() -> str:
    lines = [
        "# Pattern Index",
        "",
        "Generated from `catalog/patterns.json`.",
        "",
        "| ID | Name | Summary |",
        "| --- | --- | --- |",
    ]
    for record in load("catalog/patterns.json"):
        lines.append(f"| `{record['id']}` | {record['name']} | {record['summary']} |")
    lines.append("")
    return "\n".join(lines)


def render_template_index() -> str:
    records = load("catalog/templates.json")
    categories = sorted({str(record["category"]) for record in records})
    lines = ["# Template Index", "", "Generated from `catalog/templates.json`.", ""]
    for category in categories:
        lines.extend(
            [f"## {category}", "", "| ID | Title | Related pattern |", "| --- | --- | --- |"]
        )
        for record in records:
            if record["category"] == category:
                lines.append(
                    f"| `{record['id']}` | {record['title']} | `{record['related_pattern']}` |"
                )
        lines.append("")
    return "\n".join(lines)


def render_resource_index() -> str:
    lines = [
        "# Resource Index",
        "",
        "Generated from `catalog/resources.json`.",
        "",
        "| ID | Title | Provider | URL |",
        "| --- | --- | --- | --- |",
    ]
    for record in load("catalog/resources.json"):
        lines.append(
            f"| `{record['id']}` | {record['title']} | {record['provider']} | "
            f"[source]({record['canonical_url']}) |"
        )
    lines.append("")
    return "\n".join(lines)


OUTPUTS = {
    "docs/generated/pattern-index.md": render_pattern_index,
    "docs/generated/template-index.md": render_template_index,
    "docs/generated/resource-index.md": render_resource_index,
}


def write_outputs(check: bool) -> list[str]:
    drift: list[str] = []
    for relative_path, renderer in OUTPUTS.items():
        path = ROOT / relative_path
        content = renderer()
        if check:
            existing = path.read_text(encoding="utf-8") if path.exists() else ""
            if existing != content:
                drift.append(relative_path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    return drift


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drift = write_outputs(check=args.check)
    if drift:
        print("Generated index drift detected")
        for item in drift:
            print(f"- {item}")
        return 1
    if args.check:
        print("Generated indexes are current")
    else:
        print("Generated indexes updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
