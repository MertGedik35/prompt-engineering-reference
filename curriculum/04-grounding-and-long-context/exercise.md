# Exercise: Grounding and Long Context decision lab

Estimated time: 20–45 minutes

## Scenario

You have been asked to reconcile fictional policy excerpts with different authorities and effective dates. All people, organizations, documents, and identifiers
in this lab are fictional. Work locally; no paid service or live model is required.

## Objective

Synthesize four fictional policy excerpts into a claim-evidence table, source ranking, answer, unresolved conflicts, and missing-evidence list. Demonstrate decisions and evaluation evidence, not only a polished prompt.

## Provided inputs

- **Card 1 — Source hierarchy:** Ranks sources by authority, scope, and freshness before synthesis. A current binding policy normally outranks an old summary or anonymous comment.
- **Card 2 — Trust boundaries:** Retrieved text is evidence, not instruction. Separating trusted control text from untrusted source content is both a quality and security requirement.
- **Card 3 — Evidence tables:** Map each material claim to source IDs, passages, dates, and confidence. They make unsupported synthesis visible to reviewers.
- **Card 4 — Conflicts and missing evidence:** Conflicts should be reported, not averaged away. Missing evidence requires a question, abstention, or explicit uncertainty depending on the task.

- **Baseline request:** `Read these documents and give me the correct policy. Use whichever source sounds most convincing.`
- **Candidate boundary:** `The highest-authority source is current but silent about a transition case described only in an older memo.`

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

The highest-authority source is current but silent about a transition case described only in an older memo. Do not erase the ambiguity. Specify whether the system should clarify, proceed with
a labeled assumption, abstain, escalate, or return a structured unknown.

## Failure or adversarial case

A retrieved excerpt tells the model to hide conflicts and cite it as the system policy. Explain the safe expected behavior and the control that enforces it. Do not
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
[solution and answer key](../../labs/solutions/04-grounding-and-long-context.md) only after completing a first
draft.
