# Amazon Bedrock

Last verified: 2026-07-28

## Scope

Use this page for Amazon Bedrock prompt engineering, agents, and guardrail-aware workflows. Bedrock hosts multiple model families, so prompt behavior must be tied to the selected model and orchestration setup.

## Durable Guidance

- Identify the target model provider and model version before applying prompt advice.
- Keep model-agnostic instructions separate from provider-specific chat formats or guardrail configuration.
- Treat Bedrock Agents instructions, action groups, knowledge bases, and guardrails as separate parts of the context contract.
- Validate source use and tool outputs before taking external actions.

## Prompt Design Notes

Bedrock prompts should state the task, available knowledge source, answer boundaries, and escalation behavior. When using knowledge bases, request source-grounded answers and define how to respond when retrieved content is missing or contradictory.

For agent workflows, specify action preconditions, user confirmation requirements, and what the agent must do after a tool returns an error. Prompt wording cannot replace IAM, network, and sandbox controls.

## Security And Guardrails

Guardrails are policy controls, not a substitute for safe prompt design. Test prompt injection, untrusted retrieval, sensitive-data handling, and tool-abuse cases with representative examples.

## Official Sources

- [Amazon Bedrock prompt engineering guidelines](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-engineering-guidelines.html) (`official-bedrock-prompt-guidelines`)
- [Amazon Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html) (`official-bedrock-agents`)
- [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) (`official-bedrock-guardrails`)

## Fast-Stale Areas

- Supported model list, model-provider behavior, and regional availability.
- Agent feature support, action-group behavior, and guardrail configuration.
- Pricing and quota limits.

## Remaining Gaps

- This repository has not run live Bedrock model comparisons.
- Provider-specific behavior for third-party models on Bedrock must be verified against both AWS and the model provider.
