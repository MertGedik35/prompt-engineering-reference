from __future__ import annotations

import argparse
import json
import re
import ssl
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
URL_RE = re.compile(r"https?://[^\s)\]>]+")
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


def catalog_urls() -> set[str]:
    urls: set[str] = set()
    for file in CATALOGS:
        data = json.loads((ROOT / file).read_text(encoding="utf-8"))
        urls.update(str(record["canonical_url"]) for record in data if "canonical_url" in record)
    return urls


def markdown_urls() -> set[str]:
    urls: set[str] = set()
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", ".venv", "site"} for part in path.relative_to(ROOT).parts):
            continue
        urls.update(URL_RE.findall(path.read_text(encoding="utf-8")))
    return urls


def collect_urls() -> list[str]:
    return sorted(catalog_urls() | markdown_urls())


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
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--retries", type=int, default=1)
    args = parser.parse_args()
    malformed = [url for url in collect_urls() if not valid_shape(url)]
    broken: list[str] = []
    warnings: list[str] = []
    checked = 0
    if args.live:
        for url in collect_urls():
            status, detail = check_url(url, args.retries)
            checked += 1
            if status == "broken":
                broken.append(f"{url} -> {detail}")
            elif status in {"access_limited", "redirect"}:
                warnings.append(f"{status}: {url} -> {detail}")
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
        f"External link check passed: {len(collect_urls())} URLs, mode={mode}, "
        f"checked={checked}, warnings={len(warnings)}"
    )
    for item in warnings:
        print(f"warning: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
