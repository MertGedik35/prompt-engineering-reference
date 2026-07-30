# Exercise: Evaluation decision lab

Estimated time: 20–45 minutes

## Scenario

You have been asked to compare two source-grounded support prompts on six representative cases. All people, organizations, documents, and identifiers
in this lab are fictional. Work locally; no paid service or live model is required.

## Objective

Build an evaluation plan for a source-grounded customer-support assistant with at least six cases, assertions, a rubric, pairwise protocol, cost and latency measures, and release gates. Demonstrate decisions and evaluation evidence, not only a polished prompt.

## Provided inputs

- **Card 1 — Success criteria and datasets:** Criteria translate user value and risk into observable behavior. Representative datasets include frequent traffic, important minorities, and realistic distribution shifts.
- **Card 2 — Case families:** Normal cases establish baseline utility; edge cases probe ambiguous boundaries; adversarial cases test misuse and unsafe content without becoming an offensive collection.
- **Card 3 — Golden data and assertions:** Golden datasets contain reviewed expectations. Deterministic assertions check facts such as schema validity, citation presence, allowed labels, and forbidden leakage.
- **Card 4 — Human rubrics:** Rubrics define dimensions and anchored scores for qualities that code cannot fully judge, such as helpfulness, evidence use, or calibrated uncertainty.

- **Baseline request:** `Try both prompts a few times and ship whichever response feels more professional.`
- **Candidate boundary:** `Two prompts have equal rubric averages, but one is twice as slow and has a single critical unsupported-policy failure.`

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

Two prompts have equal rubric averages, but one is twice as slow and has a single critical unsupported-policy failure. Do not erase the ambiguity. Specify whether the system should clarify, proceed with
a labeled assumption, abstain, escalate, or return a structured unknown.

## Failure or adversarial case

A candidate output embeds language intended to influence an automated judge. Explain the safe expected behavior and the control that enforces it. Do not
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
[solution and answer key](../../labs/solutions/06-evaluation.md) only after completing a first
draft.
