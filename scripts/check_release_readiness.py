"""Publication-readiness checks for Version 2 documentation surfaces."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_SLUG = "MertGedik35/prompt-engineering-reference"
GITHUB_BLOB_PREFIX = f"https://github.com/{REPO_SLUG}/blob/"
EDIT_URI_REQUIRED = "edit_uri: edit/main/docs/"

PUBLICATION_PATHS = (
    ROOT / "README.md",
    ROOT / "docs" / "index.md",
    ROOT / "mkdocs.yml",
)
LEARN_DIR = ROOT / "docs" / "learn"
MKDOCS = ROOT / "mkdocs.yml"
PAGES_WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"

# Historical maintainer records may mention temporary development branches or PR #10.
HISTORICAL_ALLOWLIST = frozenset(
    {
        "docs/project/v2-development-record.md",
        "docs/project/v2-semantic-content-audit.md",
        "docs/project/v1-content-audit.md",
        "docs/project/v1-to-v2-migration.md",
        "docs/project/v2-architecture.md",
        "docs/project/v2-release-gates.md",
        "docs/project/privacy-audit.md",
    }
)

FORBIDDEN_BRANCH_MARKERS = (
    "feat/v2-learning-reference",
    "fix/v2-release-transition",
    "codex/",
    "refs/pull/",
)
TEMPORARY_BRANCH_REFS = (
    "feat/v2-learning-reference",
    "fix/v2-release-transition",
)
TEMPORARY_CONTENT_OPS = frozenset({"blob", "tree", "edit", "blame", "raw"})
MARKDOWN_REF_LINK_RE = re.compile(r"(?m)^\[([^\]]+)\]:\s*(\S+)")
ANGLE_AUTOLINK_RE = re.compile(r"<(https?://[^>\s]+)>")
HTML_ATTR_URL_RE = re.compile(
    r"""(?i)\b(?:href|src)\s*=\s*(?P<quote>['"])(?P<url>https?://.*?)(?P=quote)"""
)
RAW_URL_RE = re.compile(r"https?://[^\s)\]>'\"<>]+")
TRAILING_PUNCT_RE = re.compile(r"[).,;\"']+$")

PUBLIC_DRAFT_PATTERNS = (
    re.compile(r"\bv2\s+is\s+a\s+draft\b", re.IGNORECASE),
    re.compile(r"\bv2\s+remains\s+a\s+draft\b", re.IGNORECASE),
    re.compile(r"\bopen\s+v2\s+draft\s+docs\b", re.IGNORECASE),
    re.compile(r"\bv1\s+stable\s*[·•]\s*v2\s+draft\b", re.IGNORECASE),
    re.compile(r"\bdraft\s+release\s+notes\b", re.IGNORECASE),
    re.compile(r"\bdraft\s+pr\s+description\b", re.IGNORECASE),
    re.compile(r"\bv2\s+draft\s+docs\s+home\b", re.IGNORECASE),
    re.compile(r"\bcompleted\s+in\s+v2\s+draft\b", re.IGNORECASE),
    re.compile(r"\|\s*v2\s+release\s*\|\s*not\s+published\b", re.IGNORECASE),
    re.compile(r"\bstatus\s+in\s+v2\s+draft\b", re.IGNORECASE),
    re.compile(r"\bnot\s+a\s+released\s+`?v2\.0\.0`?\b", re.IGNORECASE),
)

NAV_DRAFT_LABELS = (
    "Draft Release Notes",
    "Draft PR Description",
)

LEARN_MODULE_MAP = {
    "orientation.md": "00-orientation",
    "llm-foundations.md": "01-llm-foundations",
    "prompt-anatomy.md": "02-prompt-anatomy",
    "core-techniques.md": "03-core-techniques",
    "grounding-long-context.md": "04-grounding-and-long-context",
    "structured-outputs.md": "05-structured-outputs",
    "evaluation.md": "06-evaluation",
    "agents-tools.md": "07-agents-and-tools",
    "context-engineering.md": "08-context-engineering",
    "security.md": "09-security",
    "multimodal.md": "10-multimodal",
    "production-operations.md": "11-production-operations",
    "portfolio-capstone.md": "12-portfolio-and-capstone",
}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
EXPECTED_INVENTORY = {
    "modules": 13,
    "patterns": 26,
    "templates": 28,
    "providers": 8,
    "learning_resources": 8,
    "credentials": 5,
    "official_resources": 24,
    "capstones": 3,
}


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _load_json_count(relative: str) -> int:
    payload = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise TypeError(f"{relative} must contain a list")
    return len(payload)


def inventory_counts() -> dict[str, int]:
    modules = [
        path
        for path in (ROOT / "curriculum").iterdir()
        if path.is_dir() and (path / "README.md").exists()
    ]
    capstones = [
        path for path in (ROOT / "labs" / "capstones").glob("*.md") if path.name != "README.md"
    ]
    return {
        "modules": len(modules),
        "patterns": _load_json_count("catalog/patterns.json"),
        "templates": _load_json_count("catalog/templates.json"),
        "providers": _load_json_count("catalog/provider-guides.json"),
        "learning_resources": _load_json_count("catalog/courses.json"),
        "credentials": _load_json_count("catalog/credentials.json"),
        "official_resources": _load_json_count("catalog/official-resources.json"),
        "capstones": len(capstones),
    }


def check_edit_uri(text: str | None = None) -> list[str]:
    content = MKDOCS.read_text(encoding="utf-8") if text is None else text
    errors: list[str] = []
    match = re.search(r"(?m)^edit_uri:\s*(.+?)\s*$", content)
    if match is None:
        return ["mkdocs.yml missing edit_uri"]
    value = match.group(0).strip()
    if value != EDIT_URI_REQUIRED:
        errors.append(f"mkdocs.yml edit_uri must be `{EDIT_URI_REQUIRED}`; found `{value}`")
    for marker in FORBIDDEN_BRANCH_MARKERS:
        if marker in content and "edit_uri:" in content:
            edit_line = next(
                (line for line in content.splitlines() if line.startswith("edit_uri:")),
                "",
            )
            if marker in edit_line:
                errors.append(f"mkdocs.yml edit_uri references temporary branch marker: {marker}")
    return errors


def check_public_draft_markers(
    *,
    readme: str | None = None,
    docs_index: str | None = None,
    mkdocs: str | None = None,
) -> list[str]:
    readme_text = readme if readme is not None else (ROOT / "README.md").read_text(encoding="utf-8")
    docs_index_text = (
        docs_index
        if docs_index is not None
        else (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
    )
    mkdocs_text = mkdocs if mkdocs is not None else MKDOCS.read_text(encoding="utf-8")
    errors: list[str] = []
    surfaces = {
        "README.md": readme_text,
        "docs/index.md": docs_index_text,
        "mkdocs.yml": mkdocs_text,
    }
    for location, text in surfaces.items():
        for pattern in PUBLIC_DRAFT_PATTERNS:
            if pattern.search(text):
                errors.append(f"release-critical draft marker in {location}: {pattern.pattern}")
    for label in NAV_DRAFT_LABELS:
        if re.search(rf"(?m)^\s*-\s*{re.escape(label)}\s*:", mkdocs_text):
            errors.append(f"mkdocs.yml public nav retains development label: {label}")
    if "v2-draft-release-notes.md" in mkdocs_text or "v2-pr-description.md" in mkdocs_text:
        errors.append("mkdocs.yml still references retired draft project document paths")
    if "project/v2-release-notes.md" not in mkdocs_text:
        errors.append("mkdocs.yml missing V2 Release Notes navigation entry")
    if "project/v2-development-record.md" not in mkdocs_text:
        errors.append("mkdocs.yml missing V2 Development Record navigation entry")
    return errors


def normalize_extracted_url(url: str) -> str:
    return TRAILING_PUNCT_RE.sub("", url.strip())


def extract_urls(text: str) -> list[str]:
    found: list[str] = []
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://")):
            found.append(normalize_extracted_url(target))
    for _, target in MARKDOWN_REF_LINK_RE.findall(text):
        if target.startswith(("http://", "https://")):
            found.append(normalize_extracted_url(target))
    for match in ANGLE_AUTOLINK_RE.findall(text):
        found.append(normalize_extracted_url(match))
    for match in HTML_ATTR_URL_RE.finditer(text):
        found.append(normalize_extracted_url(match.group("url")))
    for match in RAW_URL_RE.findall(text):
        found.append(normalize_extracted_url(match))
    return list(dict.fromkeys(found))


def temporary_branch_ref_from_github_path(path: str) -> str | None:
    """Return temporary branch/ref when a GitHub content URL uses one."""
    from urllib.parse import unquote, urlsplit

    if path.startswith(("http://", "https://")):
        parsed = urlsplit(path)
        if parsed.hostname != "github.com":
            return None
        path = parsed.path
    parts = [part for part in path.split("/") if part]
    if len(parts) < 4:
        return None
    owner, repo, operation = parts[0], parts[1], parts[2]
    if owner != "MertGedik35" or repo != "prompt-engineering-reference":
        return None
    if operation not in TEMPORARY_CONTENT_OPS:
        return None
    remainder = unquote("/".join(parts[3:]))
    for branch in sorted(TEMPORARY_BRANCH_REFS, key=len, reverse=True):
        if remainder == branch or remainder.startswith(f"{branch}/"):
            return branch
    if remainder.startswith("codex/"):
        return "/".join(remainder.split("/")[:2])
    if remainder.startswith("refs/pull/"):
        return "/".join(remainder.split("/")[:3])
    return None


def temporary_branch_urls(text: str) -> list[str]:
    return [
        url for url in extract_urls(text) if temporary_branch_ref_from_github_path(url) is not None
    ]


def check_forbidden_branch_references(
    *,
    root: Path | None = None,
    texts: dict[str, str] | None = None,
) -> list[str]:
    """Reject temporary-branch content URLs everywhere; plain markers outside history."""
    base = ROOT if root is None else root
    errors: list[str] = []
    if texts is not None:
        items = list(texts.items())
    else:
        collected: list[tuple[str, str]] = []
        scan_roots = [base / "README.md", base / "docs", base / "mkdocs.yml"]
        for scan_root in scan_roots:
            paths = [scan_root] if scan_root.is_file() else sorted(scan_root.rglob("*"))
            for path in paths:
                if not path.is_file():
                    continue
                if path.suffix.lower() not in {".md", ".yml", ".yaml"}:
                    continue
                relative = path.relative_to(base).as_posix()
                if relative.startswith("docs/generated/"):
                    continue
                collected.append((relative, path.read_text(encoding="utf-8")))
        items = collected

    for relative, text in items:
        if relative.startswith(".github/"):
            continue
        for url in temporary_branch_urls(text):
            ref = temporary_branch_ref_from_github_path(url) or "unknown"
            errors.append(f"active temporary-branch URL in {relative}: {url} (ref={ref})")
        if relative in HISTORICAL_ALLOWLIST:
            continue
        for marker in FORBIDDEN_BRANCH_MARKERS:
            if marker in text:
                errors.append(f"publication-sensitive branch reference in {relative}: {marker}")
    return errors


def _expected_learn_links(module_id: str) -> dict[str, str]:
    base = f"{GITHUB_BLOB_PREFIX}main/"
    return {
        "readme": f"{base}curriculum/{module_id}/README.md",
        "exercise": f"{base}curriculum/{module_id}/exercise.md",
        "quiz": f"{base}curriculum/{module_id}/quiz.md",
        "references": f"{base}curriculum/{module_id}/references.md",
        "checklist": f"{base}curriculum/{module_id}/checklist.md",
        "solution": f"{base}labs/solutions/{module_id}.md",
    }


def check_learning_stubs(learn_dir: Path | None = None) -> list[str]:
    directory = LEARN_DIR if learn_dir is None else learn_dir
    errors: list[str] = []
    for filename, module_id in LEARN_MODULE_MAP.items():
        path = directory / filename
        if not path.exists():
            errors.append(f"missing learning stub: docs/learn/{filename}")
            continue
        text = path.read_text(encoding="utf-8")
        if "feat/v2-learning-reference" in text or "fix/v2-release-transition" in text:
            errors.append(f"learning stub pins temporary branch URL: docs/learn/{filename}")
        links = LINK_RE.findall(text)
        expected = _expected_learn_links(module_id)
        for role, url in expected.items():
            if url not in links:
                errors.append(f"docs/learn/{filename} missing {role} link to {url}")
            else:
                relative = url.split("/blob/main/", 1)[-1]
                if not (ROOT / relative).exists():
                    errors.append(
                        f"docs/learn/{filename} {role} target missing on disk: {relative}"
                    )
        for link in links:
            if not link.startswith(GITHUB_BLOB_PREFIX):
                continue
            remainder = link[len(GITHUB_BLOB_PREFIX) :]
            branch, _, relative = remainder.partition("/")
            if branch != "main":
                errors.append(
                    f"docs/learn/{filename} GitHub link uses non-main branch `{branch}`: {link}"
                )
            elif relative and not (ROOT / relative).exists():
                errors.append(f"docs/learn/{filename} GitHub link target missing: {relative}")
            # Detect wrong-module curriculum links.
            if relative.startswith("curriculum/") and module_id not in relative:
                errors.append(
                    f"docs/learn/{filename} curriculum link targets wrong module: {relative}"
                )
    return errors


def check_pages_workflow_preserved() -> list[str]:
    text = PAGES_WORKFLOW.read_text(encoding="utf-8")
    errors: list[str] = []
    for needle in (
        "actions/configure-pages@v6",
        "actions/upload-pages-artifact@v5",
        "actions/deploy-pages@v5",
        "branches: [main]",
        "path: site",
        "contents: read",
        "pages: write",
        "id-token: write",
        "group: pages",
        "cancel-in-progress: false",
    ):
        if needle not in text:
            errors.append(f"pages workflow missing required fragment: {needle}")
    if "pull_request_target:" in text:
        errors.append("pages workflow must not use pull_request_target")
    return errors


def check_inventory_preserved() -> list[str]:
    counts = inventory_counts()
    errors: list[str] = []
    for key, expected in EXPECTED_INVENTORY.items():
        actual = counts[key]
        if actual != expected:
            errors.append(
                f"publication inventory drift for {key}: expected {expected}, found {actual}"
            )
    return errors


def check_release_readiness(root: Path | None = None) -> list[str]:
    if root is not None and root.resolve() != ROOT.resolve():
        raise ValueError("check_release_readiness currently validates the repository root only")
    errors: list[str] = []
    errors.extend(check_edit_uri())
    errors.extend(check_public_draft_markers())
    errors.extend(check_forbidden_branch_references())
    errors.extend(check_learning_stubs())
    errors.extend(check_pages_workflow_preserved())
    errors.extend(check_inventory_preserved())
    return errors


def main() -> int:
    errors = check_release_readiness()
    if errors:
        print("Release readiness check failed")
        for error in errors:
            print(f"- {error}")
        return 1
    counts = inventory_counts()
    print(
        "Release readiness check passed: "
        f"edit_uri=main, learn stubs=main, "
        f"modules={counts['modules']}, patterns={counts['patterns']}, "
        f"templates={counts['templates']}, providers={counts['providers']}, "
        f"learning_resources={counts['learning_resources']}, "
        f"credentials={counts['credentials']}, "
        f"official_resources={counts['official_resources']}, "
        f"capstones={counts['capstones']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
