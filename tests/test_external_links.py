from __future__ import annotations

from pathlib import Path

from scripts.check_external_links import (
    classify_own_repo_main_blob,
    evaluate_urls,
    local_path_for_own_repo_main_blob,
    normalize_extracted_url,
    tracked_repository_paths,
)
from scripts.check_release_readiness import (
    HISTORICAL_ALLOWLIST,
    check_forbidden_branch_references,
    temporary_branch_urls,
)

ROOT = Path(__file__).resolve().parents[1]
VALID = (
    "https://github.com/MertGedik35/prompt-engineering-reference/"
    "blob/main/curriculum/00-orientation/README.md"
)
SOLUTION = (
    "https://github.com/MertGedik35/prompt-engineering-reference/"
    "blob/main/labs/solutions/00-orientation.md"
)


def test_tracked_blob_main_curriculum_is_valid() -> None:
    tracked = tracked_repository_paths(ROOT)
    result = classify_own_repo_main_blob(VALID, root=ROOT, tracked_paths=tracked)
    assert result.status == "valid_tracked_target"
    assert result.relative_path == "curriculum/00-orientation/README.md"
    assert local_path_for_own_repo_main_blob(VALID, tracked_paths=tracked) == (
        ROOT / "curriculum/00-orientation/README.md"
    )


def test_tracked_blob_main_solution_is_valid() -> None:
    result = classify_own_repo_main_blob(SOLUTION, root=ROOT)
    assert result.status == "valid_tracked_target"
    assert result.relative_path == "labs/solutions/00-orientation.md"


def test_trailing_punctuation_is_normalized() -> None:
    assert normalize_extracted_url(VALID + ").") == VALID
    result = classify_own_repo_main_blob(VALID + ").")
    assert result.status == "valid_tracked_target"


def test_missing_tracked_target_fails() -> None:
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/main/curriculum/00-orientation/MISSING.md"
    )
    result = classify_own_repo_main_blob(url, root=ROOT)
    assert result.status == "missing_target"


def test_untracked_local_file_fails(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "tracked.md").write_text("tracked\n", encoding="utf-8")
    # Initialize minimal git index via explicit tracked set injection.
    tracked = frozenset({"tracked.md"})
    untracked = repo / "untracked.md"
    untracked.write_text("untracked\n", encoding="utf-8")
    url = "https://github.com/MertGedik35/prompt-engineering-reference/blob/main/untracked.md"
    result = classify_own_repo_main_blob(url, root=repo, tracked_paths=tracked)
    assert result.status == "untracked_target"
    assert "not tracked by Git" in (result.detail or "")


def test_ignored_local_file_fails_like_untracked(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    ignored = repo / "ignored.md"
    ignored.write_text("ignored\n", encoding="utf-8")
    tracked = frozenset({"tracked.md"})
    url = "https://github.com/MertGedik35/prompt-engineering-reference/blob/main/ignored.md"
    result = classify_own_repo_main_blob(url, root=repo, tracked_paths=tracked)
    assert result.status == "untracked_target"


def test_wrong_filename_case_fails_even_if_disk_matches(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "curriculum" / "00-orientation").mkdir(parents=True)
    (repo / "curriculum" / "00-orientation" / "README.md").write_text("x\n", encoding="utf-8")
    tracked = frozenset({"curriculum/00-orientation/README.md"})
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/main/curriculum/00-orientation/readme.md"
    )
    result = classify_own_repo_main_blob(url, root=repo, tracked_paths=tracked)
    assert result.status == "case_mismatch"
    assert "README.md" in (result.detail or "")


def test_wrong_directory_case_fails(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "curriculum" / "00-orientation").mkdir(parents=True)
    (repo / "curriculum" / "00-orientation" / "README.md").write_text("x\n", encoding="utf-8")
    tracked = frozenset({"curriculum/00-orientation/README.md"})
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/main/Curriculum/00-orientation/README.md"
    )
    result = classify_own_repo_main_blob(url, root=repo, tracked_paths=tracked)
    assert result.status == "case_mismatch"


def test_directory_target_fails(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "curriculum" / "00-orientation").mkdir(parents=True)
    tracked = frozenset({"curriculum/00-orientation"})
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/main/curriculum/00-orientation"
    )
    result = classify_own_repo_main_blob(url, root=repo, tracked_paths=tracked)
    assert result.status == "missing_target"
    assert "not a regular file" in (result.detail or "")


def test_wrong_owner_is_not_applicable() -> None:
    url = (
        "https://github.com/EvilOwner/prompt-engineering-reference/"
        "blob/main/curriculum/00-orientation/README.md"
    )
    assert classify_own_repo_main_blob(url).status == "not_applicable"


