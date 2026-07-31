# Open models

Catalog ID: `provider-open-models`

## Scope

- Open or open-weight deployments where model artifact, tokenizer, chat template, runtime,
  quantization, and server API are independent choices.
- Portability records grounded in the official documentation of the model owner, Transformers,
  and vLLM.

This is an ecosystem guide, not a provider profile. A deployment is the combination of artifacts
and runtime decisions that produced the tested behavior.

## Do not use this guide for

- A claim that all open models share one provider, system-message behavior, safety policy, or
  function-calling format.
- Unverified license interpretation, community fork behavior, or benchmark rankings across
  hardware and quantization methods.

An OpenAI-compatible HTTP route describes an integration shape. It does not prove equivalent
instruction following, safety behavior, tool selection, or output quality.

## Stable guidance

- Pin the model artifact, tokenizer revision, chat template, runtime version, and decoding
  configuration as one testable deployment manifest.
- Render chat messages through the tokenizer's template instead of assuming a universal role-token
  format.
- Re-run semantic, safety, and latency evaluations after quantization or server changes even when
  the application API remains compatible.

Two fine-tunes derived from the same base can require different control tokens. The chat template
is therefore part of the model artifact contract rather than decorative formatting.

## Provider-specific prompt behavior

- Use Transformers chat templating as a tokenizer-owned serialization step whose control tokens
  can differ between fine-tunes.
- Treat vLLM's OpenAI-compatible server as an API adapter, not proof of behavioral parity with
  OpenAI-hosted models.
- Record vLLM quantization configuration as an experimental variable because runtime support and
  output quality can vary by method.

The relevant owners differ: the model owner documents the artifact, Hugging Face documents
Transformers serialization, and vLLM documents serving and quantization. No single source can
validate the whole stack.

## Relevant platform features

`apply_chat_template` converts role messages into the token form expected by a tokenizer. Store the
original messages, tokenizer revision, template text or hash, and rendered output when testing a
migration. Hand-written special tokens are brittle unless the exact model-owner documentation
requires and explains them.

vLLM's server can expose OpenAI-compatible endpoints and runtime-specific extensions. The host
still needs a model-specific tool parser, authorization boundary, output validation, and safe
execution loop. Quantization is a runtime/model transformation that may change compatibility,
quality, memory, and performance; the current vLLM documentation is the dated source for supported
methods.

## Minimal provider-aware example

Store structured messages and a deployment manifest rather than a pre-rendered universal prompt:

```yaml
deployment:
  model_artifact: fictional-owner/harbor-7b
  model_revision: pinned-commit
  tokenizer_revision: pinned-commit
  chat_template_hash: recorded-sha256
  runtime: vllm-pinned-version
  quantization: none
messages:
  - role: system
    content: Answer only from the supplied harbor schedule.
  - role: user
    content: Is the fictional 18:00 ferry marked cancelled?
```

The chosen tokenizer renders the messages. The manifest deliberately uses fictional identifiers
and makes no claim that the named example exists or has been run.

## Production-oriented example

A release pipeline fetches only approved model and tokenizer revisions, verifies artifact hashes,
records the license review outside this guide, and snapshots the chat template. It starts a pinned
vLLM server with an explicit quantization setting and records server arguments. The application
submits the same normal, boundary, security, and tool-parser cases before promotion.

When testing quantization, keep artifact, template, dataset, and decoding values fixed. Compare
semantic task scores, malformed structured outputs, refusals, tool-parse failures, latency, and
memory. When testing another server, preserve raw messages and compare rendered tokens as well as
outcomes. LlamaIndex may be explored as an orchestration layer, but because its repository is a
community source in this catalog, its defaults cannot substantiate an official runtime claim.

## Evaluation and portability checks

- Every experiment manifest identifies model and tokenizer revisions, selected chat template,
  runtime version, quantization method, and decoding values.
- OpenAI-compatible HTTP shape is never reported as equivalent model behavior without cross-runtime
  evaluation evidence.
- Community orchestration material appears only under supporting sources and cannot satisfy an
  official-source requirement.
- Change one stack variable at a time when diagnosing drift; otherwise model, template, runtime,
  and quantization effects cannot be attributed.

## Fast-stale claims

| Area | Why it can change | Source | Verified |
| --- | --- | --- | --- |
| Transformers chat-template API and tokenizer templates | Library behavior and model-provided templates change across Transformers and artifact revisions. | `official-huggingface-chat-templates` | 2026-07-31 |
| vLLM quantization support matrix | Supported methods, hardware paths, and compatibility constraints evolve with vLLM releases. | `official-vllm-quantization` | 2026-07-31 |
| vLLM OpenAI-compatible server behavior | Supported endpoints and extensions change independently from the served model artifact. | `official-vllm-openai-compatible-server` | 2026-07-31 |

## Official sources

- [`official-huggingface-chat-templates` — Transformers chat templates](https://huggingface.co/docs/transformers/chat_templating)
- [`official-vllm-quantization` — vLLM quantization](https://docs.vllm.ai/en/latest/features/quantization/)
- [`official-vllm-openai-compatible-server` — vLLM OpenAI-compatible server](https://docs.vllm.ai/en/latest/serving/openai_compatible_server/)

## Supporting sources

- [`repo-llamaindex` — LlamaIndex repository](https://github.com/run-llama/llama_index) —
  community orchestration example; not an official model-owner or runtime source.

## Known limitations and unverified areas

- No artifact/runtime/quantization combination has been benchmarked by this repository.
- LlamaIndex is retained only as a community orchestration example; its defaults and integrations
  were not validated for portability.

## Last verified

2026-07-31
