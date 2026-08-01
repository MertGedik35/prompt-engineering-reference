# V1 to V2 Migration

V1 catalog IDs are preserved where the underlying concept remained useful. Shallow templates were replaced with task-specific records and may not keep every old title.

## Mapping Rules

- Pattern IDs remain stable when the mechanism stayed the same.
- Template IDs changed when the old record differed only by title.
- `catalog/resources.json` was replaced by typed resource catalogs such as `official-resources.json`, `courses.json`, and `credentials.json`.
- Provider records now use `catalog/provider-guides.json`.

Review any integration that read `catalog/resources.json` directly.

## V1 site route replacements (redirect backlog)

The Version 2 documentation tree replaces several V1 HTML routes. Clear destinations exist, but
static HTML redirects are intentional backlog and are not required for publication.

| Former V1 route | Current destination |
| --- | --- |
| `patterns/` | `generated/pattern-index/` |
| `templates/` | `generated/template-index/` |
| `prompt-doctor/` | `generated/prompt-doctor-index/` |
| `providers/amazon-bedrock/` | `providers/aws/` |
| `providers/azure-openai/` | `providers/microsoft/` |
| `providers/gemini/` | `providers/google/` |
| `providers/llama/` | `providers/meta/` |
| `security/` | `learn/security/` and `reference/security-checklist/` |
| `evaluations/` | `labs/evaluations/` |
| `context-engineering/` | `learn/context-engineering/` |
| `prompt-contract/` | `learn/prompt-anatomy/` |
| `contributing/` | `contribute/` |
| `generated/resource-index/` | Typed generated indexes under `generated/` |
| `research-positioning/` | Removed intentionally |
