# Exercise: Prompt Anatomy decision lab

Estimated time: 20–45 minutes

## Scenario

You have been asked to turn an underspecified request for an incident brief into Minimal, Standard, and Production contracts. All people, organizations, documents, and identifiers
in this lab are fictional. Work locally; no paid service or live model is required.

## Objective

Transform one vague incident-summary request into Minimal, Standard, and Production Prompt Contracts, annotating why every added field is necessary. Demonstrate decisions and evaluation evidence, not only a polished prompt.

## Provided inputs

- **Card 1 — Objective:** Names the outcome, audience, and decision the output should support. It is mandatory whenever several plausible tasks could be inferred from the same input.
- **Card 2 — Context:** Supplies background and authority boundaries. It becomes mandatory when interpretation depends on policy, domain, time period, or organizational constraints.
- **Card 3 — Inputs:** Declares the actual runtime material and its shape. Separating inputs from instructions prevents quoted documents from silently becoming commands.
- **Card 4 — Instructions:** Define the transformation or reasoning workflow. They should expose decision points without demanding unverifiable hidden reasoning.

- **Baseline request:** `Write a professional incident report from this.`
- **Candidate boundary:** `The note contains an impact estimate but no confirmed start time and embeds a copied instruction from a customer.`

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

The note contains an impact estimate but no confirmed start time and embeds a copied instruction from a customer. Do not erase the ambiguity. Specify whether the system should clarify, proceed with
a labeled assumption, abstain, escalate, or return a structured unknown.

## Failure or adversarial case

The input requests publication and includes a secret-looking value, although the contract authorizes summarization only. Explain the safe expected behavior and the control that enforces it. Do not
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
[solution and answer key](../../labs/solutions/02-prompt-anatomy.md) only after completing a first
draft.
