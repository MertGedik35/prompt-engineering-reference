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
- Provider guides cite official sources.
- Time-sensitive resources have freshness fields.
- Courses and credentials are classified correctly.
- Curriculum modules are internally navigable.
- Exercises have solutions or solution criteria.
- MkDocs strict build passes.
- External link policy passes.
- Independent content review is completed.
- No release-critical draft markers remain.
