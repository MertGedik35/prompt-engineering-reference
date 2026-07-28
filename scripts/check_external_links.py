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


def catalog_urls() -> set[str]:
    data = json.loads((ROOT / "catalog/resources.json").read_text(encoding="utf-8"))
    return {str(record["canonical_url"]) for record in data}


def markdown_urls() -> set[str]:
    urls: set[str] = set()
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", ".venv", "site"} for part in path.relative_to(ROOT).parts):
            continue
        urls.update(URL_RE.findall(path.read_text(encoding="utf-8")))
    return urls


def collect_urls() -> list[str]:
    return sorted(catalog_urls() | markdown_urls())


def check_url(url: str, retries: int) -> tuple[bool, str]:
    request = Request(url, headers={"User-Agent": "PromptEngineeringReferenceLinkCheck/1.0"})
    context = ssl.create_default_context()
    last_error = ""
    for attempt in range(retries + 1):
        try:
            with urlopen(request, timeout=20, context=context) as response:
                status = response.getcode()
                if 200 <= status < 400 or status in {401, 403}:
                    return True, str(status)
                last_error = str(status)
        except HTTPError as error:
            if error.code in {401, 403, 429}:
                return True, str(error.code)
            last_error = f"{error.code}"
        except URLError as error:
            last_error = str(error.reason)
        if attempt < retries:
            time.sleep(1.0)
    return False, last_error


def validate_url_shape(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--retries", type=int, default=1)
    args = parser.parse_args()
    urls = collect_urls()
    malformed = [url for url in urls if not validate_url_shape(url)]
    broken: list[str] = []
    checked = 0
    if args.live:
        for url in urls:
            ok, detail = check_url(url, retries=args.retries)
            checked += 1
            if not ok:
                broken.append(f"{url} -> {detail}")
    if malformed or broken:
        print("External link check failed")
        for url in malformed:
            print(f"- malformed: {url}")
        for url in broken:
            print(f"- broken: {url}")
        return 1
    mode = "live" if args.live else "syntax"
    print(f"External link check passed: {len(urls)} URLs, mode={mode}, checked={checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
