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
        "application boundary, copyable example, and three canonical verification cases.\n\n",
        "All patterns can be expressed through the repository Prompt Contract fields: Objective, "
        "Context, Inputs, Instructions, Constraints, Tools and Sources, Output Contract, and "
        "Evaluation. That universal contract is documented once here instead of repeated as "
        "record metadata.\n\n",
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
                        for case in record["verification_cases"]
                    ],
                ),
                "\n### Trade-offs\n\n",
                bullets(record["trade_offs"]),
                "\n### Related material\n\n",
                "**Primary lesson:** "
                + f"[`{record['primary_lesson']}`]"
                + f"(../learn/{LESSON_DOCS[record['primary_lesson']]}.md)\n\n",
                (
                    "**Additional lessons:** "
                    + ", ".join(
                        f"[`{lesson}`](../learn/{LESSON_DOCS[lesson]}.md)"
                        for lesson in record["related_lessons"]
                    )
                    + "\n\n"
                    if record["related_lessons"]
                    else ""
                ),
                "**Related patterns:** "
                + ", ".join(
                    f"[{by_id[pattern_id]['name']}](#{anchor(by_id[pattern_id]['name'])})"
                    for pattern_id in record["related_patterns"]
                )
                + "\n",
            ]
        )
    return "".join(parts)


def template_index() -> str:
    pattern_records = load("catalog/patterns.json")
    patterns_by_id = {record["id"]: record for record in pattern_records}
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in load("catalog/templates.json"):
        groups[str(record["category"])].append(record)
    parts = [
        HEADER,
        "# Template Index\n\n",
        "Generated from `catalog/templates.json`. Each entry provides a minimal prompt for quick "
        "use and a production prompt with task-specific boundaries, output rules, test cases, "
        "and review evidence.\n",
    ]
    for category, records in sorted(groups.items()):
        parts.append(f"\n## {category}\n\n")
        rows = [
            [
                f"[`{record['id']}`](#{anchor(record['title'])})",
                record["title"],
                f"`{record['primary_lesson']}`",
                f"`{record['related_pattern']}`",
            ]
            for record in records
        ]
        parts.append(table(["ID", "Title", "Primary lesson", "Primary pattern"], rows))

    for record in load("catalog/templates.json"):
        variables = [
            [
                f"`{variable['name']}`",
                variable["type"],
                "yes" if variable["required"] else "no",
                cell(variable["description"]),
                cell(variable["example"]),
                cell("; ".join(variable["constraints"])),
            ]
            for variable in record["variables"]
        ]
        output_sections = [
            [
                section["name"],
                "yes" if section["required"] else "no",
                cell(section["description"]),
            ]
            for section in record["output_contract"]["sections"]
        ]
        failure_rows = [
            [
                failure["name"],
                cell(failure["trigger"]),
                cell(failure["observable_symptom"]),
                cell(failure["why_it_failed"]),
            ]
            for failure in record["failure_modes"]
        ]
        test_rows = [
            [
                case["type"],
                cell(case["scenario"]),
                cell("; ".join(f"{key}={value}" for key, value in case["variable_values"].items())),
                cell(case["expected_behavior"]),
                cell("; ".join(case["pass_signals"])),
                cell("; ".join(case["failure_signals"])),
            ]
            for case in record["test_cases"]
        ]
        example = record["worked_example"]
        primary_pattern = patterns_by_id[record["related_pattern"]]
        supporting_links = ", ".join(
            f"[{patterns_by_id[pattern_id]['name']}](pattern-index.md"
            f"#{anchor(patterns_by_id[pattern_id]['name'])})"
            for pattern_id in record["supporting_patterns"]
        )
        parts.extend(
            [
                f"\n## {record['title']}\n\n",
                f"**ID:** `{record['id']}` · **Category:** {record['category']} · "
                f"**Status:** {record['status']} · **Last reviewed:** "
                f"{record['last_reviewed']}\n\n",
                f"{record['summary']}\n\n",
                "### Use when\n\n",
                bullets(record["use_when"]),
                "\n### Avoid when\n\n",
                bullets(record["avoid_when"]),
                "\n### Variables\n\n",
                table(
                    ["Name", "Type", "Required", "Description", "Example", "Constraints"],
                    variables,
                ),
                "\n### Minimal prompt\n\n",
                fenced(record["minimal_prompt"]),
                "\n### Production prompt\n\n",
                fenced(record["prompt"]),
                "\n### Expected output contract\n\n",
                f"**Format:** {record['output_contract']['format']}\n\n",
                table(["Section", "Required", "Description"], output_sections),
                f"\n**Unknown value:** {record['output_contract']['unknown_value']}\n\n",
                f"**Failure response:** {record['output_contract']['failure_response']}\n\n",
                "### Acceptance criteria\n\n",
                bullets(record["acceptance_criteria"]),
                "\n### Failure modes\n\n",
                table(["Failure", "Trigger", "Observable symptom", "Why it failed"], failure_rows),
                "\n### Test cases\n\n",
                table(
                    [
                        "Type",
                        "Scenario",
                        "Variable values",
                        "Expected behavior",
                        "Pass signals",
                        "Failure signals",
                    ],
                    test_rows,
                ),
                "\n### Worked example\n\n",
                "**Variable values:**\n\n",
                bullets([f"`{key}`: {value}" for key, value in example["variable_values"].items()]),
                "\n**Representative input:**\n\n",
                f"{example['input']}\n\n",
                "**Expected output excerpt:**\n\n",
                fenced(example["output_excerpt"]),
                f"\n**Acceptance evidence:** {example['acceptance_evidence']}\n\n",
                f"**Known limitation:** {example['limitation']}\n\n",
                "### Adaptation notes\n\n",
                bullets(record["adaptation_notes"]),
                "\n### Privacy and security\n\n",
                f"{record['privacy_and_security']}\n\n",
                (
                    f"### Provider considerations\n\n{record['provider_considerations']}\n\n"
                    if record.get("provider_considerations")
                    else ""
                ),
                "### Limitations\n\n",
                bullets(record["limitations"]),
                "\n### Related material\n\n",
                "**Primary lesson:** "
                f"[`{record['primary_lesson']}`]"
                f"(../learn/{LESSON_DOCS[record['primary_lesson']]}.md)\n\n",
                (
                    "**Additional lessons:** "
                    + ", ".join(
                        f"[`{lesson}`](../learn/{LESSON_DOCS[lesson]}.md)"
                        for lesson in record["related_lessons"]
                    )
                    + "\n\n"
                    if record["related_lessons"]
                    else ""
                ),
                "**Primary pattern:** "
                f"[{primary_pattern['name']}](pattern-index.md"
                f"#{anchor(primary_pattern['name'])})\n\n",
                (
                    f"**Supporting patterns:** {supporting_links}\n"
                    if supporting_links
                    else "**Supporting patterns:** None\n"
                ),
            ]
        )
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


