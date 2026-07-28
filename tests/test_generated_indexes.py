from __future__ import annotations

from scripts.generate_docs_indexes import write_outputs


def test_generated_indexes_are_current() -> None:
    assert write_outputs(check=True) == []
