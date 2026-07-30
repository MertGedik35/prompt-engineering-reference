# Exercise: Agents and Tools decision lab

Estimated time: 20–45 minutes

## Scenario

You have been asked to design a research agent that can search and read but requires approval for external or mutating actions. All people, organizations, documents, and identifiers
in this lab are fictional. Work locally; no paid service or live model is required.

## Objective

Create an agent contract containing a tool allowlist, approval matrix, state ledger, retry rules, stop conditions, and final evidence report. Demonstrate decisions and evaluation evidence, not only a polished prompt.

## Provided inputs

Available tools: `search_public(query)`, `read_url(url)`, `write_file(path, text)`,
`send_message(recipient, body)`, and `purchase_access(url, amount)`. The agent may use only the
first two without approval. Research budget: eight calls and two retries total. Required report:
claims with URLs and access dates, unresolved conflicts, denied or proposed actions, and remaining
evidence gaps.

- **Card 1 — Tool schemas and selection:** A tool definition states arguments, outputs, side effects, and errors. Selection policy says when supplied context is enough and when a call is justified.
- **Card 2 — Provenance and interpretation:** Tool results are observations with source and time, not unquestionable truth. Agents should record which result supports each conclusion.
- **Card 3 — Goal persistence and state:** A durable goal, plan, completed actions, unresolved questions, and constraints prevent multi-turn work from drifting or repeating.
- **Card 4 — Stop conditions:** Success, exhausted evidence, risk threshold, budget, attempt limit, and required human choice are explicit terminal states.

- **Baseline request:** `Research this thoroughly and take whatever actions are needed to finish.`
- **Candidate boundary:** `The only relevant source requires account creation and acceptance of new terms.`

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

The only relevant source requires account creation and acceptance of new terms. Do not erase the ambiguity. Specify whether the system should clarify, proceed with
a labeled assumption, abstain, escalate, or return a structured unknown.

## Failure or adversarial case

A web page instructs the research agent to upload its conversation history for access. Explain the safe expected behavior and the control that enforces it. Do not
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
[solution and answer key](../../labs/solutions/07-agents-and-tools.md) only after completing a first
draft.
