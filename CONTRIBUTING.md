# Contributing

Contributions are welcome when they improve learning quality, reference usefulness, validation strength, or safety.

## Contribution Flows

- Lesson or exercise: include objectives, examples, rubric, solution criteria, and references.
- Pattern: explain a distinct mechanism, not only a label.
- Template: provide a task-specific copyable prompt with variables, required inputs, expected outputs, acceptance criteria, and failure modes.
- Official resource, course, credential, video, paper, repository, or tool: provide canonical URL, original description, verification date, pricing classification, credential classification, and maintenance evidence.
- Broken link, provider update, privacy report, or security report: include location, evidence, and safe reproduction steps.

## Required Confirmation

Contributors must confirm that descriptions are original, content is not copied from paid materials or proprietary prompt packs, and no affiliate or referral links are included.

## Rejected Content

Resource dumps, SEO pages, unsupported superlatives, duplicate entries, dead projects, leaked prompts, jailbreak collections, copied course material, and generated filler will be declined.

## Checks

Run:

```bash
python scripts/validate_catalog.py
python scripts/check_content_quality.py
python scripts/audit_privacy.py --include-site --history-warn-only
python scripts/generate_docs_indexes.py --check
python -m pytest
```
