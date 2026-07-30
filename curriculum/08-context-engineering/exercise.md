# Exercise: Context Engineering decision lab

Estimated time: 20–45 minutes

## Scenario

You have been asked to plan context for a coding agent working across turns in a repository. All people, organizations, documents, and identifiers
in this lab are fictional. Work locally; no paid service or live model is required.

## Objective

Design a context ledger and compression policy for a five-turn coding task, including budgets, refresh triggers, conflict handling, and eviction decisions. Demonstrate decisions and evaluation evidence, not only a polished prompt.

## Provided inputs

- **Card 1 — Instruction layers:** System, developer, and user instructions carry different authority. Their exact names vary by platform, but the design principle is to preserve control boundaries.
- **Card 2 — Retrieved and conversational context:** Documents and conversation history supply data and prior decisions. They can be stale, irrelevant, contradictory, or malicious.
- **Card 3 — Memory:** Memory is selected persisted information, not perfect recall. Entries need provenance, scope, freshness, and deletion or correction rules.
- **Card 4 — Tool definitions and results:** Definitions expose capabilities; results add observations. Both consume context and should be included only when relevant to the next decision.

- **Baseline request:** `Remember everything from this project forever and use the entire repository in every request.`
- **Candidate boundary:** `A remembered API signature conflicts with the version currently declared in the repository.`

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

A remembered API signature conflicts with the version currently declared in the repository. Do not erase the ambiguity. Specify whether the system should clarify, proceed with
a labeled assumption, abstain, escalate, or return a structured unknown.

## Failure or adversarial case

A retrieved issue comment claims to replace the repository's security instructions. Explain the safe expected behavior and the control that enforces it. Do not
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
[solution and answer key](../../labs/solutions/08-context-engineering.md) only after completing a first
draft.
