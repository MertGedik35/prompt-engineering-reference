from __future__ import annotations

from scripts.check_readme_navigation import DOCS_URL, README, ROOT, check_readme


def current_readme() -> str:
    return README.read_text(encoding="utf-8")


def test_current_readme_navigation_passes() -> None:
    assert check_readme(current_readme(), ROOT) == []


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
    assert any("documentation-site link" in error for error in errors)


def test_plain_text_audience_route_fails() -> None:
    text = current_readme().replace(
        "| Complete beginner | [Orientation](curriculum/00-orientation/README.md)",
        "| Complete beginner | Orientation",
        1,
    )
    errors = check_readme(text, ROOT)
    assert any(
        "audience route contains an unlinked destination: Complete beginner" in error
        for error in errors
    )


def test_local_absolute_path_fails() -> None:
    errors = check_readme(current_readme() + "\nD:\\private\\file.md\n", ROOT)
    assert "README contains a local absolute filesystem path" in errors


def test_placeholder_destination_fails() -> None:
    errors = check_readme(
        current_readme() + "\nSee [module](curriculum/<module>/README.md).\n",
        ROOT,
    )
    assert "README contains a user-facing placeholder path" in errors
