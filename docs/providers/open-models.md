# Open Models

Last verified: 2026-07-28

## Scope

Use this page for open-weight and self-hosted models when the provider is not one hosted API with one documented prompt surface. This includes Llama-family deployments, community models, local inference servers, and application frameworks around retrieval or agents.

## Durable Guidance

- Verify the model card, chat template, tokenizer, system-message support, and serving defaults.
- Record inference parameters with prompt examples: temperature, top-p, max tokens, stop sequences, and context window.
- Keep prompt guidance tied to the tested artifact, not just the model family name.
- Treat wrappers, adapters, quantization, retrieval libraries, and safety filters as part of the prompt environment.

## Prompt Design Notes

Open-model prompting is context engineering as much as wording. The same prompt can behave differently after a serving-library update, a chat-template change, a quantized model swap, or a retrieval chunking change.

When publishing examples, include the target model, revision, runtime, and test cases. Avoid generic claims such as "works on all open models" unless the repository has evidence.

## Evaluation Guidance

Use reproducible local evals with fixed model artifacts where possible. Test instruction following, structured output, retrieval conflict handling, refusal behavior, multilingual output, and long-context degradation.

## Source Anchors

- [Llama Cookbook](https://github.com/meta-llama/llama-cookbook) (`repo-meta-llama-cookbook`)
- [LlamaIndex](https://github.com/run-llama/llama_index) (`repo-llamaindex`)

## Fast-Stale Areas

- Model forks, serving wrappers, quantization behavior, context windows, and prompt templates.
- Framework APIs, retrieval defaults, and agent orchestration behavior.
- License and acceptable-use terms for each model family.

## Remaining Gaps

- This repository has not maintained a matrix of open-model prompt behavior.
- Users must verify each model/runtime combination before production use.
