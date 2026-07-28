# Standard Prompt Contract Example

Objective: Produce a source-grounded answer for a business reader.

Context: The user will provide source excerpts and a decision question.

Inputs: Source excerpts, question, audience, and required output format.

Instructions: Use only supplied excerpts, state assumptions, and keep unsupported
claims out of the answer.

Constraints: Do not invent citations. Mark missing evidence clearly.

Tools and Sources: Use supplied excerpts first. Use external tools only when the
calling workflow explicitly allows them.

Output Contract: Return summary, evidence table, recommendation, and acceptance
check.

Evaluation: Score with the eight-dimension Prompt Quality Rubric.
