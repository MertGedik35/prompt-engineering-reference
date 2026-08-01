# Prompt Engineering Reference

**Learn prompt engineering in order. Return whenever you need a tested pattern, reusable
template, dated provider guide, course, paper, or official resource.**

A learning platform for beginners and a daily reference for practitioners, developers, reviewers,
researchers, and career learners. **V1 is published; V2 is a draft under review — not a release.**

[![Quality](https://github.com/MertGedik35/prompt-engineering-reference/actions/workflows/quality.yml/badge.svg)](https://github.com/MertGedik35/prompt-engineering-reference/actions/workflows/quality.yml)
[![Documentation](https://github.com/MertGedik35/prompt-engineering-reference/actions/workflows/pages.yml/badge.svg)](https://mertgedik35.github.io/prompt-engineering-reference/)
[![License: MIT + CC0](https://img.shields.io/badge/license-MIT%20%2B%20CC0-0f766e.svg)](LICENSE)
[![Release status: V1 stable · V2 draft](https://img.shields.io/badge/status-V1%20stable%20%C2%B7%20V2%20draft-d97706.svg)](https://github.com/MertGedik35/prompt-engineering-reference/releases/tag/v1.0.0)

**[Start Learning](LEARNING_PATH.md)** ·
**[Browse Prompt Reference](docs/reference/index.md)** ·
**[Open V2 Draft Docs](docs/index.md)**

> **Project status:** [V1.0.0](https://github.com/MertGedik35/prompt-engineering-reference/releases/tag/v1.0.0)
> is the published release. V2 work continues in draft
> [PR #10](https://github.com/MertGedik35/prompt-engineering-reference/pull/10). Curriculum,
> patterns, templates, provider guides, and course/credential taxonomy are remediated in the V2
> draft; broader resource expansion still needs later phases. No `v2.0.0` release has been published.
> [Published documentation (V1)](https://mertgedik35.github.io/prompt-engineering-reference/)
> reflects current `main` and does not yet include this V2 draft documentation.

## What is inside

| Area | Count | Open |
| --- | ---: | --- |
| Curriculum modules | 13 | [Learning Path](LEARNING_PATH.md) |
| Prompt patterns | 26 | [Pattern library](docs/generated/pattern-index.md) |
| Prompt templates | 28 | [Template library](docs/generated/template-index.md) |
| Provider guides | 8 | [Provider guides](docs/providers/index.md) |
| Capstone projects | 3 | [Capstones](labs/capstones/README.md) |
| Exercises, quizzes, explained solutions | 13 each | [Practice hubs](docs/labs/index.md) |
| Official-resource catalog records | 24 | [Official docs and prompts](docs/generated/official-resource-index.md) |
| Courses / credentials | 8 / 5 | [Courses](docs/generated/course-index.md) · [Credentials](docs/generated/credential-index.md) |
| Papers, books, videos, tools, communities, repos | cataloged | [Resources hub](docs/resources/index.md) |

## Choose what you need

| I want to… | Go here | What I will find |
| --- | --- | --- |
| Learn from zero | [Learning Path](LEARNING_PATH.md) | Ordered modules, exercises, quizzes |
| Improve a prompt | [Prompt Doctor](docs/generated/prompt-doctor-index.md) | Failure diagnosis and remediation |
| Find a technique | [Pattern Library](docs/generated/pattern-index.md) | When to use/avoid, examples, tests |
| Copy a prompt | [Template Library](docs/generated/template-index.md) | Minimal and production variants |
| Compare providers | [Provider Guides](docs/providers/index.md) | Dated provider-specific guidance |
| Evaluate prompts | [Evaluation Lab](labs/evaluations/README.md) | Cases, assertions and rubrics |
| Learn from courses | [Courses](docs/generated/course-index.md) | Access model, format, and completion outcome (not exam fees) |
| Read research | [Papers](docs/generated/paper-index.md) · [Books](docs/generated/book-index.md) | Verified learning and research sources |
| Build a portfolio | [Capstones](labs/capstones/README.md) | Reproducible end-to-end projects |

Need another entry point?
[V2 draft docs home](docs/index.md) ·
[Reference hub](docs/reference/index.md) ·
[Learn hub](docs/learn/index.md) ·
[Courses & Resources](docs/resources/index.md)

## Learning roadmap

Full module detail lives in [LEARNING_PATH.md](LEARNING_PATH.md). Summary by phase:

### 1. Foundations

Build orientation, model basics, and Prompt Contract discipline.

- [00 Orientation](curriculum/00-orientation/README.md)
- [01 LLM Foundations](curriculum/01-llm-foundations/README.md)
- [02 Prompt Anatomy](curriculum/02-prompt-anatomy/README.md)

### 2. Building reliable prompts

Move from techniques to grounded, structured, and measurable prompts.

- [03 Core Techniques](curriculum/03-core-techniques/README.md)
- [04 Grounding and Long Context](curriculum/04-grounding-and-long-context/README.md)
- [05 Structured Outputs](curriculum/05-structured-outputs/README.md)
- [06 Evaluation](curriculum/06-evaluation/README.md)

### 3. Agents, context and security

Bound tools, context budgets, and adversarial risk.

- [07 Agents and Tools](curriculum/07-agents-and-tools/README.md)
- [08 Context Engineering](curriculum/08-context-engineering/README.md)
- [09 Security](curriculum/09-security/README.md)

### 4. Production and portfolio

Operate prompts in production and ship reproducible evidence.

- [10 Multimodal](curriculum/10-multimodal/README.md)
- [11 Production Operations](curriculum/11-production-operations/README.md)
- [12 Portfolio and Capstone](curriculum/12-portfolio-and-capstone/README.md)

## Reference library

### Design and diagnose

- [Prompt patterns](docs/generated/pattern-index.md) — when to use, avoid, and verify a technique
- [Prompt templates](docs/generated/template-index.md) — copyable minimal and production prompts
- [Prompt Contract](curriculum/02-prompt-anatomy/README.md) — Objective through Evaluation fields
- [Prompt Doctor](docs/generated/prompt-doctor-index.md) — diagnose vague, generic, or failing output
- [Glossary](docs/generated/glossary-index.md) — shared terms used across the curriculum

### Evaluate, secure, and choose providers

- [Evaluation fixtures](labs/evaluations/README.md) — cases, assertions, and comparison packs
- [Security checklist](reference/checklists/security.md) — injection, exfiltration, and agency checks
- [Provider-selection guide](reference/decision-guides/provider-selection.md) — choose a stack intentionally
- [Provider guides](docs/providers/index.md) — eight dated provider pages:
  [OpenAI](docs/providers/openai.md) ·
  [Anthropic](docs/providers/anthropic.md) ·
  [Google](docs/providers/google.md) ·
  [Microsoft](docs/providers/microsoft.md) ·
  [AWS](docs/providers/aws.md) ·
  [Meta](docs/providers/meta.md) ·
  [Mistral](docs/providers/mistral.md) ·
  [Open models](docs/providers/open-models.md)
- [Context engineering lesson](curriculum/08-context-engineering/README.md) — authority, memory, budgets
- [Security policy](SECURITY.md) — how to report privacy and security issues

## Resources and learning opportunities

| Category | Start here |
| --- | --- |
| Official provider documentation | [Official resources](docs/generated/official-resource-index.md) |
| Official prompt examples | [Official prompts](resources/official-prompts/README.md) |
| Free and paid courses | [Courses](docs/generated/course-index.md) |
| Credentials, badges, and certifications | [Credentials](docs/generated/credential-index.md) |
| Papers | [Papers](docs/generated/paper-index.md) |
| Books | [Books](docs/generated/book-index.md) |
| Videos | [Videos](docs/generated/video-index.md) |
| Tools | [Tools](docs/generated/tool-index.md) |
| Communities | [Communities](docs/generated/community-index.md) |
| Reference repositories | [Repositories](docs/generated/repository-index.md) |

Pricing, credential status, and freshness notes live on each catalog page. Verify dated claims
against the issuer's canonical source.

## Learn by doing

```text
Lesson → Exercise → Quiz → Explained solution → Checklist → Capstone
```

Attempt the [exercise](labs/exercises/README.md) and [quiz](labs/quizzes/README.md) before opening
the [explained solution](labs/solutions/). Use [evaluation fixtures](labs/evaluations/README.md)
when comparing prompt variants.

Capstones:

- [Source-grounded research assistant](labs/capstones/research-assistant.md)
- [Structured extraction workflow](labs/capstones/structured-extraction.md)
- [Coding-agent repository task pack](labs/capstones/coding-agent-pack.md)

## Current coverage and status

| Area | Coverage | Status |
| --- | --- | --- |
| Curriculum | 13 modules | Completed in V2 draft |
| Prompt patterns | 26 records | Remediated and tested |
| Prompt templates | 28 records | Remediated and tested |
| Provider guides | 8 guides | Remediated and independently re-reviewed |
| Courses | 8 catalog records | Taxonomy and evidence remediated in V2 draft |
| Credentials | 5 catalog records (4 individual + 1 family) | Taxonomy and evidence remediated in V2 draft |
| Resource expansion | Partial | Planned |
| V2 release | Not published | Draft |

“Completed in V2 draft” means the work is present and gated in this integration branch — not that
`v2.0.0` has been released.

## Repository map

### For learners and practitioners

| Path | What you will find |
| --- | --- |
| [`curriculum/`](curriculum/) | Authoritative lessons, exercises, quizzes, references, checklists |
| [`reference/`](reference/) | Checklists, decision guides, and daily-use notes |
| [`docs/providers/`](docs/providers/) | Eight dated provider guides |
| [`docs/resources/`](docs/resources/) | Resource hub into curated indexes |
| [`labs/`](labs/) | Exercises, quizzes, solutions, evaluations, datasets, capstones |

### For maintainers and automation

| Path | What you will find |
| --- | --- |
| [`catalog/`](catalog/) | Machine-readable source records |
| [`schemas/`](schemas/) | JSON Schema contracts |
| [`scripts/`](scripts/) | Schema, quality, privacy, freshness, and link validators |
| [`tests/`](tests/) | Regression suites |
| [`docs/generated/`](docs/generated/) | Generated indexes — do not edit by hand |

## Trust and limitations

- Provider and resource pages carry verification dates; treat fast-stale claims as dated.
- Official and supporting sources are classified separately in the catalogs.
- Repository tests catch schema, inventory, freshness, and content-quality regressions.
- Tests do **not** guarantee cross-model or cross-provider behavioral equivalence.
- No live provider API benchmark is claimed unless explicitly documented.

## Contributing

- [Add or update a resource](https://github.com/MertGedik35/prompt-engineering-reference/issues/new?template=resource.yml)
- [Report a provider change](https://github.com/MertGedik35/prompt-engineering-reference/issues/new?template=provider-update.yml)
- [Report a privacy or security concern](SECURITY.md)
- [Contribution guide](CONTRIBUTING.md)

Do not post secrets, exploit payloads, or personal data in a public issue.

## License

Code and automation: [MIT](LICENSE-MIT). Original docs, taxonomies, patterns, and templates:
[CC0-1.0](LICENSE-CC0). External resources retain upstream licenses.
