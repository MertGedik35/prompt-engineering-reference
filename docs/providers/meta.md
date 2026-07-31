# Meta Llama

Catalog ID: `provider-meta`

## Scope

- Meta-owned Llama model artifacts, official prompt-format documents, and official cookbook
  methods.
- Deployment notes that preserve the exact Llama model revision, chat template, tokenizer, and
  runtime boundary.

This is a model-owner guide, not a guarantee about every host serving a Llama-branded artifact.
The cited prompt-format page is specifically tied to Llama 3.3.

## Do not use this guide for

- Community model forks, third-party hosted endpoints, or serving wrappers not documented by
  Meta.
- Claims that one Llama prompt format or tool convention applies to every Llama release.

License and acceptable-use decisions must be checked for the exact release. This guide does not
interpret those terms or describe current hardware requirements.

## Stable guidance

- Pin the model artifact and tokenizer together, then render messages with the chat template
  shipped for that revision.
- Store raw role content separately from rendered control tokens so a template migration can be
  reviewed.
- Re-run behavior and safety cases after quantization, adapter, fine-tune, or runtime changes.

For an open-weight deployment, a prompt is not only prose. The tokenizer and chat template turn
roles into the control-token sequence the model actually receives.

## Provider-specific prompt behavior

- Use the Llama model repository and model-specific prompt-format file as the authority for roles
  and special tokens.
- Treat Llama 3.3 tool-format examples as version-bound rather than hand-writing those tokens for
  a different Llama artifact.
- Use the official cookbook as implementation evidence while preserving the license and
  configuration assumptions of each recipe.

The official Llama 3.3 prompt-format document describes headers, end markers, and tool-call
conventions for that version. Keeping messages in structured role form and letting the matching
template render them reduces accidental token drift.

## Relevant platform features

Meta publishes model material and examples, but a self-hosted application supplies the runtime,
tool parser, authorization, safety controls, and observability. A model-emitted tool structure is
data until the host validates it. The same model weights can also behave differently after a
template, quantization, adapter, or decoding change.

The official Llama Cookbook contains practical recipes and integrations. A recipe can support an
implementation choice, but it does not turn an untested combination of hardware, server, model
revision, and quantization into a verified configuration.

## Minimal provider-aware example

Keep the fictional Alpine Outfitters inventory request as role messages before rendering:

```text
system:
Answer inventory questions only from the supplied warehouse snapshot.
If an item or timestamp is absent, return "unknown"; do not estimate stock.

user:
Warehouse snapshot: SKU MT-204 has 7 units, captured 2026-07-30T18:00Z.
Question: Can we promise 10 units of MT-204 for pickup tomorrow?
```

The matching Llama 3.3 tokenizer/template—not a manually copied token string—would serialize these
messages. The expected policy decision is not a live-model result.

## Production-oriented example

An inventory assistant stores a deployment manifest containing the exact model artifact and
revision, tokenizer revision, chat-template hash, runtime, quantization, adapter, decoding values,
and tool parser. It can request a read-only `get_inventory_snapshot` tool, but the host resolves
the warehouse from authenticated staff scope, validates the SKU, and returns quantity, capture
time, and provenance.

Tests cover missing SKUs, stale snapshots, a tool-like string inside user content, malformed model
tool output, multilingual item names, and attempted warehouse switching. Any manifest change
creates a new evaluation run. An application may preserve raw messages to compare old and new
template rendering before production migration.

## Evaluation and portability checks

- A reproducibility record names the exact Llama artifact, revision, tokenizer, template, runtime,
  and decoding settings.
- The example does not manually transplant Llama 3.3 control tokens into another model family or
  release.
- Any tool request is parsed and authorized by the serving application before an inventory system
  is queried.
- Compare both rendered token sequences and task outcomes when changing templates; matching prose
  alone is not evidence of portability.

## Fast-stale claims

| Area | Why it can change | Source | Verified |
| --- | --- | --- | --- |
| Available Llama artifacts and model-card guidance | The official model repository changes as Meta publishes revisions and accompanying documentation. | `official-llama-docs` | 2026-07-31 |
| Llama 3.3 role, tool, and special-token format | The cited prompt format belongs to one model version and does not establish future formats. | `official-llama-prompt-format` | 2026-07-31 |
| Llama Cookbook recipes and runtime integrations | Examples track changing libraries, model releases, and deployment techniques. | `repo-meta-llama-cookbook` | 2026-07-31 |

## Official sources

- [`official-llama-docs` — Llama model repository](https://github.com/meta-llama/llama-models)
- [`repo-meta-llama-cookbook` — Llama Cookbook](https://github.com/meta-llama/llama-cookbook)
- [`official-llama-prompt-format` — Llama 3.3 prompt format](https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/prompt_format.md)

## Known limitations and unverified areas

- The inventory example has not been rendered with an actual Llama 3.3 tokenizer in this
  repository.
- No controlled experiment measured drift caused by quantization or a different inference
  runtime.

## Last verified

2026-07-31
