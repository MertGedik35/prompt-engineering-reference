# Google Gemini

Last verified: 2026-07-28

## Scope

Use this page for Gemini API prompting, multimodal inputs, structured output, and function calling. Google Cloud training and certification resources are cataloged separately under resources and credentials.

## Durable Guidance

- Treat multimodal inputs as first-class context: describe the user goal, image/document role, and visual ambiguity policy.
- Use structured output when a workflow needs predictable machine-readable data.
- Keep function declarations narrow and name each tool by the real external action it performs.
- Separate stable task instructions from model-specific media limits or feature syntax.

## Prompt Design Notes

Gemini prompts often combine text, images, documents, and tool calls. State which source has priority when a visual artifact conflicts with text. For charts or screenshots, ask for uncertainty labels and require the model to identify unreadable regions.

For extraction work, combine a prose instruction with a schema, then validate the result in code. Do not depend only on wording such as "return valid JSON" when provider-native schema support is available.

## Tools And Structured Output

Function calling should be evaluated with cases where no tool is needed, multiple tools are plausible, and tool output conflicts with the user's assumption. Structured-output schemas should be versioned when downstream data contracts change.

## Official Sources

- [Gemini prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) (`official-gemini-prompting`)
- [Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output) (`official-gemini-structured-output`)
- [Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling) (`official-gemini-function-calling`)

## Fast-Stale Areas

- Model availability, media limits, context windows, and supported file types.
- Structured-output schema support.
- Thinking behavior, tool behavior, pricing, and regional availability.

## Remaining Gaps

- This repository has not validated Gemini behavior with live multimodal regression tests.
- Google Cloud Skills Boost pricing and lab-credit rules must be rechecked before recommending a paid path.
