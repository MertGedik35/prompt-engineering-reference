# Prompt Contract

The Prompt Contract is the shared structure used across patterns and templates.

## Versions

| Version | Use |
| --- | --- |
| Minimal | Small one-off tasks. |
| Standard | Reusable prompts. |
| Production | Product or operational prompts. |
| Coding-agent | Repository tasks with tools and tests. |
| Long-document | Large document analysis with provenance. |
| Tool-using agent | Agents with explicit authority and approval rules. |

## Dimensions

- Objective: the outcome the model must produce.
- Context: background needed to interpret the task.
- Inputs: data the model should transform or inspect.
- Instructions: steps, priorities, and decisions.
- Constraints: limits on scope, style, safety, cost, or authority.
- Tools and Sources: allowed tools, source hierarchy, and citation rules.
- Output Contract: exact format and required fields.
- Evaluation: acceptance criteria, test cases, and scoring rubric.
