# V1 Content Audit

Date: 2026-07-28

## Verified Findings

| Finding | File | Affected records | Evidence | Severity | Required remediation | Blocks v2.0.0 |
| --- | --- | --- | --- | --- | --- | --- |
| Template blocks were repeated | `catalog/templates.json` | 49 | Field-level check found 1 unique variables block, 1 unique required-inputs block, 1 unique expected-output block, 1 unique acceptance block, and 1 unique failure-mode block across 49 templates. | HIGH | Replace with task-specific templates. | Yes |
| Pattern blocks were repeated | `catalog/patterns.json` | 26 | Field-level check found 1 unique `use_when`, `avoid_when`, acceptance, failure-mode, and verification block across 26 patterns. | HIGH | Rewrite patterns around distinct mechanisms. | Yes |
| Prompt Contract variants were structurally duplicated | `catalog/prompt_contracts.json` | 6 | Hash check over dimensions and acceptance criteria found all six variants in one duplicate group. | HIGH | Add genuinely different copyable prompt structures. | Yes |
| Provider pages were too short | `docs/providers/*.md` | 7 provider pages | Each provider page had 12 lines and only brief summary plus source links. | MEDIUM | Expand dated provider guidance with official sources and stale-risk notes. | Yes |
| JSON Schema files were not executed by a real validator | `scripts/validate_catalog.py`, `schemas/*.json` | All schemas | No `jsonschema` dependency or Draft202012Validator execution existed. | HIGH | Add real JSON Schema validation. | Yes |
| Schemas were permissive | `schemas/*.json` | 7 schemas | Required content-quality fields were absent or shallow. | HIGH | Strengthen required fields and enums. | Yes |
| Makefile indentation was suspicious | `Makefile` | All targets | Targets were indented with spaces before target names; local `make` executable was unavailable, so execution could not be verified locally. | MEDIUM | Normalize Makefile and verify in CI. | Yes |
| Tests were insufficient | `tests/*.py` | 3 tests | Tests did not detect field-level duplication, schema execution gaps, privacy, freshness, or semantic similarity. | HIGH | Add meaningful quality gates. | Yes |
| Count claims overstated unique substance | `catalog/*.json` | Patterns and templates | Numeric counts passed while repeated blocks made many records shallow. | HIGH | Prefer fewer substantive records over filler. | Yes |
| v1.0.0 should not be promoted broadly | GitHub release | `v1.0.0` | Release exists, but v1 quality defects above were verified. | MEDIUM | Keep v1 unchanged; prepare v2 through review PR. | No |
