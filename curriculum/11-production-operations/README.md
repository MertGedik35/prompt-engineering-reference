# Production Operations

Last verified: 2026-07-30

[Previous module](../10-multimodal/README.md) · [Exercise](exercise.md) · [Quiz](quiz.md) · [References](references.md) ·
[Checklist](checklist.md) · [Solution](../../labs/solutions/11-production-operations.md)

## Learning objectives

After completing this module, you can:

- explain the important mechanisms in Production Operations without relying on slogans;
- decide which information, evidence, or control the task actually requires;
- construct and evaluate an example for this module's specific failure boundaries;
- state uncertainty and provider-sensitive assumptions instead of presenting them as universal facts;
- complete the practical task: Create a model-migration plan with inventory, baseline, evaluation gates, staged deployment, monitoring, incident triggers, rollback, and deprecation decisions.

## Why this matters

The purpose of this module is to operate prompts as versioned production components with measurable rollback paths. Prompting is useful only when it
changes observable behavior for a defined task. A long instruction can still fail when it lacks
evidence, authority, capabilities, or validation. Conversely, a compact instruction can be
adequate when the task is low risk and its inputs and acceptance conditions are already clear.

The central scenario is to migrate a schema-bound extraction prompt to a new model configuration. It forces the learner to make decisions rather
than merely recognize terminology. The lesson separates model behavior from surrounding software,
records which claims depend on current provider documentation, and treats uncertainty as part of
the design. Examples are fictional and contain no personal or confidential information.

## Prerequisites

- Complete the previous module or explain its completion checklist in your own words.
- Be able to distinguish an instruction from runtime input.
- Have a text editor and Python available for the local validation commands.
- Use only fictional or properly authorized data during the exercise.

## Core concepts

### Ownership and versioning

Every production prompt needs an accountable owner, semantic version, repository history, runtime configuration, and consumers. Prompt text alone is not the deployed artifact. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Change logs and gates

A change record explains intent, diff, affected cases, expected metrics, approvals, and rollback. Evaluation gates block regressions before deployment. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Deployment and rollback

Staged rollout, canaries, feature flags, and retained prior configurations make behavior changes observable and reversible. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Model migration

A model change can alter instruction following, schemas, tool calls, latency, cost, and safety. Migration compares behavior on representative cases rather than assuming compatibility. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Budgets

Token, monetary, and latency budgets are explicit service constraints. Optimizing one dimension may reduce evidence, reliability, or user experience. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Observability

Useful telemetry includes prompt and model versions, case type, validation errors, tool calls, escalations, latency, cost, and sampled quality review without logging prohibited data. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Incident response

Detection, containment, rollback, impact assessment, correction, communication, and follow-up evaluation apply to prompt-related incidents. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Drift and deprecation

User traffic, retrieval sources, provider behavior, and policies change. Review cadence and deprecation notices prevent abandoned prompts from silently remaining in service. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

These concepts interact. Improving one dimension can expose another constraint: adding evidence
consumes context, stricter formats create validation failures, broader tools expand authority, and
additional examples raise maintenance cost. Design therefore means selecting a coherent system,
not maximizing every prompt component.

## Mental models

Use three mental models. First, treat a model request as a **bounded experiment**: the prompt,
context, configuration, and tools are inputs; the output and operational measurements are
observations. Second, draw an **authority and evidence map**: mark what controls behavior, what
merely supplies data, and what is unknown. Third, maintain a **failure ledger**: for each important
failure, record the triggering case, expected response, detection method, and mitigation.

These models prevent a common category error. Natural language that sounds forceful is not a
security boundary, a database, a schema validator, or a statistical evaluation. Put deterministic
guarantees in software and retain the prompt for semantic choices the model is suited to make.

## Key terminology

- **Ownership and versioning:** Every production prompt needs an accountable owner, semantic version, repository history, runtime configuration, and consumers. Prompt text alone is not the deployed artifact.
- **Change logs and gates:** A change record explains intent, diff, affected cases, expected metrics, approvals, and rollback. Evaluation gates block regressions before deployment.
- **Deployment and rollback:** Staged rollout, canaries, feature flags, and retained prior configurations make behavior changes observable and reversible.
- **Model migration:** A model change can alter instruction following, schemas, tool calls, latency, cost, and safety. Migration compares behavior on representative cases rather than assuming compatibility.
- **Budgets:** Token, monetary, and latency budgets are explicit service constraints. Optimizing one dimension may reduce evidence, reliability, or user experience.
- **Observability:** Useful telemetry includes prompt and model versions, case type, validation errors, tool calls, escalations, latency, cost, and sampled quality review without logging prohibited data.
- **Incident response:** Detection, containment, rollback, impact assessment, correction, communication, and follow-up evaluation apply to prompt-related incidents.
- **Drift and deprecation:** User traffic, retrieval sources, provider behavior, and policies change. Review cadence and deprecation notices prevent abandoned prompts from silently remaining in service.

Terminology is useful only when it changes a decision. In the exercise, underline each place where
one of these terms determines an input, branch, output field, test, or stop condition.

## Minimal example

```text
Record prompt version, model configuration, schema version, owner, evaluation result, deployment date, and rollback target for this change.
```

This is minimal because it exposes the decisive boundary and a checkable response without adding
production machinery. It is appropriate for a bounded, reversible trial with supplied fictional
data. It is not evidence that the same prompt is safe for automation.

