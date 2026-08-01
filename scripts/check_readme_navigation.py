from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
DOCS_URL = "https://mertgedik35.github.io/prompt-engineering-reference/"

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
WINDOWS_PATH_RE = re.compile(r"(?i)(?:[a-z]:\\|file://|\\\\[a-z0-9_.-]+\\)")
WORD_RE = re.compile(r"[A-Za-z0-9']+")

CURRICULUM_MODULE_SLUGS = (
    "orientation",
    "llm-foundations",
    "prompt-anatomy",
    "core-techniques",
    "grounding-and-long-context",
    "structured-outputs",
    "evaluation",
    "agents-and-tools",
    "context-engineering",
    "security",
    "multimodal",
    "production-operations",
    "portfolio-and-capstone",
)
CURRICULUM_TARGETS = {
    f"curriculum/{number:02d}-{slug}/README.md"
    for number, slug in enumerate(CURRICULUM_MODULE_SLUGS)
}
# docs/learn navigation filenames mapped from curriculum module ids
LEARN_HUB_MODULE_TARGETS = {
    "00-orientation": "orientation.md",
    "01-llm-foundations": "llm-foundations.md",
    "02-prompt-anatomy": "prompt-anatomy.md",
    "03-core-techniques": "core-techniques.md",
    "04-grounding-and-long-context": "grounding-long-context.md",
    "05-structured-outputs": "structured-outputs.md",
    "06-evaluation": "evaluation.md",
    "07-agents-and-tools": "agents-tools.md",
    "08-context-engineering": "context-engineering.md",
    "09-security": "security.md",
    "10-multimodal": "multimodal.md",
    "11-production-operations": "production-operations.md",
    "12-portfolio-and-capstone": "portfolio-capstone.md",
}
PROVIDER_TARGETS = {
    f"docs/providers/{provider}.md"
    for provider in (
        "openai",
        "anthropic",
        "google",
        "microsoft",
        "aws",
        "meta",
        "mistral",
        "open-models",
    )
}
REFERENCE_TARGETS = {
    "docs/generated/pattern-index.md",
    "docs/generated/template-index.md",
    "docs/generated/prompt-doctor-index.md",
    "docs/generated/glossary-index.md",
    "reference/checklists/security.md",
    "reference/decision-guides/provider-selection.md",
    "docs/generated/official-resource-index.md",
    "resources/official-prompts/README.md",
    "docs/generated/course-index.md",
    "docs/generated/credential-index.md",
    "docs/generated/video-index.md",
    "docs/generated/paper-index.md",
    "docs/generated/book-index.md",
    "docs/generated/repository-index.md",
    "docs/generated/tool-index.md",
    "docs/generated/community-index.md",
}
PRACTICE_TARGETS = {
    "labs/exercises/README.md",
    "labs/quizzes/README.md",
    "labs/solutions/",
    "labs/evaluations/README.md",
    "labs/capstones/research-assistant.md",
    "labs/capstones/structured-extraction.md",
    "labs/capstones/coding-agent-pack.md",
}
PROJECT_TARGETS = {
    "LEARNING_PATH.md",
    "docs/index.md",
    "docs/reference/index.md",
    "docs/resources/index.md",
    "docs/labs/index.md",
    "docs/learn/index.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
}
REQUIRED_TARGETS = (
    CURRICULUM_TARGETS | PROVIDER_TARGETS | REFERENCE_TARGETS | PRACTICE_TARGETS | PROJECT_TARGETS
)

INTENT_ROWS = (
    "Learn from zero",
    "Improve a prompt",
    "Find a technique",
    "Copy a prompt",
    "Compare providers",
    "Evaluate prompts",
    "Learn from courses",
    "Read research",
    "Build a portfolio",
)

PRIMARY_CTA_ROLES = {
    "Start Learning": "LEARNING_PATH.md",
    "Browse Prompt Reference": "docs/reference/index.md",
    "Open V2 Draft Docs": "docs/index.md",
}
PRIMARY_CTA_TARGETS = set(PRIMARY_CTA_ROLES.values())

