# Exercise: Structured Outputs decision lab

Estimated time: 20–45 minutes

## Scenario

You have been asked to extract supplier incidents from noisy prose into a strict versioned schema. All people, organizations, documents, and identifiers
in this lab are fictional. Work locally; no paid service or live model is required.

## Objective

Design a JSON Schema, extraction prompt, validation assertions, and bounded recovery plan for fictional maintenance reports containing missing and contradictory fields. Demonstrate decisions and evaluation evidence, not only a polished prompt.

## Provided inputs

- **Card 1 — JSON and schemas:** JSON supplies syntax; JSON Schema supplies field names, types, required properties, enums, formats, and additional-property rules. Asking for JSON alone does not define a contract.
- **Card 2 — Native constraints:** Provider-native structured output can constrain generation to a schema, but support and limitations vary. Application-side validation remains necessary.
- **Card 3 — Function schemas:** Tool and function schemas describe callable arguments. Valid syntax does not prove that calling the function is authorized or semantically correct.
- **Card 4 — Extraction policy:** Field-level rules distinguish copying, normalization, inference, and calculation. Without them, the model may silently transform evidence.

- **Baseline request:** `Return the document as clean JSON with all useful details.`
- **Candidate boundary:** `A date contains a year and month but no day, while the downstream system accepts only full ISO dates or null.`

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

A date contains a year and month but no day, while the downstream system accepts only full ISO dates or null. Do not erase the ambiguity. Specify whether the system should clarify, proceed with
a labeled assumption, abstain, escalate, or return a structured unknown.

## Failure or adversarial case

The document asks the extractor to add an `approved` field and set it to true. Explain the safe expected behavior and the control that enforces it. Do not
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
[solution and answer key](../../labs/solutions/05-structured-outputs.md) only after completing a first
draft.
