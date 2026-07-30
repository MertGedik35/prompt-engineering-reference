# Solution and answer key: Evaluation

## Exercise reasoning criteria

A successful submission diagnoses the baseline, applies at least three module concepts to concrete
decisions, and specifies distinct behavior for complete, ambiguous, and hostile or failing input.
It separates prompt-level guidance from application-enforced controls and makes uncertainty
visible. The reviewer should be able to trace every acceptance claim to an artifact.

## Example acceptable submission

The submission begins by rejecting `Try both prompts a few times and ship whichever response feels more professional.` because it hides the relevant boundaries. It
then uses this task-specific core: `Evaluate the answer with two assertions: every policy claim has a supplied source ID, and unsupported questions return `needs_escalation`.` The production section adds:
`Run prompt A and B on six normal, edge, and adversarial cases; record deterministic assertion failures, blinded rubric scores, latency, and token cost; investigate judge disagreement; release only if safety has no regression and utility clears the gate.` A decision log explains why these controls fit the consequence and reuse
level. For the normal case it defines complete expected evidence; for the edge case it uses an
explicit uncertainty branch; for the failure case it refuses unauthorized behavior and records the
control. Four checks cover required output, evidence, edge behavior, and safe failure.

This is an example boundary, not text learners must copy. Equivalent wording is acceptable when it
preserves the mechanism and produces inspectable evidence.

## Common mistakes

- Repeating lesson definitions without applying them to an input, branch, output, or test.
- Producing one happy-path prompt and mentioning the edge case only in prose.
- Treating model confidence as proof or describing provider behavior without current evidence.
- Claiming that a prompt enforces permissions, schemas, privacy, or execution isolation.
- Omitting a limitation because it would make the portfolio or evaluation look weaker.

## Rubric interpretation

Scores of 3 show competent, explicit application. Scores of 4 or 5 require connected trade-offs:
the learner explains how evidence, authority, uncertainty, cost, or operational controls interact.
A total above 18 cannot compensate for a row below 3. Invented evidence, unauthorized action,
concealed uncertainty, or sensitive data fails the submission and requires revision.

## Acceptable alternatives

Multiple answers may be correct when the submission states its assumptions. Clarification,
abstention, structured unknowns, or escalation can each fit an ambiguous case depending on risk and
available tools. Different output formats are acceptable if they remain testable. A learner may
choose stricter controls than the example and explain the cost.

## Failing responses

A response fails when it merely rewrites the baseline more fluently, ignores one supplied case,
uses an unverified external fact, executes or recommends an unauthorized action, or reports that it
is accurate without observable checks. It also fails if every case produces the same answer despite
materially different evidence or authority.

## Quiz answers and explanations

1. **B.** Success criteria and datasets is demonstrated by an observable decision or control: Criteria translate user value and risk into observable behavior. Representative datasets include frequent traffic, important minorities, and realistic distribution shifts. Length, confidence, or undocumented assumptions do not establish the mechanism.

2. **B.** Case families is demonstrated by an observable decision or control: Normal cases establish baseline utility; edge cases probe ambiguous boundaries; adversarial cases test misuse and unsafe content without becoming an offensive collection. Length, confidence, or undocumented assumptions do not establish the mechanism.

3. **B.** Golden data and assertions is demonstrated by an observable decision or control: Golden datasets contain reviewed expectations. Deterministic assertions check facts such as schema validity, citation presence, allowed labels, and forbidden leakage. Length, confidence, or undocumented assumptions do not establish the mechanism.

4. **B.** Human rubrics is demonstrated by an observable decision or control: Rubrics define dimensions and anchored scores for qualities that code cannot fully judge, such as helpfulness, evidence use, or calibrated uncertainty. Length, confidence, or undocumented assumptions do not establish the mechanism.

5. **Scenario answer.** Two valid checks must be specific to Evaluation: one should verify the
normal output's decisive evidence or structure, and another should verify a boundary behavior.
Generic claims such as “clear and professional” receive no credit.

6. **Edge-case answer.** Two prompts have equal rubric averages, but one is twice as slow and has a single critical unsupported-policy failure. A correct answer identifies what cannot safely be assumed
and chooses clarify, labeled assumption, abstention, structured unknown, or escalation based on
consequence. More than one branch is acceptable when its boundary is explicit and testable.

7. **Error-identification answer.** The bad example lacks a decision rule, evidence or input
boundary, missing-information behavior, and acceptance criteria. Credit any three defects that are
explained through their likely failure rather than merely listed.

8. **Design answer.** For `A candidate output embeds language intended to influence an automated judge.`, the response must preserve trusted authority,
avoid the unsafe or unsupported behavior, and expose the event for review. A prompt control can
classify and delimit untrusted content; an application control must enforce capability, validation,
sandbox, or approval boundaries outside natural-language persuasion.
