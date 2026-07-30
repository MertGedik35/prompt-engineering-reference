# Orientation

Last verified: 2026-07-30

[Exercise](exercise.md) · [Quiz](quiz.md) · [References](references.md) ·
[Checklist](checklist.md) · [Solution](../../labs/solutions/00-orientation.md)

## Learning objectives

After completing this module, you can:

- explain the important mechanisms in Orientation without relying on slogans;
- decide which information, evidence, or control the task actually requires;
- construct and evaluate an example for this module's specific failure boundaries;
- state uncertainty and provider-sensitive assumptions instead of presenting them as universal facts;
- complete the practical task: Create justified repository routes for three fictional personas without treating a directory, course page, or badge family as an individual credential.

## Why this matters

The purpose of this module is to use the repository deliberately instead of treating it as a bag of prompts. Prompting is useful only when it
changes observable behavior for a defined task. A long instruction can still fail when it lacks
evidence, authority, capabilities, or validation. Conversely, a compact instruction can be
adequate when the task is low risk and its inputs and acceptance conditions are already clear.

The central scenario is to route a beginner, an agent developer, and a credential-seeking professional through different parts of the repository. It forces the learner to make decisions rather
than merely recognize terminology. The lesson separates model behavior from surrounding software,
records which claims depend on current provider documentation, and treats uncertainty as part of
the design. Examples are fictional and contain no personal or confidential information.

## Prerequisites

- Complete the previous module or explain its completion checklist in your own words.
- Be able to distinguish an instruction from runtime input.
- Have a text editor and Python available for the local validation commands.
- Use only fictional or properly authorized data during the exercise.

## Core concepts

### Learning mode

A sequenced path that builds vocabulary and judgment through lessons, exercises, quizzes, and explained solutions. It is the right default when the learner cannot yet explain why a technique works. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Reference mode

A task-first lookup surface for patterns, templates, provider notes, checklists, and diagnostics. It assumes the user can adapt an asset and evaluate the result rather than copying it blindly. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Source classes

Official sources describe a provider's current product; academic sources support research claims; community sources offer experience; commercial sources may teach useful material while carrying sales incentives. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Cost classes

Free, paid, freemium, subscription, exam-fee, and lab-credit are different claims. A free reading page does not prove that its labs, assessment, or credential are free. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Credential taxonomy

Formal certifications, applied-skill badges, course-completion certificates, professional programs, profile achievements, directories, and no-credential resources must not be collapsed into one count. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Freshness

The last-verified date records when a mutable claim was checked. Stale-risk indicates how quickly model names, prices, limits, interfaces, and feature support may change. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Local validation

Schema, catalog, quality, privacy, link, test, and strict documentation checks provide different evidence. Passing one check never implies that the others passed. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Provider sensitivity

Prompt advice is empirical. Instruction syntax, tool schemas, structured-output support, and model behavior vary, so portable guidance still requires provider-specific tests. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

These concepts interact. Improving one dimension can expose another constraint: adding evidence
consumes context, stricter formats create validation failures, broader tools expand authority, and
additional examples raise maintenance cost. Design therefore means selecting a coherent system,
not maximizing every prompt component.

## Mental models

Use three mental models. First, treat a model request as a **bounded experiment**: the prompt,
context, configuration, and tools are inputs; the output and operational measurements are
observations. Second, draw an **authority and evidence map**: mark what controls behavior, what
merely supplies data, and what is unknown. Third, maintain a **failure ledger**: for each important
failure, record the triggering case, expected response, detection method, and mitigation.

These models prevent a common category error. Natural language that sounds forceful is not a
security boundary, a database, a schema validator, or a statistical evaluation. Put deterministic
guarantees in software and retain the prompt for semantic choices the model is suited to make.

## Key terminology

- **Learning mode:** A sequenced path that builds vocabulary and judgment through lessons, exercises, quizzes, and explained solutions. It is the right default when the learner cannot yet explain why a technique works.
- **Reference mode:** A task-first lookup surface for patterns, templates, provider notes, checklists, and diagnostics. It assumes the user can adapt an asset and evaluate the result rather than copying it blindly.
- **Source classes:** Official sources describe a provider's current product; academic sources support research claims; community sources offer experience; commercial sources may teach useful material while carrying sales incentives.
- **Cost classes:** Free, paid, freemium, subscription, exam-fee, and lab-credit are different claims. A free reading page does not prove that its labs, assessment, or credential are free.
- **Credential taxonomy:** Formal certifications, applied-skill badges, course-completion certificates, professional programs, profile achievements, directories, and no-credential resources must not be collapsed into one count.
- **Freshness:** The last-verified date records when a mutable claim was checked. Stale-risk indicates how quickly model names, prices, limits, interfaces, and feature support may change.
- **Local validation:** Schema, catalog, quality, privacy, link, test, and strict documentation checks provide different evidence. Passing one check never implies that the others passed.
- **Provider sensitivity:** Prompt advice is empirical. Instruction syntax, tool schemas, structured-output support, and model behavior vary, so portable guidance still requires provider-specific tests.

Terminology is useful only when it changes a decision. In the exercise, underline each place where
one of these terms determines an input, branch, output field, test, or stop condition.

## Minimal example

```text
Goal: I am new to prompt engineering. Route me through the first three Learning-mode modules and name one exercise after each lesson. Do not recommend a credential yet.
```

This is minimal because it exposes the decisive boundary and a checkable response without adding
production machinery. It is appropriate for a bounded, reversible trial with supplied fictional
data. It is not evidence that the same prompt is safe for automation.

