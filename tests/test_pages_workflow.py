from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES_WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"


def workflow_text() -> str:
    return PAGES_WORKFLOW.read_text(encoding="utf-8")


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


def uses_lines(job_block: list[str]) -> list[str]:
    return [
        line.strip().removeprefix("- uses: ").strip()
        for line in job_block
        if line.strip().startswith("- uses: ")
    ]


def run_lines(job_block: list[str]) -> list[str]:
    return [
        line.strip().removeprefix("- run: ").strip()
        for line in job_block
        if line.strip().startswith("- run: ")
    ]


def test_pages_workflow_triggers_and_security_invariants() -> None:
    text = workflow_text()
    trigger = indented_block(text, "on", 0)
    assert "  push:" in trigger
    push = indented_block("\n".join(trigger), "push", 2)
    assert any(line.strip() == "branches: [main]" for line in push)
    assert "  workflow_dispatch:" in trigger
    assert not any("pull_request_target:" in line for line in trigger)

    permissions = indented_block(text, "permissions", 0)
    assert "  contents: read" in permissions
    assert "  pages: write" in permissions
    assert "  id-token: write" in permissions

    concurrency = indented_block(text, "concurrency", 0)
    assert "  group: pages" in concurrency
    assert "  cancel-in-progress: false" in concurrency


def test_pages_build_job_uses_coordinated_action_versions() -> None:
    text = workflow_text()
    jobs = indented_block(text, "jobs", 0)
    build = indented_block("\n".join(jobs), "build", 2)
    uses = uses_lines(build)
    runs = run_lines(build)

    assert uses[0].startswith("actions/checkout@")
    assert uses[1].startswith("actions/setup-python@")
    assert "actions/configure-pages@v6" in uses
    assert "actions/upload-pages-artifact@v5" in uses
    assert 'python -m pip install -e ".[docs]"' in runs
    assert "python -m mkdocs build --strict" in runs

    upload_index = next(
        index for index, line in enumerate(build) if "actions/upload-pages-artifact@v5" in line
    )
    assert any(line.strip() == "path: site" for line in build[upload_index : upload_index + 4])


def test_pages_deploy_job_depends_on_build_and_uses_v5() -> None:
    text = workflow_text()
    jobs = indented_block(text, "jobs", 0)
    deploy = indented_block("\n".join(jobs), "deploy", 2)
    assert "    needs: build" in deploy
    assert "      name: github-pages" in deploy
    assert "      url: ${{ steps.deployment.outputs.page_url }}" in deploy
    assert "        uses: actions/deploy-pages@v5" in deploy
    assert any(line.strip() == "- id: deployment" for line in deploy)
