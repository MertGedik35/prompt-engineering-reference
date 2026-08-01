from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
REQUIRED_PR_BASES = {"main", "feat/v2-learning-reference"}
QUALITY_COMMANDS = {
    'python -m pip install -e ".[dev,docs]"',
    "python scripts/validate_schemas.py",
    "python scripts/validate_catalog.py",
    "python scripts/check_content_quality.py",
    "python scripts/audit_privacy.py --include-git --history-warn-only",
    "python scripts/check_freshness.py",
    "python scripts/generate_docs_indexes.py --check",
    "python scripts/check_internal_links.py",
    "python scripts/check_readme_navigation.py",
    "python scripts/check_release_readiness.py",
    "python -m detect_secrets scan --all-files",
    "python -m ruff format --check .",
    "python -m ruff check .",
    "python -m mypy scripts tests",
    "python -m pytest",
    "python -m mkdocs build --strict",
    "make check",
}


def workflow_text(name: str) -> str:
    return (WORKFLOWS / name).read_text(encoding="utf-8")


def indented_block(text: str, heading: str, indent: int) -> list[str]:
    lines = text.splitlines()
    marker = f"{' ' * indent}{heading}:"
    start = lines.index(marker)
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.strip() and len(line) - len(line.lstrip()) <= indent:
            end = index
            break
    return lines[start:end]


def branch_filters(event_block: list[str]) -> set[str]:
    for index, line in enumerate(event_block):
        stripped = line.strip()
        if not stripped.startswith("branches:"):
            continue
        value = stripped.removeprefix("branches:").strip()
        if value:
            if not (value.startswith("[") and value.endswith("]")):
                raise AssertionError(f"unsupported inline branch filter: {value}")
            return {branch.strip() for branch in value[1:-1].split(",")}
        branch_indent = len(line) - len(line.lstrip())
        branches: set[str] = set()
        for candidate in event_block[index + 1 :]:
            candidate_indent = len(candidate) - len(candidate.lstrip())
            if candidate.strip() and candidate_indent <= branch_indent:
                break
            if candidate.strip().startswith("- "):
                branches.add(candidate.strip().removeprefix("- ").strip())
        return branches
    raise AssertionError("branches filter not found")


@pytest.mark.parametrize("workflow", ["quality.yml", "privacy-security.yml"])
def test_v2_child_pull_request_bases_are_explicit(workflow: str) -> None:
    trigger = indented_block(workflow_text(workflow), "on", 0)
    pull_request = indented_block("\n".join(trigger), "pull_request", 2)
    assert branch_filters(pull_request) == REQUIRED_PR_BASES


def test_privacy_manual_dispatch_and_security_guards_are_preserved() -> None:
    for workflow in ("quality.yml", "privacy-security.yml"):
        text = workflow_text(workflow)
        trigger = indented_block(text, "on", 0)
        permissions = indented_block(text, "permissions", 0)
        assert not any("pull_request_target:" in line for line in trigger)
        assert "  contents: read" in permissions
        assert not any("write" in line for line in permissions)

    privacy = workflow_text("privacy-security.yml")
    privacy_trigger = indented_block(privacy, "on", 0)
    assert "  workflow_dispatch:" in privacy_trigger
    assert "          fetch-depth: 0" in privacy
    assert "python scripts/audit_privacy.py --include-git --history-warn-only" in privacy
    assert "python -m detect_secrets scan --all-files" in privacy


def test_quality_keeps_the_full_validation_command_set() -> None:
    quality = workflow_text("quality.yml")
    commands = {
        line.strip().removeprefix("- run: ")
        for line in quality.splitlines()
        if line.strip().startswith("- run: ")
    }
    assert commands == QUALITY_COMMANDS
