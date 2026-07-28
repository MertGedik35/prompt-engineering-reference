# Meta Llama

Last verified: 2026-07-28

## Scope

Use this page for Meta Llama prompt format, official Llama documentation, and Llama cookbook examples. It applies only when the deployed model and serving layer preserve the documented chat template and model assumptions.

## Durable Guidance

- Verify the exact model family, model version, chat template, and serving library before reusing prompts.
- Preserve required message-role formatting and special tokens where the model card or prompt-format document requires them.
- Keep system instructions, user content, retrieved documents, and tool outputs visibly separated.
- Test prompts after quantization, fine-tuning, adapter changes, or serving-layer changes.

## Prompt Design Notes

Open-weight deployment creates more variables than hosted APIs: tokenization, chat template, sampling defaults, system-message support, and safety layers may differ. A Llama prompt that works in one serving stack should be treated as unverified in another until tested.

When using cookbook examples, adapt the method and evaluation approach, not just the surface wording. Record hardware, serving configuration, and model revision in experiment notes.

## Evaluation Guidance

Run regression tests on the actual deployed artifact. Include cases for instruction following, refusal boundaries, structured output, retrieval conflicts, multilingual inputs, and long-context behavior.

## Official Sources

- [Llama documentation](https://developer.meta.com/ai/docs/overview/) (`official-llama-docs`)
- [Llama Cookbook](https://github.com/meta-llama/llama-cookbook) (`repo-meta-llama-cookbook`)
- [Llama prompt format](https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/prompt_format.md) (`official-llama-prompt-format`)

## Fast-Stale Areas

- Prompt format tokens, model cards, licensing, and hosted serving behavior.
- New model releases, safety tuning, quantized variants, and community serving wrappers.
- Hardware and latency guidance.

## Remaining Gaps

- This repository has not benchmarked Llama prompts across serving stacks.
- License and acceptable-use terms for each Llama release must be checked upstream.
