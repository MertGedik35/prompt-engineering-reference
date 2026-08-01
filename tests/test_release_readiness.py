from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from scripts import check_release_readiness as readiness
from scripts.check_release_readiness import (
    EDIT_URI_REQUIRED,
    EXPECTED_INVENTORY,
    check_edit_uri,
    check_learning_stubs,
    check_pages_workflow_preserved,
    check_public_draft_markers,
    check_release_readiness,
)

ROOT = Path(__file__).resolve().parents[1]


def test_current_tree_passes_release_readiness() -> None:
    assert check_release_readiness() == []


def test_edit_uri_integration_branch_fails() -> None:
    text = (
        (ROOT / "mkdocs.yml")
        .read_text(encoding="utf-8")
        .replace(
            EDIT_URI_REQUIRED,
            "edit_uri: edit/feat/v2-learning-reference/docs/",
        )
    )
    errors = check_edit_uri(text)
    assert any("edit_uri must be" in error for error in errors)
    assert any("feat/v2-learning-reference" in error for error in errors)


def test_edit_uri_child_branch_fails() -> None:
    text = (
        (ROOT / "mkdocs.yml")
        .read_text(encoding="utf-8")
        .replace(
            EDIT_URI_REQUIRED,
            "edit_uri: edit/fix/v2-release-transition/docs/",
        )
    )
    errors = check_edit_uri(text)
    assert any("edit_uri must be" in error for error in errors)
    assert any("fix/v2-release-transition" in error for error in errors)


def test_readme_v2_is_a_draft_fails() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8") + "\nV2 is a draft under review.\n"
    errors = check_public_draft_markers(readme=readme)
    assert any("release-critical draft marker in README.md" in error for error in errors)


def test_readme_v2_draft_badge_fails() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8") + "\nV1 stable · V2 draft\n"
    errors = check_public_draft_markers(readme=readme)
    assert any("release-critical draft marker in README.md" in error for error in errors)


def test_readme_open_v2_draft_docs_fails() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8") + "\nOpen V2 Draft Docs\n"
    errors = check_public_draft_markers(readme=readme)
    assert any("release-critical draft marker in README.md" in error for error in errors)


def test_docs_index_v2_remains_a_draft_fails() -> None:
    docs_index = (ROOT / "docs" / "index.md").read_text(
        encoding="utf-8"
    ) + "\nV2 remains a draft under review.\n"
    errors = check_public_draft_markers(docs_index=docs_index)
    assert any("release-critical draft marker in docs/index.md" in error for error in errors)


def test_mkdocs_draft_release_notes_nav_fails() -> None:
    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8") + (
        "\n      - Draft Release Notes: project/v2-release-notes.md\n"
    )
    errors = check_public_draft_markers(mkdocs=mkdocs)
    assert any("Draft Release Notes" in error for error in errors)


def test_mkdocs_draft_pr_description_nav_fails() -> None:
    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8") + (
        "\n      - Draft PR Description: project/v2-development-record.md\n"
    )
    errors = check_public_draft_markers(mkdocs=mkdocs)
    assert any("Draft PR Description" in error for error in errors)


def test_learning_stub_integration_branch_fails(tmp_path: Path) -> None:
    learn = tmp_path / "docs" / "learn"
    shutil.copytree(ROOT / "docs" / "learn", learn)
    stub = learn / "orientation.md"
    stub.write_text(
        stub.read_text(encoding="utf-8").replace(
            "blob/main/",
            "blob/feat/v2-learning-reference/",
        ),
        encoding="utf-8",
    )
    errors = check_learning_stubs(learn)
    assert any("temporary branch URL" in error or "non-main branch" in error for error in errors)


def test_learning_stub_child_branch_fails(tmp_path: Path) -> None:
    learn = tmp_path / "docs" / "learn"
    shutil.copytree(ROOT / "docs" / "learn", learn)
    stub = learn / "orientation.md"
    stub.write_text(
        stub.read_text(encoding="utf-8").replace(
            "blob/main/",
            "blob/fix/v2-release-transition/",
        ),
        encoding="utf-8",
    )
    errors = check_learning_stubs(learn)
    assert any("temporary branch URL" in error or "non-main branch" in error for error in errors)


