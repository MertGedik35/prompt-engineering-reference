# Rebuild Prompt Engineering Reference As A Learning And Reference Platform

## Problem

The v1 repository shipped useful scaffolding, but the main catalogs were too shallow to support the public promise of a learning and daily-reference platform. Template, pattern, and prompt-contract records repeated large blocks of content, provider pages were thin, and validation did not execute JSON Schema.

## Current V1 Limitations

- `catalog/templates.json` had 49 template records but only one repeated variables, input, output, acceptance, and failure-mode structure.
- `catalog/patterns.json` had 26 records with repeated use/avoid/verification blocks.
- `catalog/prompt_contracts.json` had six contract variants in one structural duplicate group.
- Provider pages were short and not provider-aware enough for real reference use.
- Existing tests did not catch shallow content, duplicate blocks, privacy risk, freshness drift, or schema execution gaps.

## New Information Architecture

- Learning source: `curriculum/**` and `docs/learn/**`.
- Reference source: `reference/**` and `catalog/*.json`.
- Provider hub: `providers/**`, `docs/providers/**`, and `catalog/provider-guides.json`.
- Resource catalogs: typed JSON files for official resources, repositories, courses, credentials, videos, papers, books, tools, and communities.
- Generated docs: `docs/generated/*.md` are regenerated from catalog JSON and marked as generated.

## Curriculum

Adds 13 modules covering orientation, LLM foundations, prompt anatomy, core techniques, grounding and long context, structured outputs, evaluation, agents and tools, context engineering, security, multimodal prompting, production operations, and portfolio/capstone work.

Each module has an introduction, exercise, quiz, checklist, references, and separate solution criteria.

## Pattern And Template Rewrite

- Rebuilt 26 prompt patterns around distinct mechanisms.
- Rebuilt 28 task-specific templates with copyable prompts, variables, required inputs, expected outputs, acceptance criteria, and failure modes.
- Added 8 copyable Prompt Contract variants.
- Added 16 Prompt Doctor diagnostic entries.

## Official Resource Hub

Adds typed catalogs for:

- 21 official resources.
- 10 repositories.
- 7 courses.
- 5 credentials.
- 4 videos.
- 8 papers.
- 2 books or long-form guides.
- 5 tools.
- 3 communities.

## Course And Credential Classifications

Courses include pricing classifications: free, paid, lab credits. Credentials are classified separately as formal certification, applied skill badge, skill badge, course completion certificate, or no credential. Course-completion certificates are not treated as formal certifications.

## Privacy Audit

The repository permits `Mert Gedik` and `MertGedik35`. Current tracked files and generated documentation pages have no unapproved personal-data findings. Git history still contains a redacted personal email in one historical commit's author/committer metadata. Future commits use the GitHub noreply address; no history rewrite was performed.

## Validation Changes

- Added real JSON Schema validation with `jsonschema`.
- Added catalog integrity checks for duplicate IDs, duplicate canonical URLs, broken references, date fields, and banned markers.
- Added content similarity checks for repeated prompt/template/pattern blocks.
- Added privacy and freshness scanners.
- Preserved internal and external link checks with live retry behavior.

## Test Results

- `python scripts/validate_catalog.py`: pass, 0 errors.
- `python scripts/validate_schemas.py`: pass.
- `python scripts/check_content_quality.py`: pass, 0 duplicate/high-similarity failures.
- `python scripts/audit_privacy.py`: pass, 0 current-tree findings.
- `python scripts/check_freshness.py`: pass, 0 warnings, 0 failures.
- `python scripts/check_internal_links.py`: pass, 171 Markdown files scanned.
- `python scripts/check_external_links.py --live --retries 2`: pass, 71 URLs checked, 0 warnings.
- `python -m pytest`: pass, 32 tests.
- `python -m mkdocs build --strict`: pass.
- `detect-secrets`: pass, 0 findings in scoped repository/build scan.

## Known Limitations

- Local Windows environment does not have `make`; GitHub Actions Quality on Ubuntu passed `make check` for this branch.
- No live cross-model prompt benchmarks were run for provider-specific behavior.
- Historical commit metadata still contains a redacted personal email until a separately authorized history rewrite is performed.
- Independent content review is still required before any `v2.0.0` tag or release.

## Review Checklist

- Review curriculum module quality and navigation.
- Review provider guide source coverage and stale-risk labels.
- Review resource classifications, especially paid/lab-credit/course-completion distinctions.
- Review schema and content-quality thresholds.
- Review privacy audit conclusions and history-remediation notes.
- Confirm GitHub Actions Quality remains green after review changes.

## Release Gates Not Yet Completed

- Independent content review.
- Explicit maintainer approval to tag and publish `v2.0.0`.

This PR must remain draft until those gates are satisfied. It must not be merged or released in this run.
