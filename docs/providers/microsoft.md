# Microsoft Azure OpenAI and Copilot

Catalog ID: `provider-microsoft`

## Scope

- Azure OpenAI API prompt and function-calling decisions documented in Microsoft Learn.
- Microsoft 365 Copilot end-user prompt composition illustrated by the official Prompt Gallery.

These are two different surfaces under one vendor. The Azure example is an application integration;
the Copilot example is an end-user task inside a Microsoft 365 experience. Their context and
permission boundaries are not interchangeable.

## Do not use this guide for

- Claims that Azure OpenAI deployments and Microsoft 365 Copilot share one context, permission, or
  tool model.
- Tenant licensing, regional deployment availability, connectors, and undocumented Copilot
  orchestration.

The guide also avoids embedding Azure API versions or product-plan promises. Those details are
deployment facts to verify at implementation time.

## Stable guidance

- Record whether a workflow targets an Azure OpenAI API deployment or a Microsoft 365 Copilot user
  experience before adapting prompts.
- For Azure function calls, keep identity, authorization, argument validation, and side-effect
  approval in application controls.
- For Copilot prompts, name the work artifact, intended audience, and deliverable without presuming
  the user can access a source.

The shared lesson is about declaring the execution surface, not pretending both products implement
the same prompt protocol.

## Provider-specific prompt behavior

- Treat Azure deployment and API configuration as runtime metadata rather than embedding it in
  reusable prompt prose.
- Use Azure function definitions to expose bounded operations, then validate calls against the
  signed-in principal's permissions.
- Use Prompt Gallery examples as Microsoft 365 task patterns, not as evidence for Azure OpenAI API
  semantics.

Microsoft Learn's Azure OpenAI material covers an API application context. The Copilot Prompt
Gallery demonstrates workplace goals, context, sources, and expected outputs. A gallery example
cannot establish how an Azure deployment selects a function.

## Relevant platform features

Azure function calling lets a model propose a function and arguments. The application owns the
function implementation, authenticates the user, filters arguments, confirms sensitive actions,
and returns a minimal result. Prompt instructions about permission are defense in depth, not access
control.

Microsoft 365 Copilot works with a user-facing product context. A useful prompt identifies the
document or meeting the user selected, the audience, and the requested form. It should not promise
that Copilot can see an unnamed mailbox, site, or file.

## Minimal provider-aware example

This is a Microsoft 365 Copilot-style task, not an Azure API message:

```text
Using the project brief I selected in this Copilot session, draft a five-bullet update
for the fictional Contoso Trail team. Separate confirmed milestones from open risks.
If the selected brief does not name an owner or date, write "not specified" rather
than inferring one.
```

The source must be selected and accessible by the user in the product. This repository did not run
the prompt in a Microsoft 365 tenant.

## Production-oriented example

A separate Azure OpenAI application reviews fictional purchase requests. Developer instructions
define which request fields may be summarized and when a human reviewer is mandatory. The model
may propose `get_budget_status` for a request already resolved from authenticated application
state. It cannot choose an employee or cost center supplied by untrusted document text.

The host checks the principal, validates the request ID, executes a read-only lookup, and returns
only remaining budget and its timestamp. A second `submit_purchase` operation is never made
available until an authorized reviewer confirms the prepared request. Regression cases cover
missing approvers, prompt injection in attachments, cross-cost-center access, stale budget data,
no-function outcomes, and malformed arguments. This Azure workflow is not presented as a Copilot
Prompt Gallery pattern.

## Evaluation and portability checks

- Every example is labeled either Azure OpenAI API or Microsoft 365 Copilot and never combines
  their execution models.
- The purchase-request function requires application-side identity checks and human approval
  before a side effect.
- The Copilot example names a user-selected source and does not claim access to an unspecified
  mailbox or drive.
- For portability, inventory the source-selection mechanism, message roles, function schema,
  identity boundary, and deployment metadata separately.

## Fast-stale claims

| Area | Why it can change | Source | Verified |
| --- | --- | --- | --- |
| Azure OpenAI prompt-engineering page location and platform terminology | Microsoft Learn routes and Azure AI Foundry naming change as the platform evolves. | `official-azure-prompt-engineering` | 2026-07-31 |
| Azure function-calling API surface | API versions, supported controls, and function behavior can vary by deployment. | `official-azure-function-calling` | 2026-07-31 |
| Microsoft Copilot Prompt Gallery examples | Gallery categories and Microsoft 365 product experiences can change without Azure API changes. | `official-copilot-prompt-gallery` | 2026-07-31 |

## Official sources

- [`official-azure-prompt-engineering` — Azure OpenAI prompt engineering](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering)
- [`official-azure-function-calling` — Azure OpenAI function calling](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/function-calling)
- [`official-copilot-prompt-gallery` — Microsoft Copilot Prompt Gallery](https://adoption.microsoft.com/en-us/copilot/prompt-gallery/)

## Known limitations and unverified areas

- The Copilot meeting-brief example has not been tested in a Microsoft 365 tenant with real
  permission boundaries.
- No Azure deployment was called to validate function-choice behavior for the fictional
  purchase-request service.

## Last verified

2026-07-31
