from __future__ import annotations

from scripts.validate_catalog import validate


def test_catalog_validation_passes() -> None:
    summary, errors = validate()
    assert errors == []
    assert summary["patterns"] >= 24
    assert summary["templates"] >= 40
    assert 75 <= summary["resources"] <= 120
    assert summary["evaluations"] >= 3
