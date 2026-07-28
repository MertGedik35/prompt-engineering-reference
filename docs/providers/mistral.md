# Mistral AI

Last verified: 2026-07-28

## Scope

Use this page for Mistral prompting, function calling, and structured-output guidance. Treat model-specific behavior and product APIs as dated because Mistral's model lineup and agent APIs can change quickly.

## Durable Guidance

- Keep prompts concise while still specifying objective, source boundaries, and output contract.
- Use provider-native function calling when a workflow needs external actions or data lookup.
- Use structured-output guidance when downstream code consumes the response.
- Track which model and endpoint were used for each prompt evaluation.

## Prompt Design Notes

Mistral prompts should avoid mixing instructions and data in a single ambiguous block. For extraction and transformation tasks, use clear section labels and include at least one realistic example when the task has edge cases.

For multilingual tasks, evaluate the target language directly instead of assuming English prompt behavior transfers without degradation.

## Tools And Structured Output

Function-calling prompts should state selection criteria, arguments, and error behavior. Structured output should be validated after generation; invalid output recovery should use a bounded retry with the validation error included as data, not as a new hidden instruction.

## Official Sources

- [Mistral prompting](https://docs.mistral.ai/studio-api/conversations/chat-completion/prompting) (`official-mistral-prompting`)
- [Mistral function calling](https://docs.mistral.ai/studio-api/conversations/function-calling) (`official-mistral-function-calling`)
- [Mistral structured output](https://docs.mistral.ai/studio-api/conversations/structured-output) (`official-mistral-structured-output`)

## Fast-Stale Areas

- Agent APIs, model lineup, tool support, and structured-output behavior.
- Pricing, rate limits, and hosted deployment features.
- Language-specific performance observations.

## Remaining Gaps

- This repository has not run live Mistral regression tests.
- Structured-output examples are provider-aware but not provider-verified in CI.
