# Exercise: Production Operations decision lab

Estimated time: 20–45 minutes

## Scenario

You have been asked to migrate a schema-bound extraction prompt to a new model configuration. All people, organizations, documents, and identifiers
in this lab are fictional. Work locally; no paid service or live model is required.

## Objective

Create a model-migration plan with inventory, baseline, evaluation gates, staged deployment, monitoring, incident triggers, rollback, and deprecation decisions. Demonstrate decisions and evaluation evidence, not only a polished prompt.

## Provided inputs

Current configuration: prompt `extract-v3`, model `model-a-2026-01`, schema `2.1`, p95 latency 1.8
seconds, parse success 99.4%, and 0.3% unsupported-date rate. Candidate model B lowers median cost
by 12% in a small trial but raises p95 latency to 2.6 seconds and unsupported dates to 1.1%.
Release gates require p95 at most 2.2 seconds, no critical assertion regression, and an immediate
rollback target.

- **Card 1 — Ownership and versioning:** Every production prompt needs an accountable owner, semantic version, repository history, runtime configuration, and consumers. Prompt text alone is not the deployed artifact.
- **Card 2 — Change logs and gates:** A change record explains intent, diff, affected cases, expected metrics, approvals, and rollback. Evaluation gates block regressions before deployment.
- **Card 3 — Deployment and rollback:** Staged rollout, canaries, feature flags, and retained prior configurations make behavior changes observable and reversible.
- **Card 4 — Model migration:** A model change can alter instruction following, schemas, tool calls, latency, cost, and safety. Migration compares behavior on representative cases rather than assuming compatibility.

- **Baseline request:** `Switch to the newest model everywhere because it should be better and cheaper.`
- **Candidate boundary:** `The candidate improves quality but breaches the p95 latency budget during peak traffic.`

## Constraints

- Use only the fictional material in this exercise.
- Do not invent missing sources, tool results, prices, identities, or provider capabilities.
- State assumptions and unknowns explicitly.
- Separate instructions from untrusted input.
- Keep the submission reviewable in plain Markdown.

## Required deliverables

1. A short diagnosis of the baseline request.
2. A task-specific prompt or operating contract.
3. A decision log connecting at least three module concepts to design choices.
4. Expected behavior for the normal, edge, and failure cases.
5. At least four observable acceptance checks.
6. A limitations note and one justified next experiment.

## Normal case

Use the main scenario with complete, internally consistent fictional inputs. State what a correct
output must contain and which evidence makes it acceptable.

## Edge case

The candidate improves quality but breaches the p95 latency budget during peak traffic. Do not erase the ambiguity. Specify whether the system should clarify, proceed with
a labeled assumption, abstain, escalate, or return a structured unknown.

## Failure or adversarial case

A provider alias changes underneath an unpinned production configuration. Explain the safe expected behavior and the control that enforces it. Do not
turn the analysis into reusable offensive instructions.

## Evaluation rubric

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Module reasoning | Terms only | Three correct decisions | Interacting trade-offs are explained |
| Case coverage | Normal omitted | Three cases addressed | Each case has distinct expected behavior |
| Testability | Subjective quality | Four checks | Checks include failure and limitation evidence |
| Safety and evidence | Invented or unauthorized | Boundaries stated | Boundaries are enforced and auditable |
| Reusability | Missing inputs | Another learner can review | Adaptation points are explicit |

## Passing conditions

Earn at least 18 of 25, score at least 3 in every row, include all six deliverables, and avoid every
automatic failure: invented evidence, unauthorized action, concealed uncertainty, or sensitive
personal data.

## Optional extension

Create a second design for a different risk level. Explain which controls you removed or added and
why the change is justified by consequence, reuse, and available evidence.

## Solution link

Compare your reasoning with the
[solution and answer key](../../labs/solutions/11-production-operations.md) only after completing a first
draft.
