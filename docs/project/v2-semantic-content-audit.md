# V2 Semantic Content Audit

Last audited: 2026-07-30  
Branch baseline: `feat/v2-learning-reference` at `c8a7ab9eccb6260590d745f8b946c1906397f64d`

## Method

This audit was performed independently of the existing quality script. It combines file and
record counts, normalized-text comparison, word counts, structural inspection, and manual
sampling. Normalization lowercases text and removes punctuation and topic identifiers; it
therefore exposes files whose only meaningful difference is a module name.

## Executive finding

The V2 information architecture is useful, but the checked-in source does not yet support the
claim that the curriculum and catalogs are substantively complete. The 13 module entry lessons
contain only 21–25 words each. Every exercise repeats the same task, every quiz has three shallow
questions, and every solution uses the same one-sentence criterion with a substituted topic.
Catalog records are longer, but patterns and templates still share semantic operating skeletons.
The current quality check examines only selected JSON fields and cannot detect these Markdown
failures. This is a release blocker.

## Inventory and findings

| Area | Count | Duplication and depth | Teaching / reuse finding | Sources | Severity | Required remediation |
| --- | ---: | --- | --- | --- | --- | --- |
| `curriculum/**` | 65 Markdown files; 13 main lessons | 1,153 words total; 12 normalized duplicate files; main lessons are 21–25 words; quizzes have 3 questions each | Describes module names but does not teach them. Exercises, quizzes, and checklists are title substitutions and cannot be used as assessments. | Thin `references.md` files exist, but claims are not integrated into lessons. | Critical | Rewrite all 13 lessons, exercises, quizzes, references, and checklists with module-specific examples, rubrics, and sources. |
| `docs/learn/**` | 14 files | 5,859 words total; files are not exact duplicates, but share a repeated section frame and broad prose | Provides an outline-level introduction. Most pages lack worked decisions, bad-to-improved examples, scoring rubrics, and sufficiently distinct practice. | Links are present but coverage varies. | High | Make the curriculum lesson the substantive source and keep Learn pages as navigable companions without duplicating whole lessons. |
| `labs/exercises/**` | 1 index file | 10 words | Merely points to curriculum; no standalone exercises live here. | Not applicable. | Low | Retain as an index, but link all 13 substantive curriculum exercises. |
| `labs/quizzes/**` | 1 index file | 10 words | Merely points to curriculum. | Not applicable. | Low | Retain as an index, but link all 13 substantive quizzes. |
| `labs/solutions/**` | 13 files | 261 words total | Each file is a one-sentence acceptance statement. There is no expected reasoning, example response, common mistake, rubric interpretation, acceptable alternatives, or explicit failure case. | Not applicable. | Critical | Write one explanatory solution and answer key per module. |
| `catalog/patterns.json` | 26 records | IDs and examples vary, but `use_when`, `avoid_when`, acceptance, failure, and verification frequently use the same abstract wording | Many bad prompts are artificial rather than realistic failures. Verification rarely defines normal, edge, and failure cases with measurable behavior. | Related lessons exist; external provenance is uneven. | Critical | Rewrite all mechanism-bearing fields and add three measurable verification cases per pattern. |
| `catalog/templates.json` | 28 records | Titles and variables differ, while prompts share a generic staged instruction skeleton | A user must still design important task logic. Records lack minimal/production variants, worked I/O, test cases, adaptation, and privacy/provider guidance. | References are not first-class fields. | Critical | Expand schema and every record; require task-specific production workflows and normal/edge tests. |
| `catalog/prompt_contracts.json` | 8 records | Variants are intentionally related but insufficiently differentiated by risk and operating context | Useful reference framing, but needs to be checked by Markdown-aware validation and tied to the anatomy lesson. | No material source problem found in sampling. | Medium | Add semantic checks and preserve only distinctions that change required evidence, authority, or evaluation. |
| `catalog/courses.json` | 7 records | No exact duplicates | Anthropic tutorial is incorrectly presented as a completion certificate; Microsoft Learn achievement language is conflated with a course certificate. Important official offerings are missing. | Some canonical links exist, but credential assertions are not consistently supported. | Critical | Reverify every mutable claim against official pages; use `unknown` where silent; add the requested official offerings. |
| `catalog/credentials.json` | 5 records | No exact duplicates | The Microsoft Applied Skills directory is counted as an individual credential. Taxonomy cannot cleanly express directories or profile achievements. | Canonical links exist but classification is misleading. | Critical | Extend taxonomy, move directory records out of individual counts, and add only verified individual credentials. |
| `catalog/provider-guides.json` | 8 records | No exact duplicates; common record shape is expected | Records summarize providers. They do not function as operational references for hierarchy, schemas, tools, grounding, migration, caching, security, courses, and stale-risk boundaries. | Official links exist but do not cover every claim or fast-stale area. | High | Expand all eight guides and explicitly mark unsupported or unverified features. |
| `docs/providers/**` | 9 files | 2,322 words total | Pages are summaries rather than complete provider references; feature support and migration boundaries are too shallow. | Official sources are present but incomplete. | High | Add the required operational sections, canonical sources, gaps, and verification date. |
| `providers/**` | 8 files | 54 words total | These are source stubs that redirect to docs; they do not independently teach. | Not applicable. | Medium | Either make their source role explicit or consolidate without breaking architecture. |
| `reference/**` | 6 files | 82 words total | Primarily pointers to generated catalogs; little directly usable decision support exists. | Derived catalog links are not a substitute for authoritative sourcing. | High | Add concise usage guidance and ensure generated records carry all operational assets. |
| `resources/**` | 10 files | 102 words total | Index stubs only. | Sourcing quality depends entirely on catalogs. | Medium | Keep indexes thin, but make taxonomy and verification semantics explicit. |

## Required semantic checks

The existing `scripts/check_content_quality.py` loads only patterns and templates. It checks exact
normalized blocks in a few fields, sequence similarity for one prompt field, and a 250-character
template minimum. It does not read curriculum, Learn pages, exercises, quizzes, solutions,
provider Markdown, or reference Markdown. It also does not report paragraph duplication, shared
n-grams, missing headings, question counts, lesson depth, repeated readings, or structural
fingerprints. Consequently it passes content that is demonstrably shallow.

The replacement must print file paths and similarity scores, enforce required headings and useful
minimum depths, compare examples separately, detect repeated quiz questions and solution prose,
and inspect both minimal and production template prompts. Thresholds must be documented and tests
must include deliberately shallow fixtures.

## Explicit qualitative conclusions

- Lesson examples are reused at the conceptual level across unrelated Learn pages, while main
  lessons contain no meaningful examples at all.
- All 13 exercises differ primarily by module title and repeat “Rewrite a weak prompt”.
- Three-question quizzes cannot assess the specified module knowledge and repeat generic prompts.
- Solutions do not contain answer criteria beyond one universal sentence.
- Pattern bad examples and failure modes frequently describe the requested pattern by name instead
  of exhibiting its real failure mechanism.
- Template prompts contain category nouns but not enough task-specific decision logic to be
  production assets.
- Course and credential claims are not sufficiently supported for publication.
- Provider guides are readable summaries, not daily operational references.

## Remediation order

1. Rewrite curriculum practice and solutions so learning outcomes are assessable.
2. Deepen the 13 lessons and integrate authoritative sources.
3. Expand template schema and task-specific records.
4. Rewrite pattern mechanisms and measurable verification cases.
5. Correct courses, credentials, and provider guides using current official sources.
6. Replace the content-quality checker and add regression tests.
7. Regenerate derived docs, run privacy and full validation, and revise the draft PR report.

