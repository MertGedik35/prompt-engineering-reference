# Prompt Engineering Reference

**Learn prompt engineering systematically. Return whenever you need a tested pattern, reusable
template, official resource, course, paper, or provider guide.**

A learning platform for beginners and a daily reference for practitioners, developers, reviewers,
researchers, and career learners. V1 is published; the V2 curriculum is under review.

[![Quality](https://github.com/MertGedik35/prompt-engineering-reference/actions/workflows/quality.yml/badge.svg)](https://github.com/MertGedik35/prompt-engineering-reference/actions/workflows/quality.yml)
[![Documentation](https://github.com/MertGedik35/prompt-engineering-reference/actions/workflows/pages.yml/badge.svg)](https://mertgedik35.github.io/prompt-engineering-reference/)
[![License: MIT + CC0](https://img.shields.io/badge/license-MIT%20%2B%20CC0-0f766e.svg)](LICENSE)
[![Release status: V1 stable · V2 draft](https://img.shields.io/badge/status-V1%20stable%20%C2%B7%20V2%20draft-d97706.svg)](https://github.com/MertGedik35/prompt-engineering-reference/releases/tag/v1.0.0)

## Start here

**[Start Learning](LEARNING_PATH.md)** ·
**[Browse the Reference](docs/reference/index.md)** ·
[Open Documentation](https://mertgedik35.github.io/prompt-engineering-reference/)

Choose Learning mode for a sequenced course with practice and explained solutions. Use Reference
mode when you already have a task and need a pattern, template, diagnostic, provider note, or
verified resource.

> **Project status:** [V1.0.0](https://github.com/MertGedik35/prompt-engineering-reference/releases/tag/v1.0.0)
> remains the current published release. V2 curriculum remediation is under review in draft
> [PR #10](https://github.com/MertGedik35/prompt-engineering-reference/pull/10). Pattern, template,
> provider, course, and credential remediation may remain incomplete. No `v2.0.0` release has been
> published.

## Quick navigation

### Learn and practice

[Learning Path](LEARNING_PATH.md) · [Exercises](labs/exercises/README.md) ·
[Quizzes](labs/quizzes/README.md) · [Solutions](labs/solutions/) ·
[Capstones](labs/capstones/README.md) · [Security](curriculum/09-security/README.md) ·
[Contributing](CONTRIBUTING.md) ·
[Documentation Site](https://mertgedik35.github.io/prompt-engineering-reference/)

### Design and diagnose

[Prompt Patterns](docs/generated/pattern-index.md) ·
[Prompt Templates](docs/generated/template-index.md) ·
[Prompt Contract](catalog/prompt_contracts.json) ·
[Prompt Doctor](docs/generated/prompt-doctor-index.md) ·
[Glossary](docs/generated/glossary-index.md) ·
[Security Checklist](reference/checklists/security.md) ·
[Decision Guides](reference/decision-guides/provider-selection.md) ·
[Evaluation Cases](labs/evaluations/README.md)

### Providers and resources

[Provider Guides](docs/providers/index.md) ·
[Official Resources](docs/generated/official-resource-index.md) ·
[Courses](docs/generated/course-index.md) ·
[Credentials](docs/generated/credential-index.md) ·
[Videos](docs/generated/video-index.md) ·
[Papers](docs/generated/paper-index.md) ·
[Reference Repositories](docs/generated/repository-index.md) ·
[Tools](docs/generated/tool-index.md)

## Choose your path

| Visitor | Recommended route |
| --- | --- |
| Complete beginner | [Orientation](curriculum/00-orientation/README.md) → [LLM Foundations](curriculum/01-llm-foundations/README.md) → [Prompt Anatomy](curriculum/02-prompt-anatomy/README.md) |
| Prompt practitioner | [Core Techniques](curriculum/03-core-techniques/README.md) → [Patterns](docs/generated/pattern-index.md) → [Templates](docs/generated/template-index.md) |
| Developer | [Structured Outputs](curriculum/05-structured-outputs/README.md) → [Agents and Tools](curriculum/07-agents-and-tools/README.md) → [Evaluation](curriculum/06-evaluation/README.md) |
| Coding-agent user | [Agents and Tools](curriculum/07-agents-and-tools/README.md) → [Context Engineering](curriculum/08-context-engineering/README.md) → [Production Operations](curriculum/11-production-operations/README.md) |
| Security reviewer | [Security](curriculum/09-security/README.md) → [Agent Controls](catalog/security_controls.json) → [Security Checklist](reference/checklists/security.md) |
| Researcher | [Grounding](curriculum/04-grounding-and-long-context/README.md) → [Evaluation](curriculum/06-evaluation/README.md) → [Papers](docs/generated/paper-index.md) |
| Career learner | [Full Curriculum](LEARNING_PATH.md) → [Exercises](labs/exercises/README.md) → [Credentials](docs/generated/credential-index.md) |
| Contributor | [Contribution Guide](CONTRIBUTING.md) → [Catalog Rules](AGENTS.md#content-rules) → [Validation Commands](AGENTS.md#required-commands) |

## Full learning path

The curriculum source of truth is under [`curriculum/`](curriculum/). Complete each exercise before
opening its explained solution.

1. **00 · [Orientation](curriculum/00-orientation/README.md)** — Choose Learning or Reference mode,
   classify sources and credentials, and navigate freshness-sensitive material.
2. **01 · [LLM Foundations](curriculum/01-llm-foundations/README.md)** — Diagnose tokens, context,
   instruction authority, grounding, probabilistic output, and tool boundaries.
3. **02 · [Prompt Anatomy](curriculum/02-prompt-anatomy/README.md)** — Build Minimal, Standard, and
   Production Prompt Contracts with explicit evaluation.
4. **03 · [Core Techniques](curriculum/03-core-techniques/README.md)** — Select zero-shot, few-shot,
   delimiter, constraint, classification, extraction, style, and abstention techniques.
5. **04 · [Grounding and Long Context](curriculum/04-grounding-and-long-context/README.md)** —
   Connect claims to sources, handle conflicts, and preserve provenance through long documents.
6. **05 · [Structured Outputs](curriculum/05-structured-outputs/README.md)** — Design schemas,
   missing-value policies, validation, bounded repair, and migration behavior.
7. **06 · [Evaluation](curriculum/06-evaluation/README.md)** — Build representative cases,
   assertions, rubrics, comparisons, regressions, and release gates.
8. **07 · [Agents and Tools](curriculum/07-agents-and-tools/README.md)** — Bound tools, state,
   retries, stopping behavior, delegation, authority, and approval.
9. **08 · [Context Engineering](curriculum/08-context-engineering/README.md)** — Allocate authority,
   memory, retrieved evidence, tool results, compression, and context budgets.
10. **09 · [Security](curriculum/09-security/README.md)** — Defend against injection, untrusted
    retrieval, exfiltration, tool abuse, excessive agency, and unsafe output.
11. **10 · [Multimodal Prompting](curriculum/10-multimodal/README.md)** — Design grounded analytical,
    generative, and editing contracts for images, charts, documents, audio, and video.
12. **11 · [Production Operations](curriculum/11-production-operations/README.md)** — Operate
    versioned prompts with deployment, migration, observability, incidents, and rollback.
13. **12 · [Portfolio and Capstone](curriculum/12-portfolio-and-capstone/README.md)** — Present
    reproducible evidence, bounded claims, limitations, privacy decisions, and capstone results.

## Reference library

### Design prompts

- [Prompt patterns](docs/generated/pattern-index.md)
- [Task-specific templates](docs/generated/template-index.md)
- [Prompt Contract variants](catalog/prompt_contracts.json)
- [Security checklist](reference/checklists/security.md)
- [Provider-selection decision guide](reference/decision-guides/provider-selection.md)

### Diagnose problems

- [Prompt Doctor diagnostics](docs/generated/prompt-doctor-index.md)
- [Evaluation module](curriculum/06-evaluation/README.md)
- [Security module](curriculum/09-security/README.md)
- [Model migration guidance](curriculum/11-production-operations/README.md#model-migration)

### Work with providers

- [OpenAI](docs/providers/openai.md)
- [Anthropic Claude](docs/providers/anthropic.md)
- [Google Gemini](docs/providers/google.md)
- [Microsoft](docs/providers/microsoft.md)
- [AWS Bedrock](docs/providers/aws.md)
- [Meta Llama](docs/providers/meta.md)
- [Mistral AI](docs/providers/mistral.md)
- [Open models](docs/providers/open-models.md)

### Learn from external resources

- [Official documentation](docs/generated/official-resource-index.md)
- [Official prompts](resources/official-prompts/README.md)
- [Courses](docs/generated/course-index.md)
- [Credentials](docs/generated/credential-index.md)
- [Videos](docs/generated/video-index.md)
- [Papers](docs/generated/paper-index.md)
- [Books and long-form guides](docs/generated/book-index.md)
- [Reference repositories](docs/generated/repository-index.md)
- [Tools](docs/generated/tool-index.md)
- [Communities](docs/generated/community-index.md)

## Recommended starting points

- [Build a production Prompt Contract](curriculum/02-prompt-anatomy/README.md#production-example).
- [Diagnose vague or generic output](docs/generated/prompt-doctor-index.md).
- [Evaluate two competing prompts](curriculum/06-evaluation/README.md#worked-example).
- [Design a safe tool-using agent](curriculum/07-agents-and-tools/README.md#production-example).
- [Ground an answer in supplied sources](curriculum/04-grounding-and-long-context/README.md#worked-example).
- [Compare dated provider guidance](docs/providers/index.md).

## Learn by doing

Attempt an [exercise](labs/exercises/README.md) and [quiz](labs/quizzes/README.md) before opening the
[explained solutions](labs/solutions/). Reusable evaluation fixtures live under
[evaluation cases and datasets](labs/evaluations/README.md).

Current capstones:

- [Source-grounded research assistant](labs/capstones/research-assistant.md)
- [Structured extraction workflow](labs/capstones/structured-extraction.md)
- [Coding-agent repository task pack](labs/capstones/coding-agent-pack.md)

## Courses and credentials

The [course catalog](docs/generated/course-index.md) and
[credential catalog](docs/generated/credential-index.md) keep learning format separate from the
credential earned. The taxonomy distinguishes free, paid, freemium, subscription, and lab-credit
learning from formal certifications, applied-skill badges, completion certificates, profile
achievements, and resources with no credential.

- [Pricing classification explained](curriculum/00-orientation/README.md#cost-classes)
- [Credential taxonomy explained](curriculum/00-orientation/README.md#credential-taxonomy)
- [Course source records](catalog/courses.json)
- [Credential source records](catalog/credentials.json)

Prices and credential claims are freshness-sensitive. Verify dated catalog records against the
issuer's canonical page; a course-completion certificate is not a formal certification.

## Provider guidance

Provider pages carry their own verification dates and fast-stale notes. Use each dated guide for
scoped guidance, then confirm current syntax and feature support against its official sources.

- [OpenAI — dated guide](docs/providers/openai.md): prompting, tools, structured output,
  evaluation, and current gaps.
- [Anthropic Claude — dated guide](docs/providers/anthropic.md): prompt structure, XML, tools, long
  context, and current gaps.
- [Google Gemini — dated guide](docs/providers/google.md): multimodal prompting, grounding, tools,
  and current gaps.
- [Microsoft — dated guide](docs/providers/microsoft.md): Azure and Microsoft learning references
  with dated boundaries.
- [AWS Bedrock — dated guide](docs/providers/aws.md): Bedrock prompting, model portability, and
  operational boundaries.
- [Meta Llama — dated guide](docs/providers/meta.md): model cards, open-model prompting, and
  deployment responsibility.
- [Mistral AI — dated guide](docs/providers/mistral.md): prompting, tools, structured output, and
  current gaps.
- [Open models — dated guide](docs/providers/open-models.md): model cards, serving stacks,
  templates, licenses, and evaluation.

## Repository map

| Directory | Purpose |
| --- | --- |
| [`curriculum/`](curriculum/) | Authoritative lessons, exercises, quizzes, references, and checklists |
| [`reference/`](reference/) | Daily-use checklists, patterns, diagnostics, glossaries, and decision guides |
| [`catalog/`](catalog/) | Machine-readable source records for generated indexes |
| [`providers/`](providers/) | Provider source pages and repository-facing entry points |
| [`resources/`](resources/) | Resource-category indexes and usage guidance |
| [`labs/`](labs/) | Exercises, quizzes, solutions, evaluations, datasets, and capstones |
| [`docs/`](docs/) | MkDocs site pages and generated catalog views |
| [`scripts/`](scripts/) | Deterministic schema, quality, privacy, freshness, and link validation |
| [`tests/`](tests/) | Regression tests for catalogs, curriculum, documentation, and privacy |

## Quality and trust

- [Verification and freshness policy](docs/project/v2-release-gates.md)
- [Freshness checker](scripts/check_freshness.py)
- [JSON Schema validation](scripts/validate_schemas.py)
- [Semantic-content checks](scripts/check_content_quality.py)
- [Privacy audit](docs/project/privacy-audit.md)
- [Security policy](SECURITY.md)
- [Contribution requirements](CONTRIBUTING.md)
- [MIT and CC0 licensing](LICENSE)

These controls make evidence and limitations visible; they do not guarantee that a prompt behaves
identically across providers or use cases.

## Contributing

Read the [contribution guide](CONTRIBUTING.md) and run its validation commands before proposing a
change.

- [Suggest a new resource](https://github.com/MertGedik35/prompt-engineering-reference/issues/new?template=resource.yml)
- [Report a provider update](https://github.com/MertGedik35/prompt-engineering-reference/issues/new?template=provider-update.yml)
- [Report a privacy concern](https://github.com/MertGedik35/prompt-engineering-reference/issues/new?template=privacy-report.yml)
- [Review the security policy](SECURITY.md) or use a
  [private security advisory](https://github.com/MertGedik35/prompt-engineering-reference/security/advisories/new)
- [Join GitHub Discussions](https://github.com/MertGedik35/prompt-engineering-reference/discussions)

Do not post secrets, exploit payloads, or personal data in a public issue. No personal email address
or phone number is used as a project contact route.

## License and limitations

Code, scripts, tests, and automation are available under [MIT](LICENSE-MIT). Original
documentation, taxonomies, patterns, and templates are available under [CC0-1.0](LICENSE-CC0).
External resources retain their upstream licenses.

Prompt engineering guidance is empirical and provider-sensitive. Treat examples as starting
points, evaluate them on representative cases, and do not claim cross-model compatibility without
evidence.
