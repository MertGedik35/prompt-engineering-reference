# Learning Path

Work through the modules in order if you are new. Returning practitioners can jump to the
[reference hub](docs/reference/index.md) and open a lesson only when a concept needs reinforcement.

Practice sequence for every module:

```text
Lesson → Exercise → Quiz → Explained solution → Checklist
```

Do not treat a guessed quiz score as completion. Finish the exercise pass conditions, answer at
least 6 of 8 quiz questions correctly, and review the checklist honestly before moving on.

Exact wall-clock times are not claimed; pace depends on prior experience and how deeply you work
the exercise cases.

## Phase 1 — Foundations

**Goal:** choose Learning vs Reference mode, understand model limits, and write a Prompt Contract.

| Module | Level | Prerequisites | You will be able to | Activity | Done when |
| --- | --- | --- | --- | --- | --- |
| [00 Orientation](curriculum/00-orientation/README.md) | Beginner | None | Navigate the repo, classify sources, and spot freshness-sensitive claims | Orientation exercise + quiz | Exercise pass conditions + ≥6/8 quiz + checklist |
| [01 LLM Foundations](curriculum/01-llm-foundations/README.md) | Beginner | 00 | Diagnose tokens, context, authority, grounding, and tool boundaries | Foundations exercise + quiz | Exercise pass conditions + ≥6/8 quiz + checklist |
| [02 Prompt Anatomy](curriculum/02-prompt-anatomy/README.md) | Beginner | 01 | Build Minimal, Standard, and Production Prompt Contracts with evaluation | Anatomy exercise + quiz | Exercise pass conditions + ≥6/8 quiz + checklist |

## Phase 2 — Building reliable prompts

**Goal:** select techniques, ground claims, constrain structure, and measure quality.

| Module | Level | Prerequisites | You will be able to | Activity | Done when |
| --- | --- | --- | --- | --- | --- |
| [03 Core Techniques](curriculum/03-core-techniques/README.md) | Intermediate | 02 | Choose zero-shot, few-shot, delimiter, constraint, and abstention tactics | Techniques exercise + quiz | Exercise pass conditions + ≥6/8 quiz + checklist |
| [04 Grounding and Long Context](curriculum/04-grounding-and-long-context/README.md) | Intermediate | 03 | Connect claims to sources and preserve provenance in long inputs | Grounding exercise + quiz | Exercise pass conditions + ≥6/8 quiz + checklist |
| [05 Structured Outputs](curriculum/05-structured-outputs/README.md) | Intermediate | 03 | Design schemas, missing-value policy, validation, and bounded repair | Structured-output exercise + quiz | Exercise pass conditions + ≥6/8 quiz + checklist |
| [06 Evaluation](curriculum/06-evaluation/README.md) | Intermediate | 05 | Build cases, assertions, rubrics, comparisons, and release gates | Evaluation exercise + quiz | Exercise pass conditions + ≥6/8 quiz + checklist |

## Phase 3 — Agents, context and security

**Goal:** bound tools and memory, allocate context, and defend against adversarial misuse.

| Module | Level | Prerequisites | You will be able to | Activity | Done when |
| --- | --- | --- | --- | --- | --- |
| [07 Agents and Tools](curriculum/07-agents-and-tools/README.md) | Intermediate | 06 | Bound tools, state, retries, stopping, delegation, and approval | Agents exercise + quiz | Exercise pass conditions + ≥6/8 quiz + checklist |
| [08 Context Engineering](curriculum/08-context-engineering/README.md) | Intermediate | 07 | Allocate authority, memory, evidence, tool results, and budgets | Context exercise + quiz | Exercise pass conditions + ≥6/8 quiz + checklist |
| [09 Security](curriculum/09-security/README.md) | Intermediate | 07 | Defend against injection, exfiltration, tool abuse, and unsafe output | Security exercise + quiz | Exercise pass conditions + ≥6/8 quiz + checklist |

## Phase 4 — Production and portfolio

**Goal:** handle multimodal work, operate prompts in production, and ship reproducible evidence.

| Module | Level | Prerequisites | You will be able to | Activity | Done when |
| --- | --- | --- | --- | --- | --- |
| [10 Multimodal](curriculum/10-multimodal/README.md) | Advanced | 06 | Design grounded multimodal contracts for images, charts, audio, and video | Multimodal exercise + quiz | Exercise pass conditions + ≥6/8 quiz + checklist |
| [11 Production Operations](curriculum/11-production-operations/README.md) | Advanced | 09 | Version, deploy, observe, migrate, and roll back prompts | Production exercise + quiz | Exercise pass conditions + ≥6/8 quiz + checklist |
| [12 Portfolio and Capstone](curriculum/12-portfolio-and-capstone/README.md) | Advanced | 11 | Present bounded claims, limitations, privacy decisions, and capstone results | Capstone module exercise + quiz, then a [capstone project](labs/capstones/README.md) | Exercise pass conditions + ≥6/8 quiz + checklist + chosen capstone |

## Shortcuts for experienced practitioners

- Jump to [Prompt patterns](docs/generated/pattern-index.md) or [templates](docs/generated/template-index.md) when you already know the concept.
- Use [Prompt Doctor](docs/generated/prompt-doctor-index.md) when a live prompt is failing.
- Compare dated provider notes in [Provider guides](docs/providers/index.md).
- Return to a module only for the lesson section that fills a specific gap.
