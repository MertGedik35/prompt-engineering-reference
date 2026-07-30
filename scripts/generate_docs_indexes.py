from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HEADER = "<!-- Generated file. Do not edit manually. -->\n\n"
LESSON_DOCS = {
    "00-orientation": "orientation",
    "01-llm-foundations": "llm-foundations",
    "02-prompt-anatomy": "prompt-anatomy",
    "03-core-techniques": "core-techniques",
    "04-grounding-and-long-context": "grounding-long-context",
    "05-structured-outputs": "structured-outputs",
    "06-evaluation": "evaluation",
    "07-agents-and-tools": "agents-tools",
    "08-context-engineering": "context-engineering",
    "09-security": "security",
    "10-multimodal": "multimodal",
    "11-production-operations": "production-operations",
    "12-portfolio-and-capstone": "portfolio-capstone",
}


def load(path: str) -> list[dict[str, Any]]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines) + "\n"


def bullets(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values) + "\n"


def fenced(text: str) -> str:
    return f"```text\n{text}\n```\n"


def cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def anchor(text: str) -> str:
    return re.sub(r"[^a-z0-9 -]", "", text.lower()).strip().replace(" ", "-")


def pattern_index() -> str:
    records = load("catalog/patterns.json")
    by_id = {record["id"]: record for record in records}
    rows = [[f"`{record['id']}`", record["name"], cell(record["summary"])] for record in records]
    parts = [
        HEADER,
        "# Pattern Index\n\n",
        "Generated from `catalog/patterns.json`. Each pattern defines a distinct mechanism, "
        "application boundary, copyable example, and three verification cases.\n\n",
        table(["ID", "Name", "Purpose"], rows),
    ]
    for record in records:
        parts.extend(
            [
                f"\n## {record['name']}\n\n",
                f"**ID:** `{record['id']}` · **Status:** {record['status']} · "
                f"**Last reviewed:** {record['last_reviewed']}\n\n",
                f"{record['summary']}\n\n",
                "### Mechanism\n\n",
                f"{record['mechanism']}\n\n",
                "### Use when\n\n",
                bullets(record["use_when"]),
                "\n### Avoid when\n\n",
                bullets(record["avoid_when"]),
                "\n### Good prompt\n\n",
                fenced(record["example_prompt"]),
                "\n### Bad prompt\n\n",
                fenced(record["bad_prompt"]),
                "\n### Why it works\n\n",
                f"{record['why_it_works']}\n\n",
                "### Acceptance criteria\n\n",
                bullets(record["acceptance_criteria"]),
                "\n### Failure modes\n\n",
                bullets(record["failure_modes"]),
                "\n### Verification cases\n\n",
                table(
                    ["Type", "Scenario", "Expected behavior", "Pass signal", "Failure signal"],
                    [
                        [
                            case["type"],
                            cell(case["scenario"]),
                            cell(case["expected_behavior"]),
                            cell(case["pass_signal"]),
                            cell(case["failure_signal"]),
                        ]
                        for case in record["verification"]
                    ],
                ),
                "\n### Trade-offs\n\n",
                bullets(record["trade_offs"]),
                "\n### Related material\n\n",
                "**Lessons:** "
                + ", ".join(
                    f"[`{lesson}`](../learn/{LESSON_DOCS[lesson]}.md)"
                    for lesson in record["related_lessons"]
                )
                + "\n\n",
                "**Patterns:** "
                + ", ".join(
                    f"[{by_id[pattern_id]['name']}](#{anchor(by_id[pattern_id]['name'])})"
                    for pattern_id in record["related_patterns"]
                )
                + "\n",
            ]
        )
    return "".join(parts)


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
