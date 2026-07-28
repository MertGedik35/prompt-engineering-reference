from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TODAY = date(2026, 7, 28)
FILES = [
    "catalog/official-resources.json",
    "catalog/repositories.json",
    "catalog/courses.json",
    "catalog/credentials.json",
    "catalog/videos.json",
    "catalog/papers.json",
    "catalog/books.json",
    "catalog/tools.json",
    "catalog/communities.json",
    "catalog/provider-guides.json",
]


def load(path: str) -> list[dict[str, Any]]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def check() -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    failures: list[str] = []
    for file in FILES:
        for record in load(file):
            last_verified = record.get("last_verified")
            stale_after = record.get("stale_after_days")
            risk = record.get("stale_risk")
            if not last_verified or not stale_after or not risk:
                failures.append(f"{file}:{record.get('id')} missing freshness fields")
                continue
            age = (TODAY - date.fromisoformat(str(last_verified))).days
            if age > int(stale_after):
                message = f"{file}:{record['id']} stale by {age - int(stale_after)} days ({risk})"
                if risk == "high":
                    failures.append(message)
                else:
                    warnings.append(message)
    return warnings, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warn-only", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    warnings, failures = check()
    lines = ["Freshness check", f"warnings: {len(warnings)}", f"failures: {len(failures)}"]
    lines.extend(f"WARN {item}" for item in warnings)
    lines.extend(f"FAIL {item}" for item in failures)
    output = "\n".join(lines) + "\n"
    if args.report:
        args.report.write_text(output, encoding="utf-8", newline="\n")
    print(output, end="")
    return 0 if args.warn_only or not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
