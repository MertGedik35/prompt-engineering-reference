# V2 Architecture

V2 separates Learning mode from Reference mode.

## Source of Truth

- `catalog/*.json`: structured records and machine-readable metadata.
- `curriculum/**`: learning module source files for GitHub browsing.
- `reference/**`: reference source files for GitHub browsing.
- `docs/generated/*.md`: generated indexes. Do not edit manually.

## Major Areas

- Curriculum: 13 modules from orientation through capstone.
- Reference: patterns, templates, Prompt Doctor, checklists, glossary, and decision guides.
- Provider hub: dated provider guides with official source IDs and stale-risk areas.
- Resources: official docs, prompt resources, repositories, courses, credentials, videos, papers, books, tools, and communities.
- Labs: exercises, quizzes, solutions, evaluations, datasets, and capstones.

The design favors fewer substantive records over high counts with repeated text.