RAW_CATALOG_CTA_TARGETS = {
    "catalog/prompt_contracts.json",
    "catalog/security_controls.json",
    "catalog/patterns.json",
    "catalog/templates.json",
    "catalog/courses.json",
    "catalog/credentials.json",
}

PRACTICE_SEQUENCE = (
    "Lesson",
    "Exercise",
    "Quiz",
    "Explained solution",
    "Checklist",
    "Capstone",
)
PRACTICE_SEQUENCE_RE = re.compile(
    r"Lesson\s*(?:→|->)\s*Exercise\s*(?:→|->)\s*Quiz\s*(?:→|->)\s*"
    r"Explained solution\s*(?:→|->)\s*Checklist\s*(?:→|->)\s*Capstone",
    flags=re.IGNORECASE,
)

HUB_PAGES = {
    "docs/index.md": (
        "Choose a path",
        "What is inside",
        "Learning roadmap",
        "Status",
        "learn/index.md",
        "reference/index.md",
    ),
    "docs/learn/index.md": (
        "Phase 1",
        "Phase 2",
        "Phase 3",
        "Phase 4",
        "Lesson → Exercise → Quiz → Explained solution → Checklist → Capstone",
    ),
    "docs/reference/index.md": (
        "Prompt patterns",
        "Prompt templates",
        "Prompt Doctor",
        "Provider guides",
        "Security checklist",
    ),
    "docs/resources/index.md": (
        "Official documentation",
        "Courses",
        "Credentials",
        "Papers",
        "Books",
        "Videos",
        "Tools",
        "Communities",
        "Reference repositories",
    ),
    "docs/labs/index.md": (
        "Lesson → Exercise → Quiz → Explained solution → Checklist → Capstone",
        "Exercises",
        "Quizzes",
        "Explained solutions",
        "Capstones",
        "Evaluations",
        "Datasets",
    ),
}

HUB_MIN_WORDS = 80
MAX_LEARNING_PATH_LINKS = 4
PLACEHOLDER_MAX_WORDS = 40
PUBLISHED_LABEL_RE = re.compile(
    r"\bV1\b|Published documentation|published release|published site|current `main`",
    flags=re.IGNORECASE,
)


def normalized_target(target: str) -> str:
    return unquote(target.split("#", 1)[0].strip())


