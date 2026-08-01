from __future__ import annotations

from datetime import date
from pathlib import Path

from scripts.audit_privacy import PATTERNS, scan_files, scan_text
from scripts.check_freshness import check
from scripts.check_internal_links import check_links
from scripts.generate_docs_indexes import write_outputs

ROOT = Path(__file__).resolve().parents[1]


def test_generated_indexes_are_current() -> None:
    assert write_outputs(check=True) == []


def test_internal_links_pass() -> None:
    assert check_links() == []


def test_privacy_current_tree_has_no_unapproved_findings() -> None:
    findings = scan_files(include_site=False)
    assert [finding for finding in findings if not finding.allowed] == []


def test_turkish_phone_requires_trunk_or_country_prefix() -> None:
    phone = PATTERNS["phone"]
    local = "0" + "532" + "1234567"
    spaced = "+90 " + "532" + " " + "123" + " " + "45" + " " + "67"
    intl = "0090" + "532" + "1234567"
    bare = "532" + "1234567"
    assert phone.search(local)
    assert phone.search(spaced)
    assert phone.search(intl)
    assert phone.search(bare) is None


def test_mkdocs_material_svg_path_coordinates_are_not_phones() -> None:
    # Coordinates from mkdocs-material 9.7 GitHub icon SVG path data.
    svg_path = (
        "C436.2 457.8 504 362.9 504 252 504 113.3 391.5 8 252.8 8M105.2 352.9c-1.3 1-1 3.3.7 5.2"
    )
    findings = scan_text(svg_path, "site/index.html", "current_tree")
    assert [finding for finding in findings if finding.category == "phone"] == []


def test_freshness_has_no_failures() -> None:
    _, failures = check(as_of=date(2026, 8, 1))
    assert failures == []


def test_curriculum_has_13_modules() -> None:
    modules = [path for path in (ROOT / "curriculum").iterdir() if path.is_dir()]
    assert len(modules) == 13


def test_each_curriculum_module_has_exercise_quiz_and_checklist() -> None:
    for module in (ROOT / "curriculum").iterdir():
        if module.is_dir():
            assert (module / "exercise.md").exists()
            assert (module / "quiz.md").exists()
            assert (module / "checklist.md").exists()


def test_each_curriculum_module_has_solution_criteria() -> None:
    for module in (ROOT / "curriculum").iterdir():
        if module.is_dir():
            assert (ROOT / "labs" / "solutions" / f"{module.name}.md").exists()


def test_docs_nav_sections_exist() -> None:
    text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    for section in [
        "Start Learning:",
        "Prompt Reference:",
        "Provider Guides:",
        "Courses & Resources:",
        "Practice & Labs:",
        "Contribute:",
        "Project:",
    ]:
        assert section in text


def test_project_audit_docs_exist() -> None:
    for name in [
        "v1-content-audit.md",
        "privacy-audit.md",
        "v2-architecture.md",
        "v1-to-v2-migration.md",
        "v2-release-gates.md",
    ]:
        assert (ROOT / "docs" / "project" / name).exists()


def test_no_legacy_resources_catalog() -> None:
    assert not (ROOT / "catalog" / "resources.json").exists()


def test_learning_path_exists() -> None:
    assert (ROOT / "LEARNING_PATH.md").exists()


def test_security_policy_mentions_private_advisories() -> None:
    text = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    assert "private security advisories" in text


def test_agents_file_has_non_invention_rules() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "Never invent links" in text
    assert "Never invent links, prices, certification status" in text


def test_license_mentions_external_resources_not_relicensed() -> None:
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "does not relicense" in text


def test_labs_have_three_capstones() -> None:
    assert len(list((ROOT / "labs" / "capstones").glob("*.md"))) >= 3
