# Repository Instructions

This repository treats `catalog/` JSON files as source of truth. Update generated
documentation with `python scripts/generate_docs_indexes.py` after changing catalog
records.

Before completing work, run:

```bash
python scripts/validate_catalog.py
python scripts/generate_docs_indexes.py --check
python scripts/check_internal_links.py
python -m pytest
python -m mkdocs build --strict
```

Keep examples factual, provider guidance dated, and external resource summaries
original. Do not add jailbreak collections, leaked proprietary prompts, secrets, or
instructions that encourage bypassing safety systems.
