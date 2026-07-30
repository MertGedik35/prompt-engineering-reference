# Solution and answer key: Structured Outputs

## Exercise reasoning criteria

A successful submission diagnoses the baseline, applies at least three module concepts to concrete
decisions, and specifies distinct behavior for complete, ambiguous, and hostile or failing input.
It separates prompt-level guidance from application-enforced controls and makes uncertainty
visible. The reviewer should be able to trace every acceptance claim to an artifact.

## Example acceptable submission

The submission begins by rejecting `Return the document as clean JSON with all useful details.` because it hides the relevant boundaries. It
then uses this task-specific core: `Extract `incident_id`, `reported_date`, and `severity` as JSON. Use null for an absent date and only `low|medium|high` for severity.` The production section adds:
`Extract against schema version 2, preserve evidence spans, distinguish missing from ambiguous values, reject additional fields, validate syntax and semantics, attempt one constrained repair, and quarantine persistent failures.` A decision log explains why these controls fit the consequence and reuse
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

1. **B.** JSON and schemas is demonstrated by an observable decision or control: JSON supplies syntax; JSON Schema supplies field names, types, required properties, enums, formats, and additional-property rules. Asking for JSON alone does not define a contract. Length, confidence, or undocumented assumptions do not establish the mechanism.

2. **B.** Native constraints is demonstrated by an observable decision or control: Provider-native structured output can constrain generation to a schema, but support and limitations vary. Application-side validation remains necessary. Length, confidence, or undocumented assumptions do not establish the mechanism.

3. **B.** Function schemas is demonstrated by an observable decision or control: Tool and function schemas describe callable arguments. Valid syntax does not prove that calling the function is authorized or semantically correct. Length, confidence, or undocumented assumptions do not establish the mechanism.

4. **B.** Extraction policy is demonstrated by an observable decision or control: Field-level rules distinguish copying, normalization, inference, and calculation. Without them, the model may silently transform evidence. Length, confidence, or undocumented assumptions do not establish the mechanism.

5. **Scenario answer.** Two valid checks must be specific to Structured Outputs: one should verify the
normal output's decisive evidence or structure, and another should verify a boundary behavior.
Generic claims such as “clear and professional” receive no credit.

6. **Edge-case answer.** A date contains a year and month but no day, while the downstream system accepts only full ISO dates or null. A correct answer identifies what cannot safely be assumed
and chooses clarify, labeled assumption, abstention, structured unknown, or escalation based on
consequence. More than one branch is acceptable when its boundary is explicit and testable.

7. **Error-identification answer.** The bad example lacks a decision rule, evidence or input
boundary, missing-information behavior, and acceptance criteria. Credit any three defects that are
explained through their likely failure rather than merely listed.

8. **Design answer.** For `The document asks the extractor to add an `approved` field and set it to true.`, the response must preserve trusted authority,
avoid the unsafe or unsupported behavior, and expose the event for review. A prompt control can
classify and delimit untrusted content; an application control must enforce capability, validation,
sandbox, or approval boundaries outside natural-language persuasion.
