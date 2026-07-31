from __future__ import annotations

from scripts.check_readme_navigation import (
    DOCS_URL,
    README,
    ROOT,
    check_hub_pages,
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


def test_hub_pages_meet_information_architecture_bar() -> None:
    assert check_hub_pages(ROOT) == []


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


def test_documentation_cta_is_required() -> None:
    text = current_readme().replace(DOCS_URL, "https://example.invalid/")
    errors = check_readme(text, ROOT)
    assert any("primary CTA target" in error for error in errors)


def test_resource_cta_is_required() -> None:
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