def readme_links(text: str) -> list[tuple[str, str]]:
    return [(label, normalized_target(target)) for label, target in LINK_RE.findall(text)]


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def load_json_count(root: Path, relative: str) -> int:
    payload = json.loads((root / relative).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise TypeError(f"{relative} must contain a list")
    return len(payload)


def inventory_counts(root: Path = ROOT) -> dict[str, int]:
    modules = sorted(
        path.name
        for path in (root / "curriculum").iterdir()
        if path.is_dir() and (path / "README.md").exists()
    )
    exercises = sorted((root / "curriculum").glob("*/exercise.md"))
    quizzes = sorted((root / "curriculum").glob("*/quiz.md"))
    solutions = sorted((root / "labs" / "solutions").glob("*.md"))
    capstones = sorted(
        path.name for path in (root / "labs" / "capstones").glob("*.md") if path.name != "README.md"
    )
    return {
        "modules": len(modules),
        "patterns": load_json_count(root, "catalog/patterns.json"),
        "templates": load_json_count(root, "catalog/templates.json"),
        "providers": load_json_count(root, "catalog/provider-guides.json"),
        "capstones": len(capstones),
        "exercises": len(exercises),
        "quizzes": len(quizzes),
        "solutions": len(solutions),
        "courses": load_json_count(root, "catalog/courses.json"),
        "credentials": load_json_count(root, "catalog/credentials.json"),
        "official_resources": load_json_count(root, "catalog/official-resources.json"),
    }


def section(text: str, heading: str) -> str | None:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    return None if match is None else match.group(1)


def check_inventory_mentions(text: str, counts: dict[str, int]) -> list[str]:
    errors: list[str] = []
    expected = {
        "Curriculum modules": counts["modules"],
        "Prompt patterns": counts["patterns"],
        "Prompt templates": counts["templates"],
        "Provider guides": counts["providers"],
        "Capstone projects": counts["capstones"],
        "Official-resource catalog records": counts["official_resources"],
    }
    for label, value in expected.items():
        if not re.search(rf"{re.escape(label)}\s*\|\s*{value}\b", text):
            errors.append(f"README inventory mismatch for {label}: expected {value}")
    coverage = section(text, "Current coverage and status") or ""
    coverage_expected = {
        "Curriculum": counts["modules"],
        "Prompt patterns": counts["patterns"],
        "Prompt templates": counts["templates"],
        "Provider guides": counts["providers"],
        "Courses": counts["courses"],
        "Credentials": counts["credentials"],
    }
    for label, value in coverage_expected.items():
        if not re.search(rf"\|\s*{re.escape(label)}\s*\|\s*{value}\b", coverage):
            errors.append(f"README coverage table mismatch for {label}: expected {value}")
    return errors


def check_practice_sequence(text: str, *, location: str) -> list[str]:
    if PRACTICE_SEQUENCE_RE.search(text):
        return []
    return [f"{location} missing complete practice sequence"]


def check_learn_hub_modules(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    path = root / "docs" / "learn" / "index.md"
    if not path.exists():
        return ["missing hub page: docs/learn/index.md"]
    text = path.read_text(encoding="utf-8")
    links = readme_links(text)
    targets = [target for _, target in links]
    expected = list(LEARN_HUB_MODULE_TARGETS.values())
    for module_id, target in LEARN_HUB_MODULE_TARGETS.items():
        count = targets.count(target)
        if count == 0:
            errors.append(f"Learn hub missing module {module_id} -> {target}")
        elif count > 1:
            errors.append(f"Learn hub duplicates module {module_id} -> {target} ({count})")
    extras = sorted(
        {
            target
            for target in targets
            if "/" not in target and target.endswith(".md") and target not in expected
        }
    )
    for target in extras:
        errors.append(f"Learn hub has unexpected module target: {target}")
    return errors


def check_hub_pages(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative, markers in HUB_PAGES.items():
        path = root / relative
        if not path.exists():
            errors.append(f"missing hub page: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        words = word_count(text)
        if words < HUB_MIN_WORDS:
            errors.append(f"hub page too short: {relative} words={words} < {HUB_MIN_WORDS}")
        if words <= PLACEHOLDER_MAX_WORDS:
            errors.append(f"hub page still placeholder-sized: {relative}")
        lowered = text.lower()
        for marker in markers:
            if marker.lower() not in lowered:
                errors.append(f"hub page {relative} missing required marker: {marker}")
        if "feat/v2-learning-reference" in text:
            errors.append(f"hub page pins draft branch URL: {relative}")
        for _, target in readme_links(text):
            if target in RAW_CATALOG_CTA_TARGETS:
                errors.append(f"hub page {relative} uses raw catalog as primary CTA: {target}")
        if relative in {"docs/learn/index.md", "docs/labs/index.md"}:
            errors.extend(check_practice_sequence(text, location=relative))
    home = (root / "docs" / "index.md").read_text(encoding="utf-8")
    if "learn/index.md" not in home or "reference/index.md" not in home:
        errors.append("docs home missing Learning or Reference path")
    errors.extend(check_learn_hub_modules(root))
    return errors


def check_primary_cta_roles(text: str, links: list[tuple[str, str]]) -> list[str]:
    errors: list[str] = []
    targets = {target for _, target in links}
    for label, expected in PRIMARY_CTA_ROLES.items():
        matching = [target for link_label, target in links if link_label.strip() == label]
        if not matching:
            errors.append(f"README missing primary CTA label: {label}")
            continue
        if expected not in matching:
            errors.append(
                f"README primary CTA '{label}' must target {expected}; got {sorted(set(matching))}"
            )
        if label == "Browse Prompt Reference" and "docs/resources/index.md" in matching:
            errors.append(
                "README Browse Prompt Reference must not target Courses & Resources hub "
                "(docs/resources/index.md)"
            )
        if label == "Open V2 Draft Docs" and DOCS_URL in matching:
            errors.append(
                "README Open V2 Draft Docs must not target the published Pages site; "
                "use docs/index.md for the V2 draft"
            )

    for cta in PRIMARY_CTA_TARGETS:
        if cta not in targets:
            errors.append(f"README missing primary CTA target: {cta}")

    learning_path_links = sum(target == "LEARNING_PATH.md" for _, target in links)
    if learning_path_links > MAX_LEARNING_PATH_LINKS:
        errors.append(
            "README repeats Start Learning / LEARNING_PATH CTA too often: "
            f"{learning_path_links} > {MAX_LEARNING_PATH_LINKS}"
        )

    if DOCS_URL in targets:
        for match in re.finditer(re.escape(DOCS_URL), text):
            window = text[max(0, match.start() - 120) : match.end() + 160]
            if not PUBLISHED_LABEL_RE.search(window):
                errors.append(
                    "README published Pages URL lacks nearby V1/published labeling: " + DOCS_URL
                )
                break
    return errors


def check_readme(text: str, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    links = readme_links(text)
    targets = {target for _, target in links}
    counts = inventory_counts(root)

    for required in sorted(REQUIRED_TARGETS):
        if required not in targets:
            errors.append(f"README missing required destination: {required}")

    errors.extend(check_primary_cta_roles(text, links))

    for target in targets & RAW_CATALOG_CTA_TARGETS:
        errors.append(f"README uses raw catalog as visitor CTA: {target}")

    if "docs/reference/index.md" in targets:
        hub = (root / "docs" / "reference" / "index.md").read_text(encoding="utf-8")
        if word_count(hub) <= PLACEHOLDER_MAX_WORDS:
            errors.append(
                "Browse/Reference CTA points at placeholder-sized docs/reference/index.md"
            )

    for _, target in links:
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        candidate = (root / target).resolve()
        try:
            candidate.relative_to(root.resolve())
        except ValueError:
            errors.append(f"README link escapes repository: {target}")
            continue
        if not candidate.exists():
            errors.append(f"README internal link does not resolve: {target}")

    if WINDOWS_PATH_RE.search(text):
        errors.append("README contains a local absolute filesystem path")
    if re.search(r"(?:curriculum|docs|labs|reference)/<[^>]+>", text):
        errors.append("README contains a user-facing placeholder path")

    choose = section(text, "Choose what you need")
    if choose is None:
        errors.append("README missing Choose what you need section")
    else:
        for intent in INTENT_ROWS:
            match = re.search(
                rf"^\|\s*{re.escape(intent)}\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$",
                choose,
                flags=re.MULTILINE | re.IGNORECASE,
            )
            if not match:
                errors.append(f"README missing intent route: {intent}")
            elif not re.search(r"\[[^\]]+\]\([^)]+\)", match.group(1)):
                errors.append(f"README intent route missing link: {intent}")

    if section(text, "What is inside") is None:
        errors.append("README missing What is inside section")
    if section(text, "Learning roadmap") is None:
        errors.append("README missing Learning roadmap section")
    if section(text, "Current coverage and status") is None:
        errors.append("README missing Current coverage and status section")
    errors.extend(check_practice_sequence(text, location="README"))

    errors.extend(check_inventory_mentions(text, counts))
    errors.extend(check_hub_pages(root))
    return errors


def main() -> int:
    errors = check_readme(README.read_text(encoding="utf-8"))
    if errors:
        print("README navigation check failed")
        for error in errors:
            print(f"- {error}")
        return 1
    counts = inventory_counts()
    print(
        "README navigation check passed: "
        f"{counts['modules']} modules, {counts['providers']} providers, "
        f"{counts['patterns']} patterns, {counts['templates']} templates, "
        f"{counts['official_resources']} official-resource records, "
        f"{len(REQUIRED_TARGETS)} required destinations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
