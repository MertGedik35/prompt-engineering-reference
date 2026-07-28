# Pattern Index

Generated from `catalog/patterns.json`.

| ID | Name | Summary |
| --- | --- | --- |
| `pattern-direct-instruction-framing` | Direct instruction framing | State the task, audience, and success condition in the first lines. |
| `pattern-context-boundary-marking` | Context boundary marking | Separate instructions, trusted context, untrusted context, and input data with clear labels. |
| `pattern-role-responsibility-framing` | Role and responsibility framing | Define the assistant's job, authority, and refusal boundary without adding theatrical personas. |
| `pattern-output-contract-first` | Output contract first | Specify format, fields, ordering, and validation rules before examples or data. |
| `pattern-few-shot-calibration` | Few-shot calibration | Use compact examples to calibrate tone, structure, and edge-case handling. |
| `pattern-positive-constraints` | Positive constraint rewrite | Replace broad negative rules with concrete desired behavior and allowed alternatives. |
| `pattern-decomposition-planning` | Decomposition planning | Ask the model to break complex work into auditable stages before execution. |
| `pattern-checkpointed-execution` | Checkpointed execution | Add stopping points for review when the task changes files, spends money, or uses tools. |
| `pattern-retrieval-grounded-answering` | Retrieval-grounded answering | Force answers to use supplied sources and label unsupported claims. |
| `pattern-citation-before-answer` | Citation before answer | Have the model collect evidence snippets before synthesizing a response. |
| `pattern-clarify-or-proceed-policy` | Clarify-or-proceed policy | Define when to ask a question and when to continue with stated assumptions. |
| `pattern-assumption-ledger` | Assumption ledger | Record uncertain assumptions separately from verified facts. |
| `pattern-decision-matrix` | Decision matrix | Compare options with criteria, weights, evidence strength, and tradeoffs. |
| `pattern-rubric-driven-critique` | Rubric-driven critique | Evaluate outputs against a named rubric before revising. |
| `pattern-diff-explained-rewrite` | Diff-explained rewrite | When rewriting, show what changed and why without restating the whole source. |
| `pattern-acceptance-self-check` | Acceptance self-check | Make the model verify final output against explicit acceptance criteria. |
| `pattern-tool-selection-policy` | Tool selection policy | Define which tools are allowed, when they are required, and when approval is needed. |
| `pattern-tool-result-provenance` | Tool result provenance | Keep tool outputs traceable to source, timestamp, and transformation. |
| `pattern-long-document-map-reduce` | Long-document map-reduce | Process large inputs in chunks, then merge with conflict handling. |
| `pattern-state-handoff-summary` | State handoff summary | Create compact state summaries that preserve decisions, open items, and evidence. |
| `pattern-delegation-contract` | Multi-agent delegation contract | Give subagents bounded goals, inputs, outputs, and review requirements. |
| `pattern-safe-refusal-alternative` | Safe refusal with allowed alternative | Refuse disallowed requests while offering a useful safe path. |
| `pattern-schema-bound-extraction` | Schema-bound extraction | Extract data only into a declared schema with null and uncertainty rules. |
| `pattern-error-recovery-prompt` | Error recovery prompt | Recover from failed outputs by identifying the violated contract and retrying narrowly. |
| `pattern-prompt-compression` | Prompt compression | Compress long instructions while preserving priority, constraints, and evidence. |
| `pattern-eval-case-generation` | Eval case generation | Generate representative, adversarial, and regression test cases from success criteria. |
