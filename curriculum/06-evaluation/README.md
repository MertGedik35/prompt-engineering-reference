# Evaluation

Last verified: 2026-07-30

[Previous module](../05-structured-outputs/README.md) · [Exercise](exercise.md) · [Quiz](quiz.md) · [References](references.md) ·
[Checklist](checklist.md) · [Solution](../../labs/solutions/06-evaluation.md)

## Learning objectives

After completing this module, you can:

- explain the important mechanisms in Evaluation without relying on slogans;
- decide which information, evidence, or control the task actually requires;
- construct and evaluate an example for this module's specific failure boundaries;
- state uncertainty and provider-sensitive assumptions instead of presenting them as universal facts;
- complete the practical task: Build an evaluation plan for a source-grounded customer-support assistant with at least six cases, assertions, a rubric, pairwise protocol, cost and latency measures, and release gates.

## Why this matters

The purpose of this module is to make prompt quality an evidence-backed release decision rather than an impression. Prompting is useful only when it
changes observable behavior for a defined task. A long instruction can still fail when it lacks
evidence, authority, capabilities, or validation. Conversely, a compact instruction can be
adequate when the task is low risk and its inputs and acceptance conditions are already clear.

The central scenario is to compare two source-grounded support prompts on six representative cases. It forces the learner to make decisions rather
than merely recognize terminology. The lesson separates model behavior from surrounding software,
records which claims depend on current provider documentation, and treats uncertainty as part of
the design. Examples are fictional and contain no personal or confidential information.

## Prerequisites

- Complete the previous module or explain its completion checklist in your own words.
- Be able to distinguish an instruction from runtime input.
- Have a text editor and Python available for the local validation commands.
- Use only fictional or properly authorized data during the exercise.

## Core concepts

### Success criteria and datasets

Criteria translate user value and risk into observable behavior. Representative datasets include frequent traffic, important minorities, and realistic distribution shifts. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Case families

Normal cases establish baseline utility; edge cases probe ambiguous boundaries; adversarial cases test misuse and unsafe content without becoming an offensive collection. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Golden data and assertions

Golden datasets contain reviewed expectations. Deterministic assertions check facts such as schema validity, citation presence, allowed labels, and forbidden leakage. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Human rubrics

Rubrics define dimensions and anchored scores for qualities that code cannot fully judge, such as helpfulness, evidence use, or calibrated uncertainty. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Pairwise evaluation

Pairwise review asks which of two outputs better meets a criterion. It can be easier than absolute scoring but remains sensitive to order and presentation. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### LLM-as-judge

Model judges scale review but can prefer verbosity, share errors with candidates, or react to position and identity. Calibration and human auditing are required. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Regression and cross-model tests

A prompt change must preserve previously passing behavior. Cross-model tests reveal portability differences without assuming one model's score generalizes. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Operational metrics and statistics

Cost, latency, variance, sample size, confidence intervals, and multiple comparisons affect release decisions. Small benchmark gains may be noise or operationally unaffordable. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

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

- **Success criteria and datasets:** Criteria translate user value and risk into observable behavior. Representative datasets include frequent traffic, important minorities, and realistic distribution shifts.
- **Case families:** Normal cases establish baseline utility; edge cases probe ambiguous boundaries; adversarial cases test misuse and unsafe content without becoming an offensive collection.
- **Golden data and assertions:** Golden datasets contain reviewed expectations. Deterministic assertions check facts such as schema validity, citation presence, allowed labels, and forbidden leakage.
- **Human rubrics:** Rubrics define dimensions and anchored scores for qualities that code cannot fully judge, such as helpfulness, evidence use, or calibrated uncertainty.
- **Pairwise evaluation:** Pairwise review asks which of two outputs better meets a criterion. It can be easier than absolute scoring but remains sensitive to order and presentation.
- **LLM-as-judge:** Model judges scale review but can prefer verbosity, share errors with candidates, or react to position and identity. Calibration and human auditing are required.
- **Regression and cross-model tests:** A prompt change must preserve previously passing behavior. Cross-model tests reveal portability differences without assuming one model's score generalizes.
- **Operational metrics and statistics:** Cost, latency, variance, sample size, confidence intervals, and multiple comparisons affect release decisions. Small benchmark gains may be noise or operationally unaffordable.

Terminology is useful only when it changes a decision. In the exercise, underline each place where
one of these terms determines an input, branch, output field, test, or stop condition.

## Minimal example

```text
Evaluate the answer with two assertions: every policy claim has a supplied source ID, and unsupported questions return `needs_escalation`.
```

This is minimal because it exposes the decisive boundary and a checkable response without adding
production machinery. It is appropriate for a bounded, reversible trial with supplied fictional
data. It is not evidence that the same prompt is safe for automation.

## Production example

```text
Run prompt A and B on six normal, edge, and adversarial cases; record deterministic assertion failures, blinded rubric scores, latency, and token cost; investigate judge disagreement; release only if safety has no regression and utility clears the gate.
```

The production version adds operating controls because repeated use magnifies rare failures. A
real deployment would also pin model and prompt versions, record permitted data, validate outputs,
measure cost and latency, and provide an accountable owner. Provider support must be verified
against current official documentation before implementation.

## Bad example

```text
Try both prompts a few times and ship whichever response feels more professional.
```

## Why the bad example fails

The request hides the decision rule, evidence boundary, and response to missing or conflicting
information. It invites the model to fill gaps with plausible language. It also gives a reviewer no
stable way to distinguish success from confidence theater. The improved examples do not promise
perfection; they narrow the task, make uncertainty observable, and connect evaluation to the
failure this module addresses.

## Worked example

**Input and situation.** Compare two source-grounded support prompts on six representative cases. The supplied material is fictional,
bounded to the exercise, and may contain incomplete or conflicting information.

**Prompt design.** Begin with the minimal example, then add only the production controls required
by consequence and reuse. Delimit runtime data, name authority, state missing-information behavior,
define the output, and identify how the result will be checked. Do not request hidden chain of
thought; request concise evidence, decisions, and uncertainty that a reviewer can inspect.

**Expected behavior.** The task answers support questions from approved articles. Cases cover a direct answer, missing evidence, conflicting articles, an outdated article, a multilingual question, and injected source text. Assertions validate citations, escalation, and absence of unsupported policy. Reviewers score correctness, evidence, helpfulness, and uncertainty from one to five. Prompt B wins four pairs but fails the outdated-source assertion; despite higher average style, the revision decision is no release until freshness handling is fixed.

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
Build an evaluation plan for a source-grounded customer-support assistant with at least six cases, assertions, a rubric, pairwise protocol, cost and latency measures, and release gates. Your submission must address the supplied normal, edge, and failure or
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

- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evals)
- [Google model evaluation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-overview)

Use official sources for current product behavior. Recheck mutable claims after the verification
date; URLs alone do not prove that a feature, price, limit, or credential remains unchanged.

## Research sources

- [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)

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

Continue to [07-agents-and-tools](../07-agents-and-tools/README.md) if it is a module path. If this is the
final module, return to the Learning Path and begin a capstone only after reviewing the checklist.
