# Contributing

Contributions should improve practical prompt design, evaluation, provider guidance,
context engineering, or safety. Prefer small pull requests with one clear purpose.

## Requirements

- Add or update catalog records in `catalog/`.
- Include acceptance criteria, failure modes, version data, and review dates.
- Regenerate documentation indexes.
- Run local validation before opening a pull request.

## Local checks

```bash
python scripts/validate_catalog.py
python scripts/generate_docs_indexes.py --check
python scripts/check_internal_links.py
python -m pytest
python -m mkdocs build --strict
```
