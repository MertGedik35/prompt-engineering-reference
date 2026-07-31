from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import pytest

from scripts.check_freshness import check, main, parse_as_of

AS_OF = date(2026, 7, 31)
CATALOG_PATH = "catalog/fixture.json"


def write_records(root: Path, records: list[dict[str, object]]) -> None:
    catalog = root / "catalog"
    catalog.mkdir()
    (catalog / "fixture.json").write_text(
        json.dumps(records),
        encoding="utf-8",
        newline="\n",
    )


def record(
    *,
    last_verified: str = "2026-07-21",
    stale_after_days: int = 10,
    stale_risk: str = "high",
) -> dict[str, object]:
    return {
        "id": "fixture",
        "last_verified": last_verified,
        "stale_after_days": stale_after_days,
        "stale_risk": stale_risk,
    }


def findings(
    tmp_path: Path,
    records: list[dict[str, object]],
) -> tuple[list[str], list[str]]:
    write_records(tmp_path, records)
    return check(AS_OF, root=tmp_path, files=(CATALOG_PATH,))


def test_exact_boundary_day_is_not_stale(tmp_path: Path) -> None:
    assert findings(tmp_path, [record()]) == ([], [])


def test_one_day_past_boundary_is_stale(tmp_path: Path) -> None:
    _, failures = findings(tmp_path, [record(last_verified="2026-07-20")])
    assert len(failures) == 1
    assert "stale by 1 days" in failures[0]


def test_high_risk_stale_record_is_failure(tmp_path: Path) -> None:
    warnings, failures = findings(tmp_path, [record(last_verified="2026-07-01")])
    assert warnings == []
    assert len(failures) == 1


@pytest.mark.parametrize("risk", ["medium", "low"])
def test_lower_risk_stale_record_is_warning(tmp_path: Path, risk: str) -> None:
    warnings, failures = findings(
        tmp_path,
        [record(last_verified="2026-07-01", stale_risk=risk)],
    )
    assert len(warnings) == 1
    assert failures == []


def test_future_verification_date_is_failure(tmp_path: Path) -> None:
    _, failures = findings(tmp_path, [record(last_verified="2026-08-01")])
    assert "is after as-of 2026-07-31" in failures[0]


def test_invalid_iso_date_is_failure(tmp_path: Path) -> None:
    _, failures = findings(tmp_path, [record(last_verified="2026-02-30")])
    assert "invalid last_verified" in failures[0]


@pytest.mark.parametrize(
    ("missing_field", "expected"),
    [
        ("last_verified", "last_verified"),
        ("stale_after_days", "stale_after_days"),
        ("stale_risk", "stale_risk"),
    ],
)
def test_missing_freshness_field_is_failure(
    tmp_path: Path,
    missing_field: str,
    expected: str,
) -> None:
    value = record()
    del value[missing_field]
    _, failures = findings(tmp_path, [value])
    assert expected in failures[0]


@pytest.mark.parametrize("days", [0, -1])
def test_non_positive_stale_period_is_failure(tmp_path: Path, days: int) -> None:
    _, failures = findings(tmp_path, [record(stale_after_days=days)])
    assert "positive integer" in failures[0]


def test_unknown_risk_is_failure(tmp_path: Path) -> None:
    _, failures = findings(tmp_path, [record(stale_risk="urgent")])
    assert "unknown stale_risk" in failures[0]


def test_as_of_parser_accepts_iso_date() -> None:
    assert parse_as_of("2026-07-31") == AS_OF


def test_as_of_parser_rejects_invalid_date() -> None:
    with pytest.raises(argparse.ArgumentTypeError, match="expected YYYY-MM-DD"):
        parse_as_of("31-07-2026")


def test_cli_as_of_controls_age_calculation(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write_records(tmp_path, [record()])
    exit_code = main(["--as-of", "2026-07-31"], root=tmp_path, files=(CATALOG_PATH,))
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "as-of: 2026-07-31" in output


def test_warn_only_preserves_findings_but_changes_exit(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    write_records(tmp_path, [record(last_verified="2026-07-01")])
    assert (
        main(
            ["--as-of", "2026-07-31"],
            root=tmp_path,
            files=(CATALOG_PATH,),
        )
        == 1
    )
    normal_output = capsys.readouterr().out
    assert (
        main(
            ["--as-of", "2026-07-31", "--warn-only"],
            root=tmp_path,
            files=(CATALOG_PATH,),
        )
        == 0
    )
    warn_only_output = capsys.readouterr().out
    assert normal_output == warn_only_output
    assert "FAIL catalog/fixture.json:fixture" in warn_only_output


def test_report_contains_same_findings_as_terminal(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    write_records(tmp_path, [record(last_verified="2026-07-01")])
    report_path = tmp_path / "freshness.txt"
    exit_code = main(
        ["--as-of", "2026-07-31", "--report", str(report_path)],
        root=tmp_path,
        files=(CATALOG_PATH,),
    )
    assert exit_code == 1
    assert report_path.read_text(encoding="utf-8") == capsys.readouterr().out
