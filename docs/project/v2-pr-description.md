# Rebuild Prompt Engineering Reference As A Learning And Reference Platform

## Status

This pull request remains a draft. It is not ready to merge or release.

## Implemented foundation

- Learning and Reference modes have separate source areas.
- Catalogs use JSON Schema and integrity validation.
- Privacy, freshness, internal-link, external-link, and documentation checks exist.
- Generated catalog indexes remain derived from `catalog/*.json`.

## Curriculum Remediation Phase 1

All 13 curriculum modules now have:

- an authoritative lesson under `curriculum/<module>/README.md`;
- module-specific minimal, production, bad, and worked examples;
- a 20–45 minute exercise with normal, edge, and failure or adversarial cases;
- an eight-question module-specific quiz;
- an explanatory solution and answer key;
- relevant references and an outcome-based completion checklist.

The `docs/learn/*.md` pages are navigation entries rather than independently maintained lesson
copies. Markdown-aware semantic validation enforces lesson depth, required headings, distinct
examples, exercise structure, quiz question counts, explained solutions, and deterministic
similarity limits. Deliberately shallow test fixtures demonstrate that these checks fail for the
previous content shape.

## Work deliberately not claimed complete

The current pattern, template, provider-guide, course, and credential catalogs still require later
semantic remediation and independent verification. Earlier statements that those areas were fully
rebuilt were too broad and are withdrawn. Broader resource expansion and live cross-model
benchmarks have not been performed.

## Verification

- Catalog and JSON Schema validation pass.
- Curriculum semantic validation passes for 13 lessons, exercises, quizzes, and solutions.
- The test suite contains 45 passing tests.
- Internal-link validation and MkDocs strict build pass.
- Current-tree privacy and secret checks have no active findings.

Final-head GitHub Actions results must be confirmed after the latest push.

## Review gates

- Independent human review of all 13 curriculum packages remains required.
- Pattern and Template Remediation is the next implementation phase.
- Provider guides, courses, and credentials remain later phases.
- No `v2.0.0` tag, release, merge, or ready-for-review transition is authorized.
