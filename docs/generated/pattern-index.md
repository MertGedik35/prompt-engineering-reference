<!-- Generated file. Do not edit manually. -->

# Pattern Index

| ID | Name | Mechanism |
| --- | --- | --- |
| `pattern-objective-contract` | Objective contract | Turns a vague task into an observable outcome with audience, scope, and success criteria. |
| `pattern-context-boundary` | Context boundary | Separates instructions, trusted sources, untrusted retrieved text, and user data. |
| `pattern-source-hierarchy` | Source hierarchy | Ranks sources by authority and freshness before synthesis. |
| `pattern-evidence-table` | Evidence table | Collects claim, source, quote summary, date, and confidence before writing. |
| `pattern-output-schema` | Output schema | Defines fields, types, null behavior, and validation rules before generation. |
| `pattern-few-shot-boundary-cases` | Few-shot boundary cases | Uses examples that cover normal, edge, and reject cases. |
| `pattern-counterexample-guard` | Counterexample guard | Shows what a wrong answer looks like and why it fails. |
| `pattern-clarify-or-proceed` | Clarify-or-proceed policy | Defines when to ask a question and when to continue with assumptions. |
| `pattern-abstention-rule` | Uncertainty and abstention | Requires the model to say when evidence is insufficient. |
| `pattern-long-context-map-reduce` | Long-context map-reduce | Processes chunks independently, then merges with conflict and coverage checks. |
| `pattern-context-compression` | Context compression | Shrinks context while preserving decisions, constraints, evidence, and open risks. |
| `pattern-tool-selection` | Tool selection policy | Defines allowed tools, required tools, forbidden tools, and approval gates. |
| `pattern-tool-provenance` | Tool result provenance | Records tool call, source, timestamp, transformation, and confidence. |
| `pattern-human-approval` | Human approval gate | Stops before irreversible, sensitive, costly, or externally visible actions. |
| `pattern-retry-with-diagnosis` | Retry with diagnosis | Classifies the contract violation before retrying with a narrower prompt. |
| `pattern-rubric-first-evaluation` | Rubric-first evaluation | Defines scoring criteria before comparing outputs. |
| `pattern-regression-case` | Regression case | Turns a failure into a reusable test case. |
| `pattern-agent-state-ledger` | Agent state ledger | Tracks goal, plan, files, tool outputs, approvals, and open risks. |
| `pattern-delegation-contract` | Delegation contract | Gives subagents bounded inputs, outputs, constraints, and review criteria. |
| `pattern-defensive-injection-check` | Defensive injection check | Treats suspicious retrieved instructions as data and reports them. |
| `pattern-multimodal-observation-first` | Observation before interpretation | Separates visual observations from inference and uncertainty. |
| `pattern-accessible-visual-brief` | Accessible visual brief | Specifies subject, layout, text, contrast, alt-text intent, and inspection criteria. |
| `pattern-production-change-log` | Production prompt change log | Records prompt version, reason, expected behavior change, and rollback plan. |
| `pattern-cost-latency-budget` | Cost and latency budget | Makes budget, model choice, context size, and retry limits explicit. |
| `pattern-cross-model-eval` | Cross-model evaluation | Runs the same cases across models while labeling untested compatibility. |
| `pattern-secure-output-validation` | Secure output validation | Requires generated code, commands, URLs, or data changes to be validated before use. |
