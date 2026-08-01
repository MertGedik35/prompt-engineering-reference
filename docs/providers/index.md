# Provider guides

These eight guides are decision aids for adapting a prompt contract to a documented provider or
runtime surface. Start with the learning curriculum for universal concepts; use a provider guide
when message roles, response schemas, tool calls, media handling, agent orchestration, chat
templates, or serving layers affect an implementation.

The pages deliberately avoid rankings, feature-score matrices, prices, context-window tables, and
model inventories. Those facts change quickly and would imply a comparison this repository has not
tested.

## Stable guidance and fast-stale claims

**Stable guidance** describes a durable integration boundary: for example, application code
authorizes a tool call, and a tokenizer's chat template is part of an open-model deployment
contract. It should remain useful even when a product adds models or renames a feature.

**Fast-stale claims** describe provider surfaces that can change without a repository release.
Every such claim has a source ID and verification date. `last_verified` means a maintainer could
access the cited page and checked the scoped claim on that date. It does not mean the repository
ran the provider, and it is not a promise that the fact is still current.

`stale_risk` controls review urgency in `catalog/provider-guides.json`. High-risk records become a
freshness failure after `stale_after_days`; the clock is evaluated against the current UTC date or
an explicit audit date. Review the source whenever a fast-stale fact is operationally important,
even if the record is still inside that interval.

## Where to start

| Guide | Surface type | Start here when | Boundary to preserve |
| --- | --- | --- | --- |
| [OpenAI](openai.md) | API provider | You need developer/user instruction priority, Structured Outputs, function calling, or evals | Schema conformance is not factual validation; the host authorizes tools |
| [Anthropic Claude](anthropic.md) | API and coding product | You are defining success criteria, Claude tool use, or adapting a Claude Code workflow | Claude Code context is not a general Claude API contract |
| [Google Gemini](google.md) | Multimodal API provider | Images or documents, Gemini Structured Outputs, or function declarations shape the task | Media ambiguity, schema validation, and function execution are separate |
| [Microsoft](microsoft.md) | Cloud API plus end-user product | The work targets Azure OpenAI or Microsoft 365 Copilot | Name the surface; never combine their context and permission models |
| [Amazon Bedrock](aws.md) | Multi-model platform provider | Bedrock orchestration, Agents, knowledge sources, or Guardrails are involved | AWS platform controls do not replace the model owner's prompt format |
| [Meta Llama](meta.md) | Model owner | A Meta-owned Llama artifact and its official prompt format are the target | Model revision, tokenizer, chat template, and runtime stay coupled |
| [Mistral AI](mistral.md) | API provider | Mistral system/user prompts, function calling, or structured output are used | Provider output shape does not replace semantic or authorization checks |
| [Open models](open-models.md) | Multi-owner ecosystem | Artifact, tokenizer, template, runtime, quantization, and server can vary independently | API compatibility is not behavioral parity |

An **API provider** owns a hosted request/response surface. A **platform provider** may orchestrate
models owned by other organizations. A **model owner** publishes artifacts and model-specific
format guidance but may not own the runtime used in deployment. The **open-model ecosystem**
combines several owners; it must be recorded as a stack rather than treated as one provider.

## Supported is not tested here

An official page may state that a feature is supported. That is upstream documentation evidence.
“Tested in this repository” would require a recorded invocation, pinned configuration, evaluation
cases, and results produced by this project. This remediation performed documentation research and
deterministic catalog checks only. It did not call paid model APIs, run provider behavior
benchmarks, validate tenant permissions, or compare model quality.

Each guide therefore separates documented capability from its fictional design example and lists
unverified areas. Do not convert an example into a compatibility claim.

## Portability checklist

Before moving a workflow between providers or runtimes:

1. Preserve the task, evidence boundary, output meaning, failure behavior, and evaluation cases.
2. Map trusted and untrusted content to the target surface's documented message roles.
3. Translate response schemas against the target's supported schema subset; keep domain validators.
4. Rebuild tool definitions, call parsing, authentication, authorization, approval, and sandboxing
   as application controls.
5. For multimodal work, compare media ordering, supported formats, unreadable-region behavior, and
   source-priority rules.
6. For model artifacts, pin the tokenizer, chat template, runtime, quantization, and decoding
   configuration.
7. Re-run normal, boundary, failure, security, and no-tool cases. Record the exact provider or
   deployment version and date.
8. Label the result “documented upstream,” “tested locally,” or “not verified”; never collapse
   those evidence levels into “supported.”

## Repository boundary

The catalog contains exactly eight stable provider IDs. Adding providers, maintaining a live
feature matrix, measuring prices or latency, and recommending a “best” provider are separate
projects and are outside this remediation phase.
