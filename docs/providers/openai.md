# OpenAI

Catalog ID: `provider-openai`

## Scope

- OpenAI API message design where developer instructions, user input, and retrieved evidence must
  remain distinguishable.
- Structured Outputs, function calling, and eval-driven prompt changes used by an application.

This page is an API integration guide. It treats the prompt, response schema, tool definitions,
application authorization, and eval set as separate artifacts that must be versioned together.

## Do not use this guide for

- ChatGPT product-plan behavior, workspace administration, and undocumented interface features.
- Claims that one prompt behaves identically across every current or future OpenAI model.

Model names, context limits, price, rate limits, and availability are intentionally not embedded
here. Check the current OpenAI documentation when one of those facts affects a deployment.

## Stable guidance

- Place policy and application rules in developer instructions, then pass the end user's request
  as user input.
- Use a response schema when application code requires typed fields, and validate field meaning
  after schema conformance.
- Run prompt or schema changes against stored cases and graders before replacing the production
  version.

The schema proves shape, not truth. A support response can satisfy every JSON type while citing
the wrong ticket sentence, so evidence and business-rule checks remain application concerns.

## Provider-specific prompt behavior

- Treat Structured Outputs and JSON mode as different contracts; schema adherence is the relevant
  choice when typed output is required.
- Describe each function's business preconditions in its tool definition, but let application code
  execute and authorize the call.
- Keep evaluation cases, graders, and prompt versions connected so regressions are attributable to
  a specific change.

OpenAI documents a priority distinction between developer and user instructions. That distinction
is useful only when the application actually places trusted policy in the developer message and
keeps untrusted ticket text in the user or input data. Quoting a developer rule inside a user
message does not give it the same control role.

## Relevant platform features

Structured Outputs is appropriate for a typed downstream contract. The schema should contain only
fields the workflow can validate and should not be used to smuggle changing business policy into
the API contract. Function calling is a model-to-application request: the host decides whether the
function exists for this principal, validates arguments, executes it, and returns a bounded result.
The model's selection is never authorization.

OpenAI evals provide the release surface for prompt changes. Store normal cases, boundary cases,
known failures, and graders with the prompt version. A green hand-written example is not a
replacement for a regression set.

## Minimal provider-aware example

The fictional Northstar Bicycles triage service needs a typed decision without any external action:

```text
Developer:
Classify only from the customer ticket below. If the ticket does not support a field,
use null and set needs_human_review to true. Never invent an order or warranty fact.

Return fields: category, needs_human_review, evidence_quote.

User ticket:
"The front light stopped working after yesterday's rain. I cannot find my receipt."
```

The application supplies a Structured Outputs schema for those three fields. It then verifies that
`evidence_quote` is a literal span of the ticket. No claim is made here about results from a live
OpenAI model; this is a contract design example.

## Production-oriented example

A production support flow keeps four versioned pieces:

1. Developer instructions define allowed categories, evidence rules, and the escalation condition.
2. The response schema constrains the classification and optional lookup request.
3. A read-only `lookup_warranty` function accepts an application-resolved customer and product ID;
   it never accepts an arbitrary account ID copied from ticket text.
4. The host authorizes the signed-in agent, executes the lookup, redacts unrelated fields, and
   returns only warranty status and provenance.

After the tool result, the model produces the typed answer. The host rejects evidence not found in
the ticket or returned tool record. A prompt release must pass stored cases for missing receipts,
conflicting warranty dates, prompt injection inside ticket text, no-tool decisions, and attempted
cross-account lookup. Human approval remains required for refunds or account changes.

## Evaluation and portability checks

- The sample keeps developer policy separate from the fictional customer message.
- The production workflow validates both Structured Outputs conformance and cited ticket evidence.
- Any function call remains subject to application authorization and is not treated as permission
  granted by the model.
- Re-run the same cases when changing the response schema, tool definition, model snapshot, or
  decoding controls; record failures by version rather than describing the prompt as portable.

## Fast-stale claims

| Area | Why it can change | Source | Verified |
| --- | --- | --- | --- |
| Instruction-role and model-specific prompting recommendations | The prompt guide can change as model families and recommended controls evolve. | `official-openai-prompt-engineering` | 2026-07-31 |
| Supported Structured Outputs schema surface | Supported schema features and model coverage are provider-versioned behavior. | `official-openai-structured-outputs` | 2026-07-31 |
| Function-calling parameters and strict-mode behavior | Tool controls and schema requirements can change with the API surface. | `official-openai-function-calling` | 2026-07-31 |

## Official sources

- [`official-openai-prompt-engineering` — OpenAI prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [`official-openai-structured-outputs` — OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [`official-openai-function-calling` — OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling)
- [`official-openai-evals` — OpenAI evals guide](https://developers.openai.com/api/docs/guides/evals)

## Known limitations and unverified areas

- This repository has not executed the examples against multiple OpenAI model snapshots.
- Latency, token use, and grader agreement have not been measured for the fictional support-triage
  workflow.

## Last verified

2026-07-31
