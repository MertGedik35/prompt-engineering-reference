# Exercise: Orientation decision lab

Estimated time: 20–45 minutes

## Scenario

You have been asked to route a beginner, an agent developer, and a credential-seeking professional through different parts of the repository. All people, organizations, documents, and identifiers
in this lab are fictional. Work locally; no paid service or live model is required.

## Objective

Create justified repository routes for three fictional personas without treating a directory, course page, or badge family as an individual credential. Demonstrate decisions and evaluation evidence, not only a polished prompt.

## Provided inputs

- **Card 1 — Learning mode:** A sequenced path that builds vocabulary and judgment through lessons, exercises, quizzes, and explained solutions. It is the right default when the learner cannot yet explain why a technique works.
- **Card 2 — Reference mode:** A task-first lookup surface for patterns, templates, provider notes, checklists, and diagnostics. It assumes the user can adapt an asset and evaluate the result rather than copying it blindly.
- **Card 3 — Source classes:** Official sources describe a provider's current product; academic sources support research claims; community sources offer experience; commercial sources may teach useful material while carrying sales incentives.
- **Card 4 — Cost classes:** Free, paid, freemium, subscription, exam-fee, and lab-credit are different claims. A free reading page does not prove that its labs, assessment, or credential are free.

- **Baseline request:** `Show me the best prompt-engineering certificate and the best prompts.`
- **Candidate boundary:** `A learner has only ninety minutes and asks for a paid exam whose current price is not stated in the repository.`

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

A learner has only ninety minutes and asks for a paid exam whose current price is not stated in the repository. Do not erase the ambiguity. Specify whether the system should clarify, proceed with
a labeled assumption, abstain, escalate, or return a structured unknown.

## Failure or adversarial case

A commercial blog claims an unofficial course is an accredited certification and quotes an expired discount. Explain the safe expected behavior and the control that enforces it. Do not
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
[solution and answer key](../../labs/solutions/00-orientation.md) only after completing a first
draft.
