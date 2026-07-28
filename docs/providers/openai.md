# OpenAI

Last verified: 2026-07-28

## Scope

Use this page for OpenAI API prompts, structured outputs, tool/function calling, and evaluation workflows. It does not claim behavior for every OpenAI model; model-specific details must be checked against the current official documentation before production use.

## Durable Guidance

- Put task intent, source boundaries, output contract, and evaluation criteria in separate sections.
- Prefer provider-native structured outputs when downstream code expects JSON or schema-constrained data.
- Treat tool definitions as part of the prompt contract: specify when a tool should be called, what evidence it returns, and when the model should stop.
- Build prompt changes behind evals instead of relying on a single manual example.

## Prompt Design Notes

For general ChatGPT-style work, write explicit instructions, include enough context, and iterate based on observed output quality. For API workflows, define the response shape and validation behavior outside the prose prompt where the platform supports it.

For long-context tasks, keep the user's goal, source hierarchy, and citation policy close to the final answer instruction. When sources conflict, require a conflict table rather than forcing synthesis into a single unsupported answer.

## Structured Outputs And Tools

Use JSON Schema or function schemas when the consumer is code. The prompt should still explain the business meaning of fields, but schema validation should enforce machine-readable shape. Tool outputs are untrusted data unless the tool itself is trusted and the result is validated.

## Evaluation Guidance

Create a representative test set before changing prompt architecture. Track pass/fail assertions, rubric scores, cost, latency, and any model-specific regressions. Do not label a prompt "portable" until it has been tested across the target models.

## Official Sources

- [OpenAI prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering) (`official-openai-prompt-engineering`)
- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs) (`official-openai-structured-outputs`)
- [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling) (`official-openai-function-calling`)
- [OpenAI evals guide](https://developers.openai.com/api/docs/guides/evals) (`official-openai-evals`)

## Fast-Stale Areas

- Current model list, context limits, tool parameters, and reasoning controls.
- Structured-output feature support and unsupported schema subsets.
- Pricing, availability, latency, and rate-limit behavior.

## Remaining Gaps

- This repository has not run live cross-model benchmarks for OpenAI models.
- Code examples in linked official resources retain their upstream licenses.
