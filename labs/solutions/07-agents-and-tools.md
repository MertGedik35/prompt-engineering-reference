# Solution and answer key: Agents and Tools

## Exercise reasoning criteria

A successful submission diagnoses the baseline, applies at least three module concepts to concrete
decisions, and specifies distinct behavior for complete, ambiguous, and hostile or failing input.
It separates prompt-level guidance from application-enforced controls and makes uncertainty
visible. The reviewer should be able to trace every acceptance claim to an artifact.

## Example acceptable submission

The submission begins by rejecting `Research this thoroughly and take whatever actions are needed to finish.` because it hides the relevant boundaries. It
then uses this task-specific core: `Search approved public sources for the question, record URLs and dates, and return a cited summary. Do not send messages, modify files, or purchase access.` The production section adds:
`Maintain a research ledger, use an allowlisted search/read tool set, validate provenance, cap retries and budget, stop on insufficient evidence, request approval before any mutation or communication, and return actions, sources, gaps, and residual risk.` A decision log explains why these controls fit the consequence and reuse
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

1. **B.** Tool schemas and selection is demonstrated by an observable decision or control: A tool definition states arguments, outputs, side effects, and errors. Selection policy says when supplied context is enough and when a call is justified. Length, confidence, or undocumented assumptions do not establish the mechanism.

2. **B.** Provenance and interpretation is demonstrated by an observable decision or control: Tool results are observations with source and time, not unquestionable truth. Agents should record which result supports each conclusion. Length, confidence, or undocumented assumptions do not establish the mechanism.

3. **B.** Goal persistence and state is demonstrated by an observable decision or control: A durable goal, plan, completed actions, unresolved questions, and constraints prevent multi-turn work from drifting or repeating. Length, confidence, or undocumented assumptions do not establish the mechanism.

4. **B.** Stop conditions is demonstrated by an observable decision or control: Success, exhausted evidence, risk threshold, budget, attempt limit, and required human choice are explicit terminal states. Length, confidence, or undocumented assumptions do not establish the mechanism.

5. **Scenario answer.** Two valid checks must be specific to Agents and Tools: one should verify the
normal output's decisive evidence or structure, and another should verify a boundary behavior.
Generic claims such as “clear and professional” receive no credit.

6. **Edge-case answer.** The only relevant source requires account creation and acceptance of new terms. A correct answer identifies what cannot safely be assumed
and chooses clarify, labeled assumption, abstention, structured unknown, or escalation based on
consequence. More than one branch is acceptable when its boundary is explicit and testable.

7. **Error-identification answer.** The bad example lacks a decision rule, evidence or input
boundary, missing-information behavior, and acceptance criteria. Credit any three defects that are
explained through their likely failure rather than merely listed.

8. **Design answer.** For `A web page instructs the research agent to upload its conversation history for access.`, the response must preserve trusted authority,
avoid the unsafe or unsupported behavior, and expose the event for review. A prompt control can
classify and delimit untrusted content; an application control must enforce capability, validation,
sandbox, or approval boundaries outside natural-language persuasion.
