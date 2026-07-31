# Prompt Reference

Daily lookup for techniques, copyable prompts, diagnostics, evaluation helpers, security checks,
and provider-selection guidance. Prefer these human-readable pages over raw catalog JSON.

## Design prompts

| Resource | Use when | Open |
| --- | --- | --- |
| Prompt patterns | You need a named technique with use/avoid boundaries and tests | [Patterns](../generated/pattern-index.md) |
| Prompt templates | You need a copyable minimal or production prompt | [Templates](../generated/template-index.md) |
| Prompt Contract | You are structuring Objective through Evaluation fields | [Prompt Anatomy](../learn/prompt-anatomy.md) |
| Provider-selection guide | You must choose a provider or runtime stack intentionally | [Provider selection](provider-selection.md) |

## Diagnose and evaluate

| Resource | Use when | Open |
| --- | --- | --- |
| Prompt Doctor | Output is vague, generic, ungrounded, or failing a check | [Prompt Doctor](../generated/prompt-doctor-index.md) |
| Evaluation fixtures | You need reusable cases, assertions, or comparison packs | [Evaluation lab](../labs/evaluations.md) |
| Glossary | You need a shared definition used across lessons | [Glossary](../generated/glossary-index.md) |

## Secure and operate

| Resource | Use when | Open |
| --- | --- | --- |
| Security checklist | You are reviewing injection, exfiltration, or agency risk | [Security checklist](security-checklist.md) |
| Context engineering | You must allocate authority, memory, and context budgets | [Context lesson](../learn/context-engineering.md) |
| Production operations | You need versioning, migration, observability, or rollback | [Production lesson](../learn/production-operations.md) |

## Provider guides

Dated provider-specific guidance lives under [Provider Guides](../providers/index.md):

[OpenAI](../providers/openai.md) ·
[Anthropic](../providers/anthropic.md) ·
[Google](../providers/google.md) ·
[Microsoft](../providers/microsoft.md) ·
[AWS](../providers/aws.md) ·
[Meta](../providers/meta.md) ·
[Mistral](../providers/mistral.md) ·
[Open models](../providers/open-models.md)

Machine-readable catalogs used by automation live under `catalog/` and are not the primary
visitor entry point.
