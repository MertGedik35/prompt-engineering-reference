PYTHON ?= python

    .PHONY: install validate test docs check format lint type

    install:
	$(PYTHON) -m pip install -e ".[dev,docs]"

    validate:
	$(PYTHON) scripts/validate_catalog.py
	$(PYTHON) scripts/generate_docs_indexes.py --check
	$(PYTHON) scripts/check_internal_links.py

    test:
	$(PYTHON) -m pytest

    docs:
	$(PYTHON) -m mkdocs build --strict

    format:
	$(PYTHON) -m ruff format --check .

    lint:
	$(PYTHON) -m ruff check .

    type:
	$(PYTHON) -m mypy scripts tests

    check: validate format lint type test docs
