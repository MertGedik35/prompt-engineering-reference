# Privacy Audit

Date: 2026-07-28

Permitted maintainer identifiers: `Mert Gedik`, `MertGedik35`.

## Scope

Scanned current tracked files, generated documentation output, Git metadata, GitHub issues, release notes, and Pages URL metadata. The privacy script redacts sensitive values in output and skips only generated third-party MkDocs theme JavaScript/CSS assets.

## Findings

| Category | Current tree | Historical or remote | Action |
| --- | ---: | ---: | --- |
| Personal names | 1 permitted maintainer name | 1 permitted maintainer name | Allowed |
| GitHub username | 1 permitted username | 1 permitted username | Allowed |
| Personal email addresses | 0 current-tree or generated-page findings after v2 changes | 2 redacted metadata matches from 1 historical commit: `<redacted-email>` | Future commits configured to GitHub noreply; no history rewrite performed |
| Telephone numbers | 0 | 0 | No action |
| IBAN or bank data | 0 | 0 | No action |
| Secrets or private keys | 0 | 0 | No action |
| Local private paths | 0 | 0 | No action |

## History Policy

No history rewrite was performed. If historical personal email removal is required later, use a separately authorized history-rewrite plan and coordinate tag, release, Pages, and clone invalidation impacts.
