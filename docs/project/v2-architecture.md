# V2 Architecture

V2 separates Learning mode from Reference mode.

## Source of Truth

- `catalog/*.json`: structured records and machine-readable metadata.
- `curriculum/<module>/README.md`: authoritative lesson content.
- `curriculum/<module>/{exercise,quiz,references,checklist}.md`: authoritative activities.
- `labs/solutions/<module>.md`: authoritative explained solutions and answer keys.
- `docs/learn/*.md`: concise MkDocs navigation entries that link to curriculum sources. They are
  deliberately not second lesson copies.
- `reference/**`: reference source files for GitHub browsing.
- `docs/generated/*.md`: generated indexes. Do not edit manually.

## Major Areas

- Curriculum: 13 modules from orientation through capstone.
- Reference: patterns, templates, Prompt Doctor, checklists, glossary, and decision guides.
- Provider hub: dated provider guides with official source IDs and stale-risk areas.
- Resources: official docs, prompt resources, repositories, courses, credentials, videos, papers, books, tools, and communities.
- Labs: exercises, quizzes, solutions, evaluations, datasets, and capstones.

The design favors fewer substantive records over high counts with repeated text.

## Curriculum drift prevention

Lesson changes belong in `curriculum/**`. The semantic quality checker enforces the authoritative
lesson headings, depth, distinct examples, exercises, quiz questions, references, and explanatory
solutions. Site entries under `docs/learn/` state that they are navigational; reviewers should
reject substantive lesson prose added there because it would create two independently maintained
copies.
