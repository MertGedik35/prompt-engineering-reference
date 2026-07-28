# V1 to V2 Migration

V1 catalog IDs are preserved where the underlying concept remained useful. Shallow templates were replaced with task-specific records and may not keep every old title.

## Mapping Rules

- Pattern IDs remain stable when the mechanism stayed the same.
- Template IDs changed when the old record differed only by title.
- `catalog/resources.json` was replaced by typed resource catalogs such as `official-resources.json`, `courses.json`, and `credentials.json`.
- Provider records now use `catalog/provider-guides.json`.

Review any integration that read `catalog/resources.json` directly.
