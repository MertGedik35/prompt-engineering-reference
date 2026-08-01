# Mistral AI

Catalog ID: `provider-mistral`

## Scope

- Mistral chat-completion prompts using documented system and user roles with hierarchical
  instruction structure.
- Mistral function calling and provider-native structured output for typed application workflows.

The working example is a multilingual incident router. It demonstrates the separation between a
stable routing policy, an untrusted user report, a typed incident record, and an optional
application tool.

## Do not use this guide for

- Undocumented model-specific performance, current model lineup, pricing, rate limits, or
  agent-product behavior.
- Assuming Mistral structured output removes the need for domain validation or safe retry limits.

Language quality and endpoint behavior are empirical properties. This page does not generalize an
English prompt result to another language without test evidence.

## Stable guidance

- Put persistent behavior in the system message and keep the concrete fictional case in the user
  message.
- Use headings or another visible hierarchy when constraints, source text, and output requirements
  could be confused.
- Validate typed output and bound any repair attempt rather than accepting structurally valid but
  impossible values.

Conciseness is useful only after the decision boundary is complete. A short prompt that omits
severity rules or evidence handling is not more reliable than a longer, structured contract.

## Provider-specific prompt behavior

- Follow Mistral's documented system/user separation without assuming a hidden prompt template for
  every endpoint.
- Use Mistral function declarations for candidate tool requests while the host application
  executes the selected function.
- Choose the documented structured-output mode that matches the consumer and verify its current
  constraints upstream.

Mistral's prompting page recommends clear hierarchical organization. Its function-calling flow
returns a requested call to the application; the application executes it and supplies a result.
Structured output is a separate way to constrain response representation.

## Relevant platform features

Function descriptions should expose only operations needed by the incident workflow. A request to
page an on-call team is not self-authorizing: the host checks the user's organization, incident
severity, allowed team, and confirmation policy. A provider-native output mode can constrain
fields, while application rules validate timestamps, team names, and severity transitions.

If a typed result is semantically invalid, one bounded repair may return the validation error as
data. Repeated retries can amplify cost and hide a bad contract, so the workflow escalates after
the configured attempt.

## Minimal provider-aware example

The fictional Northwind Ferry desk receives a Turkish incident report:

```text
System:
Classify transport incidents using only the supplied report.
Return the report language unchanged in summary.
Use severity "critical" only for immediate danger to people.
Missing location or time must be null, not inferred.

User:
"İskele 4'te bilet ekranı dondu. Yolcular bekliyor, yaralanma yok.
Olay saatini bilmiyorum."
```

The response contract contains `summary`, `language`, `severity`, `location`, `occurred_at`, and
`missing_fields`. No assertion is made about output from a live Mistral endpoint.

## Production-oriented example

The production router validates the typed record against allowed severities and team identifiers.
Only critical, evidence-supported events can lead the model to request
`prepare_on_call_escalation`. The host maps the location to a permitted operations team, checks the
operator's role, shows the prepared message for confirmation, and performs the page only after
approval. The model never receives a credential or a free-form recipient.

Regression data covers missing timestamps, contradictory danger statements, mixed languages,
prompt injection inside a copied report, unsupported team names, no-tool informational events,
malformed arguments, and a failed tool result. A release records the Mistral endpoint
configuration, prompt version, response contract, tool schema, validator version, and repair
count.

## Evaluation and portability checks

- The incident workflow keeps routing policy in the system message and the fictional report in
  user content.
- The escalation function is requested only for an eligible severity and remains
  application-authorized.
- Structured incident fields pass schema validation plus allowed-team and timestamp business
  rules.
- Evaluate every target language and endpoint directly; compare schema support and tool-call
  representation before translating the contract to another provider.

## Fast-stale claims

| Area | Why it can change | Source | Verified |
| --- | --- | --- | --- |
| Mistral prompting recommendations and chat surface | The provider can revise prompting guidance as endpoints and models evolve. | `official-mistral-prompting` | 2026-07-31 |
| Mistral function-calling flow and supported controls | Tool APIs and orchestration options are versioned provider behavior. | `official-mistral-function-calling` | 2026-07-31 |
| Mistral structured-output modes and schema behavior | Output-mode availability and constraints can change across API revisions. | `official-mistral-structured-output` | 2026-07-31 |

## Official sources

- [`official-mistral-prompting` — Mistral prompting](https://docs.mistral.ai/studio-api/conversations/chat-completion/prompting)
- [`official-mistral-function-calling` — Mistral function calling](https://docs.mistral.ai/studio-api/conversations/function-calling)
- [`official-mistral-structured-output` — Mistral structured output](https://docs.mistral.ai/studio-api/conversations/structured-output)

## Known limitations and unverified areas

- The multilingual incident-routing example has not been evaluated on a live Mistral endpoint.
- The repository has not measured how often a bounded repair succeeds after semantic validation
  rejects an output.

## Last verified

2026-07-31
