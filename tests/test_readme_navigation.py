from __future__ import annotations

from pathlib import Path

from scripts.check_readme_navigation import (
    DOCS_URL,
    README,
    ROOT,
    check_hub_pages,
    check_learn_hub_modules,
    check_readme,
    inventory_counts,
)


def current_readme() -> str:
    return README.read_text(encoding="utf-8")


def test_current_readme_navigation_passes() -> None:
    assert check_readme(current_readme(), ROOT) == []


def test_inventory_matches_source_of_truth() -> None:
    counts = inventory_counts(ROOT)
    assert counts["modules"] == 13
    assert counts["patterns"] == 26
    assert counts["templates"] == 28
    assert counts["providers"] == 8
    assert counts["capstones"] == 3
    assert counts["exercises"] == 13
    assert counts["quizzes"] == 13
    assert counts["solutions"] == 13
    assert counts["official_resources"] == 24
    assert counts["courses"] == 7
    assert counts["credentials"] == 5


def test_hub_pages_meet_information_architecture_bar() -> None:
    assert check_hub_pages(ROOT) == []


def test_learn_hub_lists_all_modules() -> None:
    assert check_learn_hub_modules(ROOT) == []


def test_removing_curriculum_module_fails() -> None:
    text = current_readme().replace(
        "curriculum/05-structured-outputs/README.md",
        "curriculum/05-structured-output-missing/README.md",
    )
    errors = check_readme(text, ROOT)
    assert any("05-structured-outputs" in error for error in errors)


def test_removing_provider_guide_fails() -> None:
    text = current_readme().replace("docs/providers/mistral.md", "docs/providers/missing.md")
    errors = check_readme(text, ROOT)
    assert any("docs/providers/mistral.md" in error for error in errors)


def test_removing_capstone_fails() -> None:
    text = current_readme().replace(
        "labs/capstones/research-assistant.md",
        "labs/capstones/missing-research-assistant.md",
    )
    errors = check_readme(text, ROOT)
    assert any("labs/capstones/research-assistant.md" in error for error in errors)


def test_v2_draft_docs_cta_is_required() -> None:
    text = current_readme().replace("(docs/index.md)", "(docs/missing-home.md)")
    errors = check_readme(text, ROOT)
    assert any("docs/index.md" in error for error in errors)


def test_prompt_reference_cta_must_not_target_resources() -> None:
    text = current_readme().replace(
        "[Browse Prompt Reference](docs/reference/index.md)",
        "[Browse Prompt Reference](docs/resources/index.md)",
        1,
    )
    errors = check_readme(text, ROOT)
    assert any("must not target Courses & Resources hub" in error for error in errors)


def test_v2_draft_docs_cta_must_not_target_pages() -> None:
    text = current_readme().replace(
        "[Open V2 Draft Docs](docs/index.md)",
        f"[Open V2 Draft Docs]({DOCS_URL})",
        1,
    )
    errors = check_readme(text, ROOT)
    assert any("must not target the published Pages site" in error for error in errors)


def test_resources_hub_remains_reachable() -> None:
    text = current_readme().replace("docs/resources/index.md", "docs/resources/missing.md")
    errors = check_readme(text, ROOT)
    assert any("docs/resources/index.md" in error for error in errors)


def test_raw_catalog_cta_fails() -> None:
    text = current_readme() + "\n[Contracts](catalog/prompt_contracts.json)\n"
    errors = check_readme(text, ROOT)
    assert any("raw catalog as visitor CTA" in error for error in errors)


def test_inventory_drift_fails() -> None:
    text = current_readme().replace("| Prompt patterns | 26 |", "| Prompt patterns | 99 |")
    text = text.replace("| Prompt patterns | 26 records |", "| Prompt patterns | 99 records |")
    errors = check_readme(text, ROOT)
    assert any("Prompt patterns" in error and "expected 26" in error for error in errors)


def test_official_resource_inventory_drift_fails() -> None:
    text = current_readme().replace(
        "| Official-resource catalog records | 24 |",
        "| Official-resource catalog records | 25 |",
    )
    errors = check_readme(text, ROOT)
    assert any(
        "Official-resource catalog records" in error and "expected 24" in error for error in errors
    )


def test_missing_middle_learn_module_fails(tmp_path: Path) -> None:
    learn = ROOT / "docs" / "learn" / "index.md"
    original = learn.read_text(encoding="utf-8")
    mutated = original.replace("[LLM Foundations](llm-foundations.md)", "REMOVED")
    # Evaluate through a temporary root copy is heavy; mutate via check_learn_hub_modules
    # by writing to a temp tree.
    import shutil

    for name in ("docs", "curriculum", "catalog", "labs"):
        shutil.copytree(ROOT / name, tmp_path / name, dirs_exist_ok=True)
    (tmp_path / "docs" / "learn" / "index.md").write_text(mutated, encoding="utf-8")
    errors = check_learn_hub_modules(tmp_path)
    assert any("01-llm-foundations" in error for error in errors)


def test_duplicate_learn_module_fails(tmp_path: Path) -> None:
    import shutil

    for name in ("docs", "curriculum", "catalog", "labs"):
        shutil.copytree(ROOT / name, tmp_path / name, dirs_exist_ok=True)
    learn = tmp_path / "docs" / "learn" / "index.md"
    text = learn.read_text(encoding="utf-8")
    learn.write_text(
        text + "\n| Extra | Dup | [LLM Foundations](llm-foundations.md) |\n",
        encoding="utf-8",
    )
    errors = check_learn_hub_modules(tmp_path)
    assert any("duplicates module 01-llm-foundations" in error for error in errors)


def test_missing_explained_solution_fails() -> None:
    text = current_readme().replace(
        "Lesson → Exercise → Quiz → Explained solution → Checklist → Capstone",
        "Lesson → Exercise → Quiz → Checklist → Capstone",
    )
    errors = check_readme(text, ROOT)
    assert any("missing complete practice sequence" in error for error in errors)


def test_reordered_practice_sequence_fails() -> None:
    text = current_readme().replace(
        "Lesson → Exercise → Quiz → Explained solution → Checklist → Capstone",
        "Lesson → Quiz → Exercise → Explained solution → Checklist → Capstone",
    )
    errors = check_readme(text, ROOT)
    assert any("missing complete practice sequence" in error for error in errors)


def test_intent_route_must_be_linked() -> None:
    text = current_readme().replace(
        "| Learn from zero | [Learning Path](LEARNING_PATH.md) |",
        "| Learn from zero | Learning Path |",
        1,
    )
    errors = check_readme(text, ROOT)
    assert any("intent route missing link: Learn from zero" in error for error in errors)


def test_local_absolute_path_fails() -> None:
    errors = check_readme(current_readme() + "\nD:\\private\\file.md\n", ROOT)
    assert "README contains a local absolute filesystem path" in errors


def test_placeholder_destination_fails() -> None:
    errors = check_readme(
        current_readme() + "\nSee [module](curriculum/<module>/README.md).\n",
        ROOT,
    )
    assert "README contains a user-facing placeholder path" in errors