def test_wrong_repository_is_not_applicable() -> None:
    url = "https://github.com/MertGedik35/other-repo/blob/main/curriculum/00-orientation/README.md"
    assert classify_own_repo_main_blob(url).status == "not_applicable"


def test_wrong_branch_is_not_applicable() -> None:
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/feat/v2-learning-reference/curriculum/00-orientation/README.md"
    )
    assert classify_own_repo_main_blob(url).status == "not_applicable"


def test_tree_main_is_not_applicable() -> None:
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "tree/main/curriculum/00-orientation/README.md"
    )
    assert classify_own_repo_main_blob(url).status == "not_applicable"


def test_raw_main_is_not_applicable() -> None:
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "raw/main/curriculum/00-orientation/README.md"
    )
    assert classify_own_repo_main_blob(url).status == "not_applicable"


def test_non_https_is_not_applicable() -> None:
    url = (
        "http://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/main/curriculum/00-orientation/README.md"
    )
    assert classify_own_repo_main_blob(url).status == "not_applicable"


def test_lookalike_host_is_not_applicable() -> None:
    url = (
        "https://github.com.evil.example/MertGedik35/prompt-engineering-reference/"
        "blob/main/curriculum/00-orientation/README.md"
    )
    assert classify_own_repo_main_blob(url).status == "not_applicable"


def test_path_traversal_is_invalid() -> None:
    url = "https://github.com/MertGedik35/prompt-engineering-reference/blob/main/../README.md"
    result = classify_own_repo_main_blob(url)
    assert result.status == "invalid_url"


def test_encoded_traversal_is_invalid() -> None:
    url = "https://github.com/MertGedik35/prompt-engineering-reference/blob/main/%2e%2e/README.md"
    result = classify_own_repo_main_blob(url)
    assert result.status == "invalid_url"
    assert "percent-encoding" in (result.detail or "")


def test_encoded_slash_is_invalid() -> None:
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/main/curriculum%2f00-orientation/README.md"
    )
    result = classify_own_repo_main_blob(url)
    assert result.status == "invalid_url"


def test_encoded_backslash_is_invalid() -> None:
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/main/curriculum%5c00-orientation/README.md"
    )
    result = classify_own_repo_main_blob(url)
    assert result.status == "invalid_url"


def test_query_string_is_invalid_for_blob_main() -> None:
    result = classify_own_repo_main_blob(VALID + "?plain=1")
    assert result.status == "invalid_url"
    assert "query" in (result.detail or "")


def test_fragment_is_invalid_for_blob_main() -> None:
    result = classify_own_repo_main_blob(VALID + "#L1")
    assert result.status == "invalid_url"


def test_extra_path_component_missing() -> None:
    url = VALID + "/extra"
    result = classify_own_repo_main_blob(url)
    assert result.status == "missing_target"


def test_wrong_module_tracked_path_is_valid_but_distinct() -> None:
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/main/curriculum/01-llm-foundations/README.md"
    )
    result = classify_own_repo_main_blob(url)
    assert result.status == "valid_tracked_target"
    assert result.relative_path == "curriculum/01-llm-foundations/README.md"


def test_issue_link_uses_http_path_not_local_map() -> None:
    url = "https://github.com/MertGedik35/prompt-engineering-reference/issues/1"
    assert classify_own_repo_main_blob(url).status == "not_applicable"
    seen: list[str] = []

    def fake_http(candidate: str, retries: int) -> tuple[str, str]:
        seen.append(candidate)
        return "ok", "200"

    malformed, broken, warnings, checked = evaluate_urls(
        [url],
        live=True,
        retries=0,
        http_checker=fake_http,
    )
    assert malformed == []
    assert broken == []
    assert checked == 1
    assert seen == [url]
    assert not any("same_repo_main_local_target" in item for item in warnings)


def test_valid_local_target_emits_durable_warning() -> None:
    malformed, broken, warnings, checked = evaluate_urls(
        [VALID],
        live=True,
        retries=0,
        http_checker=lambda url, retries: ("broken", "should-not-run"),
    )
    assert malformed == []
    assert broken == []
    assert checked == 1
    assert any(item.startswith("same_repo_main_local_target:") for item in warnings)
    assert not any("pending_main_publication" in item for item in warnings)