def course_index() -> str:
    guidance = "\n".join(
        [
            "## How to read this index",
            "",
            "- **Course vs tutorial vs lab:** structured courses and learning paths are journeys;",
            "  tutorials, guided labs, and exercise repositories are practice-first formats.",
            "- **Completion certificate vs certification:** a completion record or optional",
            "  certificate is not a formal certification exam credential.",
            "- **Access vs credential cost:** course access is separate from optional badges or",
            "  paid exams.",
            "- **Prompt relevance:** `direct` is primarily about prompting;",
            "  `substantial_component` means a major prompting unit; `adjacent`/`broad_ai`",
            "  means broader AI coverage.",
            "- **Freshness:** verification dates are catalog metadata. Confirm prices, lab",
            "  credits, and exam details on the issuer page.",
            "",
            "",
        ]
    )
    groups = [
        (
            "Direct prompt-engineering learning",
            lambda record: record.get("prompt_engineering_relevance") == "direct",
        ),
        (
            "Prompt evaluation and production learning",
            lambda record: (
                "06-evaluation" in record.get("related_lessons", [])
                or "evaluation" in str(record.get("title", "")).lower()
            ),
        ),
        (
            "Provider-specific generative-AI learning",
            lambda record: (
                record.get("prompt_engineering_relevance") in {"substantial_component", "adjacent"}
                and record.get("resource_type")
                in {"learning_path", "structured_course", "guided_lab"}
            ),
        ),
        (
            "Tutorials and guided labs",
            lambda record: (
                record.get("resource_type")
                in {"interactive_tutorial", "guided_lab", "exercise_repository", "workshop"}
            ),
        ),
        (
            "Adjacent broader AI learning",
            lambda record: record.get("prompt_engineering_relevance") in {"adjacent", "broad_ai"},
        ),
    ]
    courses = load("catalog/courses.json")
    parts = [HEADER, "# Courses\n\n", guidance]
    seen: set[str] = set()
    for heading, predicate in groups:
        rows = []
        for record in courses:
            course_id = str(record["id"])
            if course_id in seen or not predicate(record):
                continue
            seen.add(course_id)
            rows.append(
                [
                    f"[{cell(record['title'])}]({record['canonical_url']})",
                    cell(str(record["provider"])),
                    cell(str(record["resource_type"])),
                    cell(str(record["access_model"])),
                    cell(str(record["credential_outcome"])),
                    cell(str(record["level"])),
                    "yes" if record.get("hands_on") else "no",
                    cell(str(record["prompt_engineering_relevance"])),
                    cell(str(record["last_verified"])),
                ]
            )
        if not rows:
            continue
        parts.append(f"## {heading}\n\n")
        parts.append(
            table(
                [
                    "Course",
                    "Provider",
                    "Format",
                    "Access",
                    "Completion outcome",
                    "Level",
                    "Hands-on",
                    "Prompt relevance",
                    "Verified",
                ],
                rows,
            )
        )
        parts.append("\n")
    remaining = [record for record in courses if str(record["id"]) not in seen]
    if remaining:
        rows = [
            [
                f"[{cell(record['title'])}]({record['canonical_url']})",
                cell(str(record["provider"])),
                cell(str(record["resource_type"])),
                cell(str(record["access_model"])),
                cell(str(record["credential_outcome"])),
                cell(str(record["level"])),
                "yes" if record.get("hands_on") else "no",
                cell(str(record["prompt_engineering_relevance"])),
                cell(str(record["last_verified"])),
            ]
            for record in remaining
        ]
        parts.append("## Additional verified learning records\n\n")
        parts.append(
            table(
                [
                    "Course",
                    "Provider",
                    "Format",
                    "Access",
                    "Completion outcome",
                    "Level",
                    "Hands-on",
                    "Prompt relevance",
                    "Verified",
                ],
                rows,
            )
        )
        parts.append("\n")
    return "".join(parts).rstrip("\n") + "\n"


