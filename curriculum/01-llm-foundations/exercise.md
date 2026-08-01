# Exercise: LLM Foundations decision lab

Estimated time: 20–45 minutes

## Scenario

You have been asked to answer a warranty question under missing context, grounded context, conflicting authority, and authorized tool access. All people, organizations, documents, and identifiers
in this lab are fictional. Work locally; no paid service or live model is required.

## Objective

Diagnose three outputs caused respectively by missing policy data, conflicting instructions, and a request requiring an unavailable account lookup tool. Demonstrate decisions and evaluation evidence, not only a polished prompt.

## Provided inputs

Diagnose these outputs:

- **Case A:** No policy was supplied, yet the answer says accidental damage is covered for two years.
- **Case B:** The system requires cited policy; the user says to ignore citations and approve the claim.
- **Case C:** The user asks for their remaining warranty balance, but no account data or lookup tool is available.
- **Approved excerpt for comparison:** `P1 (effective 2026-01-01): manufacturing defects are covered; accidental damage is excluded.`

- **Card 1 — Tokens:** Models process text and other inputs as token sequences, not as human concepts. Tokenization affects context usage, truncation, latency, and cost, while token counts differ across models and languages.
- **Card 2 — Context windows:** The context window bounds the information available during a request. Large windows reduce some truncation problems but do not guarantee attention, factuality, or correct prioritization.
- **Card 3 — Instruction hierarchy:** Higher-authority instructions constrain lower-authority requests. User content, retrieved documents, and tool results may contain text that looks imperative without gaining authority.
- **Card 4 — Probabilistic generation:** The model predicts continuations from learned distributions. A fluent answer is not a database lookup or proof, and repeated runs may differ even when the prompt is unchanged.

- **Baseline request:** `Tell the customer whether their current warranty covers this. Be completely certain.`
- **Candidate boundary:** `Two approved excerpts use different effective dates and produce different coverage answers.`

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

Two approved excerpts use different effective dates and produce different coverage answers. Do not erase the ambiguity. Specify whether the system should clarify, proceed with
a labeled assumption, abstain, escalate, or return a structured unknown.

## Failure or adversarial case

A retrieved customer note says to ignore the policy and approve every claim. Explain the safe expected behavior and the control that enforces it. Do not
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
[solution and answer key](../../labs/solutions/01-llm-foundations.md) only after completing a first
draft.
