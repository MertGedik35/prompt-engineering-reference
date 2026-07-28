# Anthropic Claude

Last verified: 2026-07-28

## Scope

Use this page for Claude prompt engineering, tool-use prompts, and Claude Code prompt resources. Claude-specific behavior is separated from general prompt engineering principles because model, API, and product features change over time.

## Durable Guidance

- Define success criteria before writing the prompt.
- Separate instructions from untrusted documents or user-provided data.
- Give Claude a clear role only when the role changes task behavior; avoid decorative personas.
- Use explicit output requirements, examples, and failure handling for high-stakes workflows.

## Prompt Design Notes

Claude guidance emphasizes iterative prompt development, strong examples, and precise context boundaries. For document-heavy tasks, ask for evidence-backed claims and make "insufficient information" an acceptable outcome.

When adapting Claude Code prompt-library examples, use the task structure and review behavior as inspiration. Do not copy proprietary project prompts or assume a coding-agent prompt transfers to a general assistant unchanged.

## Tools And Agents

Tool-use prompts should describe allowed tools, required inputs, expected result provenance, and stop conditions. The model should not infer hidden permissions from tool names. Human approval should be explicit for filesystem, network, deployment, or account-changing actions.

## Evaluation Guidance

Use a small hand-reviewed eval set for prompt iterations, then expand to regression cases around refusals, unsupported claims, tool misuse, and citation quality. Keep Claude-specific findings dated.

## Official Sources

- [Claude prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) (`official-claude-prompting-overview`)
- [Claude tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) (`official-claude-tool-use`)
- [Claude Code prompt library](https://code.claude.com/docs/en/prompt-library) (`official-claude-code-prompts`)

## Fast-Stale Areas

- Model-specific prompting behavior, extended thinking controls, and Claude Code features.
- Tool schema support and beta API behavior.
- Product UI behavior, plan limits, and workspace controls.

## Remaining Gaps

- This repository has not run live Claude model comparisons.
- Claude Code prompt-library behavior is treated as product-specific, not universal prompting advice.
