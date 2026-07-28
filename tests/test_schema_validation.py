from __future__ import annotations

from scripts.validate_schemas import validate_all


def test_schema_validation_passes() -> None:
    _, errors = validate_all()
    assert errors == []


def test_schema_catalog_counts_are_nonzero() -> None:
    counts, _ = validate_all()
    assert all(count > 0 for count in counts.values())