def credential_index() -> str:
    guidance = "\n".join(
        [
            "## How to read this index",
            "",
            "- **Formal certification** means an issuer exam or equivalent assessed program.",
            "- **Applied/assessed skill credentials and badges** are narrower scenario",
            "  credentials and are not interchangeable with multi-year certifications.",
            "- **Credential families** are overview pages for many individual credentials and",
            "  must not inflate individual credential counts.",
            "- **Exam cost vs course access:** paid exams are separate from free or",
            "  account-gated learning content.",
            "- Confirm fees, validity, and renewal on the issuer page before relying on",
            "  catalog summaries.",
            "",
            "",
        ]
    )
    credentials = load("catalog/credentials.json")
    group_order = [
        (
            "Formal certifications",
            lambda record: record.get("credential_type") == "formal_certification",
        ),
        (
            "Assessed skill credentials",
            lambda record: record.get("credential_type") == "assessed_skill_credential",
        ),
        (
            "Applied skill credentials",
            lambda record: (
                record.get("credential_type") == "applied_skill_credential"
                and record.get("entity_type") == "individual_credential"
            ),
        ),
        (
            "Badges",
            lambda record: record.get("credential_type") in {"skill_badge", "digital_badge"},
        ),
        (
            "Professional certificate programs",
            lambda record: record.get("credential_type") == "professional_certificate_program",
        ),
        (
            "Credential families and overview resources",
            lambda record: (
                record.get("entity_type") in {"credential_family", "overview_resource", "program"}
            ),
        ),
    ]
    parts = [HEADER, "# Credentials\n\n", guidance]
    seen: set[str] = set()
    individual = sum(
        1 for record in credentials if record.get("entity_type") == "individual_credential"
    )
    families = sum(1 for record in credentials if record.get("entity_type") == "credential_family")
    parts.append(
        f"Catalog inventory: **{len(credentials)}** total records "
        f"(**{individual}** individual credentials, **{families}** family/overview records).\n\n"
    )
    for heading, predicate in group_order:
        rows = []
        for record in credentials:
            credential_id = str(record["id"])
            if credential_id in seen or not predicate(record):
                continue
            seen.add(credential_id)
            rows.append(
                [
                    f"[{cell(record['title'])}]({record['canonical_url']})",
                    cell(str(record["issuer"])),
                    cell(str(record["credential_type"])),
                    cell(str(record["assessment_type"])),
                    cell(str(record["access_or_exam_model"])),
                    cell(str(record["prompt_engineering_relevance"])),
                    cell(str(record["validity_or_renewal"])),
                    cell(str(record["last_verified"])),
                ]
            )
        if not rows:
            continue
        parts.append(f"## {heading}\n\n")
        parts.append(
            table(
                [
                    "Credential",
                    "Issuer",
                    "Type",
                    "Assessment",
                    "Access/exam model",
                    "Prompt relevance",
                    "Validity/renewal",
                    "Verified",
                ],
                rows,
            )
        )
        parts.append("\n")
    return "".join(parts).rstrip("\n") + "\n"


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
    "docs/generated/course-index.md": course_index,
    "docs/generated/credential-index.md": credential_index,
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