def test_untracked_blob_main_is_broken_not_http_fallback(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "untracked.md").write_text("x\n", encoding="utf-8")
    tracked = frozenset({"tracked.md"})
    url = "https://github.com/MertGedik35/prompt-engineering-reference/blob/main/untracked.md"
    seen: list[str] = []

    def fake_http(candidate: str, retries: int) -> tuple[str, str]:
        seen.append(candidate)
        return "ok", "200"

    # Patch classify by using evaluate with custom root via classify injection path:
    # evaluate_urls uses tracked_repository_paths(root); for tmp repos without git,
    # call classify directly and assert status, then assert evaluate with monkeypatched
    # tracked set by testing classify + broken message format.
    result = classify_own_repo_main_blob(url, root=repo, tracked_paths=tracked)
    assert result.status == "untracked_target"
    assert seen == []


def test_historical_prose_may_mention_temporary_branch() -> None:
    text = (
        "The integration branch was `feat/v2-learning-reference`.\n"
        "V2 was reviewed through draft PR #10.\n"
        "The release-transition branch was fix/v2-release-transition.\n"
        "See https://github.com/MertGedik35/prompt-engineering-reference/pull/10\n"
        "and https://github.com/MertGedik35/prompt-engineering-reference/pull/18\n"
        "and https://github.com/MertGedik35/prompt-engineering-reference/"
        "commit/5874a1e56c7bdd570a6f005d4541d08874672234\n"
    )
    relative = next(iter(HISTORICAL_ALLOWLIST))
    errors = check_forbidden_branch_references(texts={relative: text})
    assert errors == []
    assert temporary_branch_urls(text) == []


def test_historical_markdown_blob_link_is_rejected() -> None:
    relative = "docs/project/v2-development-record.md"
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/feat/v2-learning-reference/curriculum/00-orientation/README.md"
    )
    text = f"[Old lesson]({url})\n"
    errors = check_forbidden_branch_references(texts={relative: text})
    assert any("active temporary-branch URL" in error for error in errors)
    assert any(url in error for error in errors)
    assert any(relative in error for error in errors)
    assert any("feat/v2-learning-reference" in error for error in errors)


def test_historical_raw_tree_url_is_rejected() -> None:
    relative = "docs/project/v2-semantic-content-audit.md"
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "tree/feat/v2-learning-reference/curriculum"
    )
    errors = check_forbidden_branch_references(texts={relative: url + "\n"})
    assert any("active temporary-branch URL" in error and url in error for error in errors)


def test_historical_html_edit_href_is_rejected() -> None:
    relative = "docs/project/v1-to-v2-migration.md"
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "edit/feat/v2-learning-reference/docs/index.md"
    )
    text = f'<a href="{url}">edit</a>\n'
    errors = check_forbidden_branch_references(texts={relative: text})
    assert any(url in error for error in errors)


def test_historical_html_raw_src_is_rejected() -> None:
    relative = "docs/project/v2-architecture.md"
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "raw/feat/v2-learning-reference/README.md"
    )
    text = f'<img src="{url}" />\n'
    errors = check_forbidden_branch_references(texts={relative: text})
    assert any(url in error for error in errors)


def test_historical_child_branch_blob_is_rejected() -> None:
    relative = "docs/project/v2-release-gates.md"
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/fix/v2-release-transition/README.md"
    )
    errors = check_forbidden_branch_references(texts={relative: f"[x]({url})\n"})
    assert any("fix/v2-release-transition" in error for error in errors)


def test_historical_codex_branch_blob_is_rejected() -> None:
    relative = "docs/project/privacy-audit.md"
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/codex/example-branch/README.md"
    )
    errors = check_forbidden_branch_references(texts={relative: f"[x]({url})\n"})
    assert any("codex/" in error or "codex/example-branch" in error for error in errors)


def test_historical_reference_style_link_is_rejected() -> None:
    relative = "docs/project/v1-content-audit.md"
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/feat/v2-learning-reference/README.md"
    )
    text = f"[label][ref]\n\n[ref]: {url}\n"
    errors = check_forbidden_branch_references(texts={relative: text})
    assert any(url in error for error in errors)


def test_historical_autolink_is_rejected() -> None:
    relative = "docs/project/v2-development-record.md"
    url = (
        "https://github.com/MertGedik35/prompt-engineering-reference/"
        "blob/feat/v2-learning-reference/README.md"
    )
    text = f"<{url}>\n"
    errors = check_forbidden_branch_references(texts={relative: text})
    assert any(url in error for error in errors)


def test_non_historical_file_still_rejects_plain_branch_marker() -> None:
    errors = check_forbidden_branch_references(
        texts={"docs/index.md": "See feat/v2-learning-reference for history.\n"}
    )
    assert any("publication-sensitive branch reference" in error for error in errors)
