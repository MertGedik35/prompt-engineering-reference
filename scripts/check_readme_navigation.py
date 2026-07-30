from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
DOCS_URL = "https://mertgedik35.github.io/prompt-engineering-reference/"

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
WINDOWS_PATH_RE = re.compile(r"(?i)(?:[a-z]:\\|file://|\\\\[a-z0-9_.-]+\\)")

CURRICULUM_TARGETS = {
    f"curriculum/{number:02d}-{slug}/README.md"
    for number, slug in enumerate(
        (
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
    )
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
    "catalog/prompt_contracts.json",
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
    "docs/reference/index.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
}
REQUIRED_TARGETS = (
    CURRICULUM_TARGETS | PROVIDER_TARGETS | REFERENCE_TARGETS | PRACTICE_TARGETS | PROJECT_TARGETS
)

AUDIENCE_NAMES = (
    "Complete beginner",
    "Prompt practitioner",
    "Developer",
    "Coding-agent user",
    "Security reviewer",
    "Researcher",
    "Career learner",
    "Contributor",
)


def normalized_target(target: str) -> str:
    return unquote(target.split("#", 1)[0].strip())


def readme_links(text: str) -> list[tuple[str, str]]:
    return [(label, normalized_target(target)) for label, target in LINK_RE.findall(text)]


def check_readme(text: str, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    links = readme_links(text)
    targets = {target for _, target in links}

    for required in sorted(REQUIRED_TARGETS):
        if required not in targets:
            errors.append(f"README missing required destination: {required}")

    docs_cta_count = sum(target == DOCS_URL for _, target in links)
    if "LEARNING_PATH.md" not in targets:
        errors.append("README missing Start Learning CTA")
    if "docs/reference/index.md" not in targets:
        errors.append("README missing Browse the Reference CTA")
    if docs_cta_count == 0:
        errors.append(f"README missing documentation-site link: {DOCS_URL}")

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

    choose_path = re.search(
        r"^## Choose your path\s*$\n(.*?)(?=^##\s+|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not choose_path:
        errors.append("README missing Choose your path section")
    else:
        rows = choose_path.group(1)
        for audience in AUDIENCE_NAMES:
            match = re.search(
                rf"^\|\s*{re.escape(audience)}\s*\|\s*(.*?)\s*\|$",
                rows,
                flags=re.MULTILINE | re.IGNORECASE,
            )
            if not match:
                errors.append(f"README missing audience route: {audience}")
            else:
                destinations = [item.strip() for item in match.group(1).split("→")]
                if any(not re.fullmatch(r"\[[^\]]+\]\([^)]+\)", item) for item in destinations):
                    errors.append(
                        f"README audience route contains an unlinked destination: {audience}"
                    )

    return errors


def main() -> int:
    errors = check_readme(README.read_text(encoding="utf-8"))
    if errors:
        print("README navigation check failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "README navigation check passed: "
        f"{len(CURRICULUM_TARGETS)} modules, {len(PROVIDER_TARGETS)} providers, "
        f"{len(REQUIRED_TARGETS)} required destinations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