## Production example

```text
Run baseline and candidate on the golden dataset, compare validation, quality, cost, and latency, canary the candidate with monitoring, stop on critical regression, and retain an immediate rollback configuration.
```

The production version adds operating controls because repeated use magnifies rare failures. A
real deployment would also pin model and prompt versions, record permitted data, validate outputs,
measure cost and latency, and provide an accountable owner. Provider support must be verified
against current official documentation before implementation.

## Bad example

```text
Switch to the newest model everywhere because it should be better and cheaper.
```

## Why the bad example fails

The request hides the decision rule, evidence boundary, and response to missing or conflicting
information. It invites the model to fill gaps with plausible language. It also gives a reviewer no
stable way to distinguish success from confidence theater. The improved examples do not promise
perfection; they narrow the task, make uncertainty observable, and connect evaluation to the
failure this module addresses.

## Worked example

**Input and situation.** Migrate a schema-bound extraction prompt to a new model configuration. The supplied material is fictional,
bounded to the exercise, and may contain incomplete or conflicting information.

**Prompt design.** Begin with the minimal example, then add only the production controls required
by consequence and reuse. Delimit runtime data, name authority, state missing-information behavior,
define the output, and identify how the result will be checked. Do not request hidden chain of
thought; request concise evidence, decisions, and uncertainty that a reviewer can inspect.

**Expected behavior.** The team snapshots the current extraction prompt and model, runs both configurations on normal, incomplete, multilingual, and adversarial reports, and discovers fewer parse failures but more invented dates. It revises the null rule, reruns the gate, and canaries ten percent of traffic. Monitoring keys every result to prompt, schema, and model versions. The old configuration remains available until the observation window closes.

**Evaluation.** A passing response follows the declared authority, uses only authorized evidence
and capabilities, produces the required artifacts, handles the edge case explicitly, and fails
safely on the adversarial case. Reviewers should be able to reproduce the judgment from the
submission rather than trusting an unsupported self-assessment.

## Provider-specific considerations

Providers differ in instruction roles, tool schemas, native structured output, context limits,
multimodal inputs, caching, safety layers, and model lifecycle. Check the applicable provider guide
and its verification date before copying syntax. Where official documentation is silent, label the
behavior `unknown` and test it. Do not infer feature support from another provider or from a model
family name.

Model behavior can also change without a prompt edit when an alias, retrieval index, safety system,
or runtime configuration changes. Record the tested configuration with evaluation results. This
lesson teaches portable design principles, not identical behavior across models.

## Hands-on exercise

Complete [the module exercise](exercise.md). Allow approximately 20–45 minutes. The core task is:
Create a model-migration plan with inventory, baseline, evaluation gates, staged deployment, monitoring, incident triggers, rollback, and deprecation decisions. Your submission must address the supplied normal, edge, and failure or
adversarial cases, then link each claimed success to the rubric.

## Evaluation rubric

| Dimension | Passing evidence |
| --- | --- |
| Conceptual accuracy | At least three module concepts are applied correctly, not merely named. |
| Boundary handling | The normal, edge, and failure cases produce deliberately different behavior. |
| Evidence and authority | Claims, inputs, instructions, and unknowns are visibly separated. |
| Usability | Another learner can run or review the artifact without inventing missing rules. |
| Evaluation | The submission defines observable checks and reports limitations honestly. |

A passing submission earns at least 3 on every dimension and 18 of 25 overall. Any unauthorized
action, invented source, concealed uncertainty, or exposure of sensitive information is an
automatic failure regardless of the total.

## Common failure modes

- **Vocabulary without mechanism:** the submission names module terms but no branch, field, test,
  or decision changes because of them.
- **Happy-path-only design:** the normal case works while missing, conflicting, stale, malformed,
  or adversarial input is silently forced into the same answer.
- **Unsupported portability:** behavior observed with one model or configuration is described as a
  universal property.
- **Self-certified quality:** the output says it is accurate or safe without evidence that a
  reviewer or deterministic check can inspect.
- **Prompt-only guarantees:** permissions, validation, storage, or execution safety are delegated
  to persuasive wording instead of enforced by the surrounding application.

## Official sources

- [OpenAI production best practices](https://platform.openai.com/docs/guides/production-best-practices)
- [Google generative AI evaluation](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview)

Use official sources for current product behavior. Recheck mutable claims after the verification
date; URLs alone do not prove that a feature, price, limit, or credential remains unchanged.

## Research sources

- [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems)

Research informs mechanisms and limitations, but a paper's experimental setting may not match a
current hosted model. Record that transfer as a hypothesis until it is tested.

## Completion checklist

- [ ] I can explain at least three core concepts without reading their definitions.
- [ ] I completed the normal, edge, and failure or adversarial cases.
- [ ] My minimal, production, and bad examples have different purposes.
- [ ] I identified provider-sensitive and unknown behavior.
- [ ] I applied the rubric and recorded limitations rather than hiding them.
- [ ] I scored at least 6 of 8 quiz questions using the explained answer key.
- [ ] I ran the relevant local content, link, privacy, and test checks.

## Next module

Continue to [12-portfolio-and-capstone](../12-portfolio-and-capstone/README.md) if it is a module path. If this is the
final module, return to the Learning Path and begin a capstone only after reviewing the checklist.
