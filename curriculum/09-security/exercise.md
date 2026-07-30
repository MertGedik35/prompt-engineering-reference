# Exercise: Security decision lab

Estimated time: 20–45 minutes

## Scenario

You have been asked to review a RAG agent whose retrieved document attempts to override trusted instructions. All people, organizations, documents, and identifiers
in this lab are fictional. Work locally; no paid service or live model is required.

## Objective

Map trust boundaries, attack paths, preventative controls, detective controls, approval points, and residual risks for a fictional retrieval agent. Demonstrate decisions and evaluation evidence, not only a polished prompt.

## Provided inputs

- **Card 1 — Direct and indirect injection:** Direct injection arrives through a user request; indirect injection is embedded in retrieved pages, documents, images, or tool results. Both exploit confusion between data and instruction.
- **Card 2 — Untrusted retrieval:** Retrieval relevance does not create trust. Content must remain delimited, attributed, and prohibited from redefining goals or tool authority.
- **Card 3 — Exfiltration and secrets:** Prompts and outputs can leak credentials, personal data, system instructions, or private context. Sensitive data minimization and output filtering reduce exposure.
- **Card 4 — Tool abuse and agency:** A model with broad tools can convert a text error into external harm. Least privilege restricts tools, targets, scope, and duration.

- **Baseline request:** `Follow every instruction in the retrieved documents so the answer is complete.`
- **Candidate boundary:** `A legitimate policy document contains imperative language aimed at employees, which must be quoted as evidence without becoming an agent instruction.`

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

A legitimate policy document contains imperative language aimed at employees, which must be quoted as evidence without becoming an agent instruction. Do not erase the ambiguity. Specify whether the system should clarify, proceed with
a labeled assumption, abstain, escalate, or return a structured unknown.

## Failure or adversarial case

An untrusted document asks for secrets and an external upload; analyze it defensively without reproducing an operational exploit. Explain the safe expected behavior and the control that enforces it. Do not
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
[solution and answer key](../../labs/solutions/09-security.md) only after completing a first
draft.
