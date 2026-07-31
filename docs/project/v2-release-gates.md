# V2 Release Gates

A future `v2.0.0` release requires:

- Privacy scan passes with no active secrets.
- Makefile works in CI.
- Real JSON Schema validation passes.
- At least 45 meaningful tests pass.
- Every authoritative curriculum lesson contains at least 900 meaningful English words after
  headings, navigation, code fences, tables, and source lists are excluded.
- Every exercise contains at least 300 meaningful words and the required normal, edge, failure,
  rubric, and passing-condition sections.
- Every quiz has at least eight questions, including two scenarios, and an answer-key link.
- Every solution contains at least 500 meaningful words, all required explanatory sections, and
  eight explained answers.
- Normalized exact duplication is forbidden. Lesson five-token-shingle Jaccard similarity must
  remain below `0.72`; the checker reports both paths and the measured score.
- Minimal, production, and bad examples must be distinct across modules. Exercises, quiz
  questions, solutions, and unrelated reading lists must not be normalized duplicates.
- Every prompt pattern must define a distinct mechanism, observable use and avoidance boundaries,
  a realistic good and bad prompt, at least three measurable acceptance criteria, at least three
  pattern-specific failure modes, and exactly one structured normal, edge, and failure
  verification case. Identity-normalized field similarity must remain below the documented
  thresholds in `scripts/check_content_quality.py`.
- `verification_cases` is the sole pattern verification source. The removed legacy `verification`
  projection must not be restored; consumers must read the structured cases directly.
- Pattern `name` is the single display label. A duplicate `title` alias is not part of the pattern
  schema.
- The universal Prompt Contract fields—Objective, Context, Inputs, Instructions, Constraints,
  Tools and Sources, Output Contract, and Evaluation—apply at catalog level and are not repeated
  as identical `prompt_contract_fields` metadata on every pattern.
- Every stable pattern ID must have the semantically approved primary curriculum lesson enforced
  by `PATTERN_PRIMARY_LESSONS`; additional lessons are limited by the maintained adjacency
  taxonomy.
- Every stable template ID must provide one directly copyable minimal prompt and one operational
  production prompt, with structured canonical variables, a machine-readable output contract,
  at least four observable acceptance criteria, at least three structured task-specific failure
  modes, one worked example, and exactly one normal, edge, and failure test case.
- Template prompts must implement their mechanisms directly. Internal `pattern-...` instructions,
  the former four-step universal skeleton, undeclared prompt variables, unused inputs, duplicate
  prompt or evaluation blocks, and identity-normalized prompt similarity at or above the
  documented thresholds in `scripts/check_content_quality.py` are release blockers.
- `variables` is the sole template input-definition source. The removed `required_inputs` and
  `expected_outputs` projections must not return; output requirements live only in the structured
  `output_contract`.
- All 28 stable template IDs must have the approved primary pattern, supporting-pattern allowlist,
  primary curriculum lesson, and additional-lesson allowlist enforced by
  `scripts/template_taxonomy.py`.
- Provider guides cite official sources.
- Time-sensitive resources have freshness fields.
- Courses and credentials are classified correctly.
- Curriculum modules are internally navigable.
- Exercises have solutions or solution criteria.
- MkDocs strict build passes.
- External link policy passes.
- Independent content review is completed.
- No release-critical draft markers remain.
