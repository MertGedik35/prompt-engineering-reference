"""External URL validation with narrow same-repository main-link Git checks."""

from __future__ import annotations

import argparse
import json
import re
import ssl
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Literal
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
URL_RE = re.compile(r"https?://[^\s)\]>'\"<>]+")
TRAILING_PUNCT_RE = re.compile(r"[).,;\"']+$")
OWNER = "MertGedik35"
REPO = "prompt-engineering-reference"
REPO_SLUG = f"{OWNER}/{REPO}"
BLOB_MAIN_PREFIX = f"/{REPO_SLUG}/blob/main/"
CONTENT_OPS = frozenset({"blob", "tree", "edit", "blame", "raw"})
LocalStatus = Literal[
    "not_applicable",
    "valid_tracked_target",
    "invalid_url",
    "missing_target",
    "untracked_target",
    "case_mismatch",
    "outside_root",
]

CATALOGS = [
    "catalog/official-resources.json",
    "catalog/repositories.json",
    "catalog/courses.json",
    "catalog/credentials.json",
    "catalog/videos.json",
    "catalog/papers.json",
    "catalog/books.json",
    "catalog/tools.json",
    "catalog/communities.json",
]


@dataclass(frozen=True)
class LocalMainTarget:
    status: LocalStatus
    relative_path: str | None = None
    detail: str | None = None


def normalize_extracted_url(url: str) -> str:
    return TRAILING_PUNCT_RE.sub("", url.strip())


def tracked_repository_paths(root: Path = ROOT) -> frozenset[str]:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    paths = [
        path.replace("\\", "/") for path in completed.stdout.decode("utf-8").split("\0") if path
    ]
    return frozenset(paths)


def _encoded_path_is_unsafe(encoded_relative: str) -> str | None:
    lowered = encoded_relative.lower()
    for token in ("%2e", "%2f", "%5c"):
        if token in lowered:
            return f"unsafe percent-encoding ({token})"
    if "\\" in encoded_relative or "\x00" in encoded_relative:
        return "backslash or NUL in path"
    return None


def _decoded_relative_is_unsafe(relative: str) -> str | None:
    if not relative or relative.startswith("/") or relative.startswith("\\"):
        return "empty or absolute relative path"
    if "\\" in relative or "\x00" in relative:
        return "backslash or NUL after decode"
    if re.match(r"^[A-Za-z]:", relative):
        return "drive-letter path"
    posix = PurePosixPath(relative)
    if posix.is_absolute():
        return "absolute POSIX path"
    for part in posix.parts:
        if part in {".", ".."}:
            return "dot-segment in path"
    return None


def classify_own_repo_main_blob(
    url: str,
    *,
    root: Path = ROOT,
    tracked_paths: frozenset[str] | None = None,
) -> LocalMainTarget:
    """Classify exact same-repository ``blob/main`` URLs against the Git index."""
    cleaned = normalize_extracted_url(url)
    parsed = urlsplit(cleaned)
    if parsed.scheme != "https" or parsed.hostname != "github.com":
        return LocalMainTarget("not_applicable")
    if parsed.port not in {None, 443}:
        return LocalMainTarget("not_applicable")
    if parsed.query or parsed.fragment:
        if parsed.path.startswith(BLOB_MAIN_PREFIX):
            return LocalMainTarget(
                "invalid_url",
                detail="query strings and fragments are not allowed",
            )
        return LocalMainTarget("not_applicable")

    path = parsed.path
    if not path.startswith(BLOB_MAIN_PREFIX):
        return LocalMainTarget("not_applicable")
    encoded_relative = path[len(BLOB_MAIN_PREFIX) :]
    if not encoded_relative:
        return LocalMainTarget("invalid_url", detail="missing repository-relative path")

    unsafe_encoded = _encoded_path_is_unsafe(encoded_relative)
    if unsafe_encoded is not None:
        return LocalMainTarget("invalid_url", detail=unsafe_encoded)

    relative = unquote(encoded_relative)
    if relative != encoded_relative and "%" in relative:
        # Reject ambiguous double-encoded forms after one controlled decode.
        return LocalMainTarget("invalid_url", detail="ambiguous percent-encoding")
    unsafe_decoded = _decoded_relative_is_unsafe(relative)
    if unsafe_decoded is not None:
        return LocalMainTarget("invalid_url", detail=unsafe_decoded)

    relative = PurePosixPath(relative).as_posix()
    tracked = tracked_paths if tracked_paths is not None else tracked_repository_paths(root)
    if relative not in tracked:
        lower_hits = sorted(path for path in tracked if path.lower() == relative.lower())
        if lower_hits:
            return LocalMainTarget(
                "case_mismatch",
                relative_path=relative,
                detail=f"Git index has exact path {lower_hits[0]!r}",
            )
        candidate = root / relative
        if candidate.exists():
            return LocalMainTarget(
                "untracked_target",
                relative_path=relative,
                detail="path exists on disk but is not tracked by Git",
            )
        return LocalMainTarget(
            "missing_target",
            relative_path=relative,
            detail="path is not present in the Git index",
        )

    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return LocalMainTarget(
            "outside_root",
            relative_path=relative,
            detail="resolved path escapes repository root",
        )
    if candidate.is_symlink():
        # Symlink targets must still resolve inside the repository.
        try:
            candidate.resolve(strict=True).relative_to(root.resolve())
        except (OSError, ValueError):
            return LocalMainTarget(
                "outside_root",
                relative_path=relative,
                detail="symlink resolves outside repository root",
            )
    if not candidate.is_file():
        return LocalMainTarget(
            "missing_target",
            relative_path=relative,
            detail="tracked path is not a regular file",
        )
    return LocalMainTarget("valid_tracked_target", relative_path=relative)


