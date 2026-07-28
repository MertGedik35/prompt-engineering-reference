from __future__ import annotations

import argparse
import json
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HEADER = "<!-- Generated file. Do not edit manually. -->\n\n"


def load(path: str) -> list[dict[str, Any]]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines) + "\n"


def pattern_index() -> str:
    rows = [[f"`{r['id']}`", r["name"], r["summary"]] for r in load("catalog/patterns.json")]
    return HEADER + "# Pattern Index\n\n" + table(["ID", "Name", "Mechanism"], rows)


def template_index() -> str:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in load("catalog/templates.json"):
        groups[str(record["category"])].append(record)
    parts = [HEADER + "# Template Index\n"]
    for category, records in sorted(groups.items()):
        parts.append(f"\n## {category}\n\n")
        rows = [[f"`{r['id']}`", r["title"], f"`{r['related_pattern']}`"] for r in records]
        parts.append(table(["ID", "Title", "Pattern"], rows))
    return "".join(parts)


def doctor_index() -> str:
    rows = [
        [f"`{r['id']}`", r["symptom"], f"`{r['relevant_pattern']}`"]
        for r in load("catalog/prompt_doctor.json")
    ]
    return HEADER + "# Prompt Doctor Index\n\n" + table(["ID", "Symptom", "Pattern"], rows)


def glossary_index() -> str:
    rows = [[r["term"], r["definition"]] for r in load("catalog/glossary.json")]
    return HEADER + "# Glossary\n\n" + table(["Term", "Definition"], rows)


def resource_index(path: str, title: str) -> str:
    rows = []
    for record in load(path):
        url = record.get("canonical_url", "")
        pricing = record.get("pricing_type", "")
        credential = record.get("credential_type", "")
        stale = record.get("stale_risk", "")
        rows.append(
            [f"`{record['id']}`", record["title"], pricing, credential, stale, f"[source]({url})"]
        )
    return (
        HEADER
        + f"# {title}\n\n"
        + table(["ID", "Title", "Pricing", "Credential", "Stale risk", "URL"], rows)
    )


OUTPUTS: dict[str, Callable[[], str]] = {
    "docs/generated/pattern-index.md": pattern_index,
    "docs/generated/template-index.md": template_index,
    "docs/generated/prompt-doctor-index.md": doctor_index,
    "docs/generated/glossary-index.md": glossary_index,
    "docs/generated/official-resource-index.md": lambda: resource_index(
        "catalog/official-resources.json", "Official Resources"
    ),
    "docs/generated/repository-index.md": lambda: resource_index(
        "catalog/repositories.json", "Repositories"
    ),
    "docs/generated/course-index.md": lambda: resource_index("catalog/courses.json", "Courses"),
    "docs/generated/credential-index.md": lambda: resource_index(
        "catalog/credentials.json", "Credentials"
    ),
    "docs/generated/video-index.md": lambda: resource_index("catalog/videos.json", "Videos"),
    "docs/generated/paper-index.md": lambda: resource_index("catalog/papers.json", "Papers"),
    "docs/generated/book-index.md": lambda: resource_index("catalog/books.json", "Books"),
    "docs/generated/tool-index.md": lambda: resource_index("catalog/tools.json", "Tools"),
    "docs/generated/community-index.md": lambda: resource_index(
        "catalog/communities.json", "Communities"
    ),
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
    print("Generated indexes are current" if args.check else "Generated indexes updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
