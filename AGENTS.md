# Repository Instructions

## Mission

Prompt Engineering Reference is a learning platform and daily reference. Preserve the split between Learning mode and Reference mode.

## Source of Truth

- Catalog source files: `catalog/*.json`.
- Authoritative curriculum lessons and activities: `curriculum/<module>/**`.
- `docs/learn/*.md` files are navigation-only site entries. Do not duplicate or independently
  rewrite lesson content there.
- Reference source pages: `reference/**`.
- Generated site indexes: `docs/generated/*.md`. Do not edit generated files manually.

## Required Commands

```bash
python scripts/validate_schemas.py
python scripts/validate_catalog.py
python scripts/check_content_quality.py
python scripts/audit_privacy.py --include-site --include-git --history-warn-only
python scripts/check_freshness.py
python scripts/generate_docs_indexes.py --check
python scripts/check_internal_links.py
python scripts/check_readme_navigation.py
python -m ruff format --check .
python -m ruff check .
python -m mypy scripts tests
python -m pytest
python -m mkdocs build --strict
```

## Content Rules

Never invent links, prices, certification status, official status, or command results. Never create filler to meet counts. Never reuse one generic prompt across unrelated templates. Never add jailbreak collections, leaked prompts, affiliate links, referral links, or copied paid materials.

## Privacy and Security

`Mert Gedik` and `MertGedik35` may remain. Personal contact details, addresses, bank data, identity numbers, credentials, tokens, cookies, and private local paths must not be added. Run `scripts/audit_privacy.py` before completion.

## Licensing

Code and automation are MIT. Original docs, taxonomies, patterns, and templates are CC0-1.0. External resources retain upstream licenses.

## Generated Docs

Update generated files with:

```bash
python scripts/generate_docs_indexes.py
```

If generated-index drift appears, update the source catalog first, regenerate, and rerun checks.

## Completion Rules

Do not weaken validation, delete failing tests, rewrite public history, publish a release, or merge without explicit authorization.
