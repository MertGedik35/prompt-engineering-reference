PYTHON ?= python

.PHONY: install validate schemas quality privacy freshness links test docs format lint type check

install:
	$(PYTHON) -m pip install -e ".[dev,docs]"

schemas:
	$(PYTHON) scripts/validate_schemas.py

validate: schemas
	$(PYTHON) scripts/validate_catalog.py
	$(PYTHON) scripts/check_content_quality.py
	$(PYTHON) scripts/audit_privacy.py --include-site --include-git --history-warn-only
	$(PYTHON) scripts/check_freshness.py
	$(PYTHON) scripts/generate_docs_indexes.py --check
	$(PYTHON) scripts/check_internal_links.py
	$(PYTHON) scripts/check_readme_navigation.py

privacy:
	$(PYTHON) scripts/audit_privacy.py --include-site --include-git --history-warn-only

freshness:
	$(PYTHON) scripts/check_freshness.py

links:
	$(PYTHON) scripts/check_external_links.py --live --retries 2

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

quality: validate format lint type test docs

check: quality
