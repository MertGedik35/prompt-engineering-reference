from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:"))


def strip_anchor(target: str) -> str:
    return target.split("#", 1)[0]


def markdown_files() -> list[Path]:
    ignored = {".git", ".venv", "site"}
    return [
        path
        for path in ROOT.rglob("*.md")
        if not any(part in ignored for part in path.relative_to(ROOT).parts)
    ]


def check_links() -> list[str]:
    errors: list[str] = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = unquote(strip_anchor(match.group(1)).strip())
            if not target or is_external(target):
                continue
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(ROOT)
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)} links outside repository: {target}")
                continue
            if not candidate.exists():
                errors.append(f"{path.relative_to(ROOT)} missing link target: {target}")
    return errors


def main() -> int:
    errors = check_links()
    if errors:
        print("Internal link check failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Internal link check passed: {len(markdown_files())} markdown files scanned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
