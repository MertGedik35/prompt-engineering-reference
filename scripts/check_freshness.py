from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FILES = (
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
)
STALE_RISKS = frozenset({"low", "medium", "high"})


def utc_today() -> date:
    """Return the current calendar date in UTC."""
    return datetime.now(UTC).date()


def parse_as_of(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"invalid --as-of date {value!r}; expected YYYY-MM-DD"
        ) from error


def load(path: str, root: Path = ROOT) -> list[dict[str, Any]]:
    data = json.loads((root / path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise TypeError(f"{path} must contain a list")
    return [record for record in data if isinstance(record, dict)]


def _age_findings(
    *,
    location: str,
    last_verified: date,
    stale_after: int,
    risk: str,
    as_of: date,
) -> tuple[list[str], list[str]]:
    age = (as_of - last_verified).days
    if age <= stale_after:
        return [], []
    message = (
        f"{location} stale by {age - stale_after} days "
        f"(age={age}, limit={stale_after}, risk={risk})"
    )
    if risk == "high":
        return [], [message]
    return [message], []


def _record_freshness(
    file: str,
    record: dict[str, Any],
    as_of: date,
) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    failures: list[str] = []
    record_id = record.get("id", "<missing-id>")
    missing = [
        field
        for field in ("last_verified", "stale_after_days", "stale_risk")
        if field not in record or record[field] in (None, "")
    ]
    if missing:
        failures.append(f"{file}:{record_id} missing freshness fields: {', '.join(missing)}")
        return warnings, failures

    last_verified_value = record["last_verified"]
    try:
        last_verified = date.fromisoformat(str(last_verified_value))
    except ValueError:
        failures.append(
            f"{file}:{record_id} invalid last_verified {last_verified_value!r}; expected YYYY-MM-DD"
        )
        return warnings, failures

    stale_after = record["stale_after_days"]
    if isinstance(stale_after, bool) or not isinstance(stale_after, int) or stale_after <= 0:
        failures.append(
            f"{file}:{record_id} stale_after_days must be a positive integer; got {stale_after!r}"
        )
        return warnings, failures

    risk = record["stale_risk"]
    if risk not in STALE_RISKS:
        failures.append(
            f"{file}:{record_id} unknown stale_risk {risk!r}; expected one of {sorted(STALE_RISKS)}"
        )
        return warnings, failures

    if last_verified > as_of:
        failures.append(
            f"{file}:{record_id} last_verified {last_verified.isoformat()} "
            f"is after as-of {as_of.isoformat()}"
        )
        return warnings, failures

    parent_warnings, parent_failures = _age_findings(
        location=f"{file}:{record_id}",
        last_verified=last_verified,
        stale_after=stale_after,
        risk=str(risk),
        as_of=as_of,
    )
    warnings.extend(parent_warnings)
    failures.extend(parent_failures)

    claims = record.get("fast_stale_areas")
    if not isinstance(claims, list):
        return warnings, failures

    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            failures.append(f"{file}:{record_id} fast_stale_areas[{index}] must be an object")
            continue
        source_id = claim.get("source_id", "<missing-source>")
        location = f"{file}:{record_id} fast_stale_areas[{index}] (source_id={source_id})"
        child_value = claim.get("last_verified")
        if child_value in (None, ""):
            failures.append(f"{location} missing last_verified")
            continue
        try:
            child_verified = date.fromisoformat(str(child_value))
        except ValueError:
            failures.append(
                f"{location} invalid last_verified {child_value!r}; expected YYYY-MM-DD"
            )
            continue
        if child_verified > as_of:
            failures.append(
                f"{location} last_verified {child_verified.isoformat()} "
                f"is after as-of {as_of.isoformat()}"
            )
            continue
        if child_verified > last_verified:
            failures.append(
                f"{location} last_verified {child_verified.isoformat()} "
                f"is after parent last_verified {last_verified.isoformat()}"
            )
            continue
        child_warnings, child_failures = _age_findings(
            location=location,
            last_verified=child_verified,
            stale_after=stale_after,
            risk=str(risk),
            as_of=as_of,
        )
        warnings.extend(child_warnings)
        failures.extend(child_failures)
    return warnings, failures


def check(
    as_of: date | None = None,
    *,
    root: Path = ROOT,
    files: Sequence[str] = FILES,
) -> tuple[list[str], list[str]]:
    effective_date = as_of or utc_today()
    warnings: list[str] = []
    failures: list[str] = []
    for file in files:
        for record in load(file, root):
            record_warnings, record_failures = _record_freshness(file, record, effective_date)
            warnings.extend(record_warnings)
            failures.extend(record_failures)
    return warnings, failures


def render_report(as_of: date, warnings: Sequence[str], failures: Sequence[str]) -> str:
    lines = [
        "Freshness check",
        f"as-of: {as_of.isoformat()}",
        f"warnings: {len(warnings)}",
        f"failures: {len(failures)}",
    ]
    lines.extend(f"WARN {item}" for item in warnings)
    lines.extend(f"FAIL {item}" for item in failures)
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--as-of",
        type=parse_as_of,
        help="evaluate record age on this UTC calendar date (YYYY-MM-DD)",
    )
    parser.add_argument("--warn-only", action="store_true")
    parser.add_argument("--report", type=Path)
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    root: Path = ROOT,
    files: Sequence[str] = FILES,
) -> int:
    args = build_parser().parse_args(argv)
    as_of = args.as_of or utc_today()
    warnings, failures = check(as_of, root=root, files=files)
    output = render_report(as_of, warnings, failures)
    if args.report:
        args.report.write_text(output, encoding="utf-8", newline="\n")
    print(output, end="")
    return 0 if args.warn_only or not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
