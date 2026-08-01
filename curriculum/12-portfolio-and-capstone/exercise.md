# Exercise: Portfolio and Capstone decision lab

Estimated time: 20–45 minutes

## Scenario

You have been asked to design a portfolio case study for a grounded support assistant. All people, organizations, documents, and identifiers
in this lab are fictional. Work locally; no paid service or live model is required.

## Objective

Create a portfolio-ready capstone proposal with problem statement, evidence plan, prompt-version strategy, evaluation design, privacy constraints, limitations, and honest claim language. Demonstrate decisions and evaluation evidence, not only a polished prompt.

## Provided inputs

Candidate project: a source-grounded assistant for six synthetic support articles. Available
artifacts are three prompt versions, six English test cases, assertion results, two human rubric
reviews, and latency measurements from one model. There is no production traffic, credential,
non-English evaluation, or cross-model benchmark. One failed citation case must remain in the
reported dataset.

- **Card 1 — Project selection:** A useful capstone has a real user, bounded task, available non-sensitive data, observable success, and enough complexity to demonstrate judgment.
- **Card 2 — Problem statements:** Describe the baseline problem, stakeholders, constraints, consequence of error, and what is explicitly outside scope.
- **Card 3 — Evidence design:** Artifacts should include prompt versions, representative cases, source or schema contracts, evaluation code, results, and decisions caused by evidence.
- **Card 4 — Evaluation reporting:** Report dataset composition, metrics, rubric anchors, reviewer process, uncertainty, and regressions. A single polished example is not a benchmark.

- **Baseline request:** `I engineered a perfect prompt that makes any model 80% more accurate.`
- **Candidate boundary:** `The project has strong results on six synthetic English cases but no production traffic or cross-model testing.`

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

The project has strong results on six synthetic English cases but no production traffic or cross-model testing. Do not erase the ambiguity. Specify whether the system should clarify, proceed with
a labeled assumption, abstain, escalate, or return a structured unknown.

## Failure or adversarial case

A portfolio draft implies a course directory is an earned certification and removes failed cases from the reported dataset. Explain the safe expected behavior and the control that enforces it. Do not
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
[solution and answer key](../../labs/solutions/12-portfolio-and-capstone.md) only after completing a first
draft.
