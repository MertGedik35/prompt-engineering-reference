# Microsoft Azure OpenAI And Copilot

Last verified: 2026-07-28

## Scope

Use this page for Azure OpenAI prompt design, Azure function-calling guidance, and Microsoft 365 Copilot prompt examples. Azure OpenAI API guidance and Microsoft 365 Copilot end-user prompting are related but not interchangeable.

## Durable Guidance

- Separate API prompts from workplace Copilot prompts because the surrounding context, permissions, and tool surface differ.
- For Azure OpenAI, define grounding sources, output schema, function behavior, and evaluation criteria explicitly.
- For Microsoft 365 Copilot, include goal, context, source location, audience, and desired format.
- Record tenant, region, and product assumptions outside reusable prompts.

## Prompt Design Notes

Azure OpenAI workloads should treat retrieval and tool responses as untrusted until validated. Copilot prompts should avoid assuming access to a file, meeting, or mailbox item unless the user can provide or select that source in the product.

Prompt caching, deployment configuration, and model availability are platform concerns, not timeless prompt-writing rules. Keep them in dated provider guidance.

## Evaluation And Governance

Evaluate prompts with representative enterprise documents, redacted test data, and permission-bound scenarios. Security review should cover prompt injection through retrieved content, excessive tool permissions, and accidental disclosure of internal data.

## Official Sources

- [Azure OpenAI prompt engineering concepts](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/prompt-engineering) (`official-azure-prompt-engineering`)
- [Azure OpenAI function calling](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/function-calling) (`official-azure-function-calling`)
- [Microsoft Copilot Prompt Gallery](https://adoption.microsoft.com/en-us/copilot/prompt-gallery/) (`official-copilot-prompt-gallery`)

## Fast-Stale Areas

- Regional model availability, Azure AI Foundry feature names, and API versions.
- Microsoft 365 Copilot licensing, connectors, and prompt-gallery availability.
- Prompt caching and tool/function behavior.

## Remaining Gaps

- This repository has not tested prompts inside a live Microsoft 365 tenant.
- Credential and Applied Skills pages are high-stale-risk and must be rechecked before release.