def test_learning_stub_missing_curriculum_file_fails(tmp_path: Path) -> None:
    learn = tmp_path / "docs" / "learn"
    shutil.copytree(ROOT / "docs" / "learn", learn)
    stub = learn / "orientation.md"
    stub.write_text(
        stub.read_text(encoding="utf-8").replace(
            "curriculum/00-orientation/README.md",
            "curriculum/00-orientation/MISSING-README.md",
        ),
        encoding="utf-8",
    )
    errors = check_learning_stubs(learn)
    assert any("target missing" in error or "missing readme link" in error for error in errors)


def test_learning_stub_wrong_module_fails(tmp_path: Path) -> None:
    learn = tmp_path / "docs" / "learn"
    shutil.copytree(ROOT / "docs" / "learn", learn)
    stub = learn / "orientation.md"
    stub.write_text(
        stub.read_text(encoding="utf-8").replace(
            "curriculum/00-orientation/exercise.md",
            "curriculum/01-llm-foundations/exercise.md",
        ),
        encoding="utf-8",
    )
    errors = check_learning_stubs(learn)
    assert any("wrong module" in error or "missing exercise link" in error for error in errors)


def test_learning_stub_missing_solution_fails(tmp_path: Path) -> None:
    learn = tmp_path / "docs" / "learn"
    shutil.copytree(ROOT / "docs" / "learn", learn)
    stub = learn / "orientation.md"
    stub.write_text(
        stub.read_text(encoding="utf-8").replace(
            "labs/solutions/00-orientation.md",
            "labs/solutions/00-orientation-missing.md",
        ),
        encoding="utf-8",
    )
    errors = check_learning_stubs(learn)
    assert any("target missing" in error or "missing solution link" in error for error in errors)


def test_project_page_rename_without_nav_fails() -> None:
    mkdocs = (
        (ROOT / "mkdocs.yml")
        .read_text(encoding="utf-8")
        .replace("project/v2-release-notes.md", "project/v2-release-notes-missing.md")
    )
    errors = check_public_draft_markers(mkdocs=mkdocs)
    assert any("missing V2 Release Notes navigation entry" in error for error in errors)


def test_inventory_constant_drift_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    mutated = dict(EXPECTED_INVENTORY)
    mutated["patterns"] = EXPECTED_INVENTORY["patterns"] + 1
    monkeypatch.setattr(readiness, "EXPECTED_INVENTORY", mutated)
    errors = readiness.check_inventory_preserved()
    assert any("publication inventory drift for patterns" in error for error in errors)


def test_historical_development_record_may_mention_pr10() -> None:
    text = (ROOT / "docs" / "project" / "v2-development-record.md").read_text(encoding="utf-8")
    assert "PR #10" in text
    assert check_release_readiness() == []


def test_learning_content_may_use_draft_a_prompt() -> None:
    text = (ROOT / "curriculum" / "02-prompt-anatomy" / "README.md").read_text(encoding="utf-8")
    assert "draft" in text.lower()
    assert check_release_readiness() == []


def test_generated_indexes_unchanged_by_release_transition() -> None:
    generated = ROOT / "docs" / "generated"
    assert generated.is_dir()
    # Release transition must not hand-edit generated catalog indexes.
    assert check_release_readiness() == []


def test_pages_action_pins_remain_unchanged() -> None:
    assert check_pages_workflow_preserved() == []
    text = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    assert "actions/configure-pages@v6" in text
    assert "actions/upload-pages-artifact@v5" in text
    assert "actions/deploy-pages@v5" in text


def test_pages_main_only_deployment_preserved() -> None:
    text = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    assert "branches: [main]" in text
    assert "pull_request_target:" not in text
    assert check_pages_workflow_preserved() == []


def test_own_repo_main_blob_maps_to_local_curriculum() -> None:
    from scripts.check_external_links import local_path_for_own_repo_main_blob

    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/main/curriculum/00-orientation/README.md"
    )
    path = local_path_for_own_repo_main_blob(url)
    assert path is not None
    assert path.is_file()
    missing = local_path_for_own_repo_main_blob(
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/main/curriculum/00-orientation/MISSING.md"
    )
    assert missing is not None
    assert not missing.is_file()