## Production example

```text
Given persona, current skill, desired outcome, time budget, provider, and evidence needs, return a justified route containing curriculum modules, reference pages, freshness checks, costs that still require verification, and a stop condition for reassessment.
```

The production version adds operating controls because repeated use magnifies rare failures. A
real deployment would also pin model and prompt versions, record permitted data, validate outputs,
measure cost and latency, and provide an accountable owner. Provider support must be verified
against current official documentation before implementation.

## Bad example

```text
Show me the best prompt-engineering certificate and the best prompts.
```

## Why the bad example fails

The request hides the decision rule, evidence boundary, and response to missing or conflicting
information. It invites the model to fill gaps with plausible language. It also gives a reviewer no
stable way to distinguish success from confidence theater. The improved examples do not promise
perfection; they narrow the task, make uncertainty observable, and connect evaluation to the
failure this module addresses.

## Worked example

**Input and situation.** Route a beginner, an agent developer, and a credential-seeking professional through different parts of the repository. The supplied material is fictional,
bounded to the exercise, and may contain incomplete or conflicting information.

**Prompt design.** Begin with the minimal example, then add only the production controls required
by consequence and reuse. Delimit runtime data, name authority, state missing-information behavior,
define the output, and identify how the result will be checked. Do not request hidden chain of
thought; request concise evidence, decisions, and uncertainty that a reviewer can inspect.

**Expected behavior.** A beginner receives Orientation, Foundations, and Prompt Anatomy before templates. An agent developer skims Foundations, then studies Agents, Context Engineering, Security, and provider references. A credential seeker first reads Portfolio and Capstone plus the credential taxonomy, then verifies each current offering on its issuer's canonical page. The route is evaluated by whether every recommendation names its mode, prerequisite, evidence class, and freshness risk.

**Evaluation.** A passing response follows the declared authority, uses only authorized evidence
and capabilities, produces the required artifacts, handles the edge case explicitly, and fails
safely on the adversarial case. Reviewers should be able to reproduce the judgment from the
submission rather than trusting an unsupported self-assessment.

## Provider-specific considerations

Providers differ in instruction roles, tool schemas, native structured output, context limits,
multimodal inputs, caching, safety layers, and model lifecycle. Check the applicable provider guide
and its verification date before copying syntax. Where official documentation is silent, label the
behavior `unknown` and test it. Do not infer feature support from another provider or from a model
family name.

Model behavior can also change without a prompt edit when an alias, retrieval index, safety system,
or runtime configuration changes. Record the tested configuration with evaluation results. This
lesson teaches portable design principles, not identical behavior across models.

## Hands-on exercise

Complete [the module exercise](exercise.md). Allow approximately 20–45 minutes. The core task is:
Create justified repository routes for three fictional personas without treating a directory, course page, or badge family as an individual credential. Your submission must address the supplied normal, edge, and failure or
adversarial cases, then link each claimed success to the rubric.

## Evaluation rubric

| Dimension | Passing evidence |
| --- | --- |
| Conceptual accuracy | At least three module concepts are applied correctly, not merely named. |
| Boundary handling | The normal, edge, and failure cases produce deliberately different behavior. |
| Evidence and authority | Claims, inputs, instructions, and unknowns are visibly separated. |
| Usability | Another learner can run or review the artifact without inventing missing rules. |
| Evaluation | The submission defines observable checks and reports limitations honestly. |

A passing submission earns at least 3 on every dimension and 18 of 25 overall. Any unauthorized
action, invented source, concealed uncertainty, or exposure of sensitive information is an
automatic failure regardless of the total.

## Common failure modes

- **Vocabulary without mechanism:** the submission names module terms but no branch, field, test,
  or decision changes because of them.
- **Happy-path-only design:** the normal case works while missing, conflicting, stale, malformed,
  or adversarial input is silently forced into the same answer.
- **Unsupported portability:** behavior observed with one model or configuration is described as a
  universal property.
- **Self-certified quality:** the output says it is accurate or safe without evidence that a
  reviewer or deterministic check can inspect.
- **Prompt-only guarantees:** permissions, validation, storage, or execution safety are delegated
  to persuasive wording instead of enforced by the surrounding application.

## Official sources

- [MkDocs documentation](https://www.mkdocs.org/)
- [JSON Schema documentation](https://json-schema.org/learn/getting-started-step-by-step)

Use official sources for current product behavior. Recheck mutable claims after the verification
date; URLs alone do not prove that a feature, price, limit, or credential remains unchanged.

## Research sources

- [The Craft of Research](https://press.uchicago.edu/ucp/books/book/chicago/C/bo23521678.html)

Research informs mechanisms and limitations, but a paper's experimental setting may not match a
current hosted model. Record that transfer as a hypothesis until it is tested.

## Completion checklist

- [ ] I can explain at least three core concepts without reading their definitions.
- [ ] I completed the normal, edge, and failure or adversarial cases.
- [ ] My minimal, production, and bad examples have different purposes.
- [ ] I identified provider-sensitive and unknown behavior.
- [ ] I applied the rubric and recorded limitations rather than hiding them.
- [ ] I scored at least 6 of 8 quiz questions using the explained answer key.
- [ ] I ran the relevant local content, link, privacy, and test checks.

## Next module

Continue to [01-llm-foundations](../01-llm-foundations/README.md) if it is a module path. If this is the
final module, return to the Learning Path and begin a capstone only after reviewing the checklist.
