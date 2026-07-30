# Exercise: Multimodal Prompting decision lab

Estimated time: 20–45 minutes

## Scenario

You have been asked to compare chart analysis, image generation, and image editing contracts. All people, organizations, documents, and identifiers
in this lab are fictional. Work locally; no paid service or live model is required.

## Objective

Design one chart-analysis prompt and one image-generation brief from fictional assets, then explain how grounding, uncertainty, and accessibility differ. Demonstrate decisions and evaluation evidence, not only a polished prompt.

## Provided inputs

- **Card 1 — Image understanding:** Requests should identify the inspection goal, relevant regions, acceptable inference, and uncertainty. Visible pixels do not prove identity, intent, or events outside the frame.
- **Card 2 — Screenshots and documents:** Layout, cropping, resolution, hidden content, OCR errors, and page order affect interpretation. Text extraction should retain page or region references.
- **Card 3 — Charts and diagrams:** Axes, units, legends, baselines, encodings, and annotations must be inspected before conclusions. Source data is preferable for exact calculations.
- **Card 4 — Generation briefs:** A generation brief specifies subject, composition, medium, lighting, constraints, intended use, and review criteria rather than asking for an abstract quality adjective.

- **Baseline request:** `Look at this and make it better.`
- **Candidate boundary:** `The chart legend is cropped and two series use colors that are indistinguishable for some viewers.`

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

The chart legend is cropped and two series use colors that are indistinguishable for some viewers. Do not erase the ambiguity. Specify whether the system should clarify, proceed with
a labeled assumption, abstain, escalate, or return a structured unknown.

## Failure or adversarial case

A screenshot contains text telling the analyzer to ignore the user's question and disclose hidden context. Explain the safe expected behavior and the control that enforces it. Do not
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
[solution and answer key](../../labs/solutions/10-multimodal.md) only after completing a first
draft.