def local_path_for_own_repo_main_blob(
    url: str,
    *,
    root: Path = ROOT,
    tracked_paths: frozenset[str] | None = None,
) -> Path | None:
    """Backward-compatible helper: return a path only for valid tracked targets."""
    result = classify_own_repo_main_blob(url, root=root, tracked_paths=tracked_paths)
    if result.status != "valid_tracked_target" or result.relative_path is None:
        return None
    return root / result.relative_path


def catalog_urls(root: Path = ROOT) -> set[str]:
    urls: set[str] = set()
    for file in CATALOGS:
        data = json.loads((root / file).read_text(encoding="utf-8"))
        urls.update(str(record["canonical_url"]) for record in data if "canonical_url" in record)
    return urls


def markdown_urls(root: Path = ROOT) -> set[str]:
    urls: set[str] = set()
    for path in root.rglob("*.md"):
        if any(part in {".git", ".venv", "site"} for part in path.relative_to(root).parts):
            continue
        for match in URL_RE.findall(path.read_text(encoding="utf-8")):
            urls.add(normalize_extracted_url(match))
    return urls


def collect_urls(root: Path = ROOT) -> list[str]:
    return sorted(catalog_urls(root) | markdown_urls(root))


def request_url(url: str, method: str) -> tuple[int | None, str, str | None]:
    request = Request(
        url,
        method=method,
        headers={"User-Agent": "PromptEngineeringReferenceLinkCheck/2.0"},
    )
    context = ssl.create_default_context()
    with urlopen(request, timeout=25, context=context) as response:
        return response.getcode(), response.url, None


def check_url(url: str, retries: int) -> tuple[str, str]:
    last_error = ""
    for attempt in range(retries + 1):
        try:
            status, final_url, _ = request_url(url, "HEAD")
            if status and 200 <= status < 400:
                if final_url.rstrip("/") != url.rstrip("/"):
                    return "redirect", final_url
                return "ok", str(status)
        except HTTPError as error:
            if error.code in {405, 403}:
                try:
                    status, final_url, _ = request_url(url, "GET")
                    if status and 200 <= status < 400:
                        detail = f"{status} after GET fallback"
                        if final_url.rstrip("/") != url.rstrip("/"):
                            detail = f"redirect to {final_url}"
                        return "ok", detail
                except HTTPError as get_error:
                    if get_error.code in {401, 403}:
                        return "access_limited", str(get_error.code)
                    last_error = str(get_error.code)
                except URLError as get_error:
                    last_error = str(get_error.reason)
            elif error.code in {401, 429}:
                return "access_limited", str(error.code)
            else:
                last_error = str(error.code)
        except URLError as error:
            last_error = str(error.reason)
        if attempt < retries:
            time.sleep(1.0 + attempt)
    return "broken", last_error


def valid_shape(url: str) -> bool:
    parsed = urlsplit(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def evaluate_urls(
    urls: list[str],
    *,
    live: bool,
    retries: int = 1,
    root: Path = ROOT,
    http_checker: Callable[[str, int], tuple[str, str]] | None = None,
) -> tuple[list[str], list[str], list[str], int]:
    """Return malformed, broken, warnings, and checked count."""
    checker = http_checker or check_url
    malformed = [url for url in urls if not valid_shape(url)]
    broken: list[str] = []
    warnings: list[str] = []
    checked = 0
    if not live:
        return malformed, broken, warnings, checked

    tracked = tracked_repository_paths(root)
    for url in urls:
        local = classify_own_repo_main_blob(url, root=root, tracked_paths=tracked)
        if local.status == "valid_tracked_target":
            checked += 1
            warnings.append(
                "same_repo_main_local_target: "
                f"{url} -> verified against tracked Git path {local.relative_path}"
            )
            continue
        if local.status != "not_applicable":
            checked += 1
            detail = local.detail or local.status
            broken.append(
                f"{url} -> same-repo blob/main {local.status}" + (f" ({detail})" if detail else "")
            )
            continue
        status, detail = checker(url, retries)
        checked += 1
        if status == "broken":
            broken.append(f"{url} -> {detail}")
        elif status in {"access_limited", "redirect"}:
            warnings.append(f"{status}: {url} -> {detail}")
    return malformed, broken, warnings, checked


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--retries", type=int, default=1)
    args = parser.parse_args()
    urls = collect_urls()
    malformed, broken, warnings, checked = evaluate_urls(
        urls,
        live=args.live,
        retries=args.retries,
    )
    if malformed or broken:
        print("External link check failed")
        for url in malformed:
            print(f"- malformed: {url}")
        for item in broken:
            print(f"- broken: {item}")
        for item in warnings:
            print(f"- warning: {item}")
        return 1
    mode = "live" if args.live else "syntax"
    print(
        f"External link check passed: {len(urls)} URLs, mode={mode}, "
        f"checked={checked}, warnings={len(warnings)}"
    )
    for item in warnings:
        print(f"warning: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
