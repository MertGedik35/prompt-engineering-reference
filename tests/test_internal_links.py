from __future__ import annotations

from scripts.check_internal_links import check_links


def test_internal_links_pass() -> None:
    assert check_links() == []
