# Security

Last verified: 2026-07-28

## Learning objectives

- Explain the purpose of security.
- Apply the concept to a small prompt.
- Evaluate the result with an explicit rubric.

## Why this matters

Defend against prompt injection, tool abuse, data exfiltration, and unsafe autonomy. Without this layer, prompt advice becomes a list of tricks instead of a system that can be tested.

## Prerequisites

- Read the previous module or skim the module introduction.
- Have one real task you can use for practice.

## Core concept

Security connects prompt text to observable behavior. The lesson asks what information the model receives, which authority each piece has, and how the final answer will be checked.

## Mental model

Treat a prompt as an interface contract. Inputs enter on one side; a reviewed output leaves on the other side. The contract explains what should happen when information is missing, conflicting, unsafe, or too expensive.

## Minimal example

```text
Objective: Summarize the supplied note for a project manager.
Input: {note}
Output: three bullets and one risk.
Verification: every bullet must be supported by the note.
```

## Production example

```text
Objective: Produce a customer-facing answer from approved policy excerpts.
Context: Treat policy excerpts as the only authoritative source.
Constraints: Do not infer policy that is not stated.
Output Contract: answer, source IDs, missing information, escalation flag.
Evaluation: run normal, edge, and adversarial cases before deployment.
```

## Bad example

```text
Make this better and be accurate.
```

## Why the bad example fails

It does not name the audience, source boundary, output format, or acceptance criteria. A reviewer cannot tell whether the model succeeded.

## Provider-specific considerations

Provider-specific syntax for tools, structured output, context limits, and multimodal inputs changes over time. Use the provider pages and check their verification dates before copying model-specific guidance.

## Hands-on exercise

Rewrite a vague prompt from your own work into the Prompt Contract format. Include objective, context, inputs, constraints, output contract, and evaluation.

## Expected outcome

You should have one prompt that another person can run without asking what format or evidence is required.

## Evaluation rubric

| Dimension | Pass condition |
| --- | --- |
| Objective | The outcome and audience are explicit. |
| Context | Trusted and untrusted context are separated. |
| Output | The format is checkable. |
| Evaluation | At least one test case is named. |

## Common failure modes

- The prompt gives instructions but no acceptance criteria.
- The prompt hides assumptions instead of naming them.
- The prompt claims provider portability without testing.

## Further official reading

- [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [Claude prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
- [Gemini prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)

## Further research reading

- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)

## Next module

Multimodal prompting
