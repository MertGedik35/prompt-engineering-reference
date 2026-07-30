# Multimodal Prompting

Last verified: 2026-07-30

[Previous module](../09-security/README.md) · [Exercise](exercise.md) · [Quiz](quiz.md) · [References](references.md) ·
[Checklist](checklist.md) · [Solution](../../labs/solutions/10-multimodal.md)

## Learning objectives

After completing this module, you can:

- explain the important mechanisms in Multimodal Prompting without relying on slogans;
- decide which information, evidence, or control the task actually requires;
- construct and evaluate an example for this module's specific failure boundaries;
- state uncertainty and provider-sensitive assumptions instead of presenting them as universal facts;
- complete the practical task: Design one chart-analysis prompt and one image-generation brief from fictional assets, then explain how grounding, uncertainty, and accessibility differ.

## Why this matters

The purpose of this module is to match prompts and output contracts to visual, audio, and generative evidence. Prompting is useful only when it
changes observable behavior for a defined task. A long instruction can still fail when it lacks
evidence, authority, capabilities, or validation. Conversely, a compact instruction can be
adequate when the task is low risk and its inputs and acceptance conditions are already clear.

The central scenario is to compare chart analysis, image generation, and image editing contracts. It forces the learner to make decisions rather
than merely recognize terminology. The lesson separates model behavior from surrounding software,
records which claims depend on current provider documentation, and treats uncertainty as part of
the design. Examples are fictional and contain no personal or confidential information.

## Prerequisites

- Complete the previous module or explain its completion checklist in your own words.
- Be able to distinguish an instruction from runtime input.
- Have a text editor and Python available for the local validation commands.
- Use only fictional or properly authorized data during the exercise.

## Core concepts

### Image understanding

Requests should identify the inspection goal, relevant regions, acceptable inference, and uncertainty. Visible pixels do not prove identity, intent, or events outside the frame. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Screenshots and documents

Layout, cropping, resolution, hidden content, OCR errors, and page order affect interpretation. Text extraction should retain page or region references. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Charts and diagrams

Axes, units, legends, baselines, encodings, and annotations must be inspected before conclusions. Source data is preferable for exact calculations. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Generation briefs

A generation brief specifies subject, composition, medium, lighting, constraints, intended use, and review criteria rather than asking for an abstract quality adjective. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Image editing

Editing needs a source image, preserved elements, changed region, blending expectations, and treatment of text or identities. It differs from creating a new scene. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Video

Video prompts include shot sequence, duration, camera behavior, motion, continuity, and audio intent. Current capabilities and limits are provider-sensitive. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Audio and voice

Language, speaker count, acoustic conditions, timing, transcription uncertainty, consent, and accessibility shape the contract. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

### Grounding and accessibility

Analytical outputs separate observation from inference. Generative outputs include alt-text intent, contrast, legibility, captions, and alternatives where relevant. In practice, test this concept against the module scenario rather than assuming the wording alone guarantees behavior.

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

- **Image understanding:** Requests should identify the inspection goal, relevant regions, acceptable inference, and uncertainty. Visible pixels do not prove identity, intent, or events outside the frame.
- **Screenshots and documents:** Layout, cropping, resolution, hidden content, OCR errors, and page order affect interpretation. Text extraction should retain page or region references.
- **Charts and diagrams:** Axes, units, legends, baselines, encodings, and annotations must be inspected before conclusions. Source data is preferable for exact calculations.
- **Generation briefs:** A generation brief specifies subject, composition, medium, lighting, constraints, intended use, and review criteria rather than asking for an abstract quality adjective.
- **Image editing:** Editing needs a source image, preserved elements, changed region, blending expectations, and treatment of text or identities. It differs from creating a new scene.
- **Video:** Video prompts include shot sequence, duration, camera behavior, motion, continuity, and audio intent. Current capabilities and limits are provider-sensitive.
- **Audio and voice:** Language, speaker count, acoustic conditions, timing, transcription uncertainty, consent, and accessibility shape the contract.
- **Grounding and accessibility:** Analytical outputs separate observation from inference. Generative outputs include alt-text intent, contrast, legibility, captions, and alternatives where relevant.

Terminology is useful only when it changes a decision. In the exercise, underline each place where
one of these terms determines an input, branch, output field, test, or stop condition.

## Minimal example

```text
Inspect the chart title, axes, units, legend, and visible values. Answer the question, cite the visual elements used, and flag unreadable or ambiguous labels.
```

This is minimal because it exposes the decisive boundary and a checkable response without adding
production machinery. It is appropriate for a bounded, reversible trial with supplied fictional
data. It is not evidence that the same prompt is safe for automation.

## Production example

```text
For analysis, preserve region-level evidence and avoid unsupported precision. For generation, return a production brief and QA checklist. For editing, enumerate preserved and changed elements and reject changes requiring missing source assets.
```

The production version adds operating controls because repeated use magnifies rare failures. A
real deployment would also pin model and prompt versions, record permitted data, validate outputs,
measure cost and latency, and provide an accountable owner. Provider support must be verified
against current official documentation before implementation.

## Bad example

```text
Look at this and make it better.
```

## Why the bad example fails

The request hides the decision rule, evidence boundary, and response to missing or conflicting
information. It invites the model to fill gaps with plausible language. It also gives a reviewer no
stable way to distinguish success from confidence theater. The improved examples do not promise
perfection; they narrow the task, make uncertainty observable, and connect evaluation to the
failure this module addresses.

## Worked example

**Input and situation.** Compare chart analysis, image generation, and image editing contracts. The supplied material is fictional,
bounded to the exercise, and may contain incomplete or conflicting information.

**Prompt design.** Begin with the minimal example, then add only the production controls required
by consequence and reuse. Delimit runtime data, name authority, state missing-information behavior,
define the output, and identify how the result will be checked. Do not request hidden chain of
thought; request concise evidence, decisions, and uncertainty that a reviewer can inspect.

**Expected behavior.** The chart-analysis prompt asks for evidence and ambiguity, not artistic style. The image-generation brief defines a new accessible infographic, composition, palette, and text constraints. The edit request preserves the photographed product while replacing only the background and shadow. Their output contracts differ because one returns claims, one creates pixels, and one transforms a supplied asset under preservation rules.

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
Design one chart-analysis prompt and one image-generation brief from fictional assets, then explain how grounding, uncertainty, and accessibility differ. Your submission must address the supplied normal, edge, and failure or
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

- [OpenAI vision guide](https://developers.openai.com/api/docs/guides/images-vision)
- [Google image understanding](https://ai.google.dev/gemini-api/docs/image-understanding)

Use official sources for current product behavior. Recheck mutable claims after the verification
date; URLs alone do not prove that a feature, price, limit, or credential remains unchanged.

## Research sources

- [GPT-4V system card](https://cdn.openai.com/papers/GPTV_System_Card.pdf)

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

Continue to [11-production-operations](../11-production-operations/README.md) if it is a module path. If this is the
final module, return to the Learning Path and begin a capstone only after reviewing the checklist.
