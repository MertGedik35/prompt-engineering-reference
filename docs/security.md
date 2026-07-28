# Security

This repository covers prompt and agent risks without adding harmful jailbreak
libraries or leaked proprietary prompt collections.

Covered areas:

- Direct prompt injection.
- Indirect prompt injection.
- Tool abuse.
- Data exfiltration.
- Secret exposure.
- Excessive agency.
- Untrusted retrieved content.
- Output validation.
- Human approval.
- Least privilege.
- Sandboxing.
- Audit trails.

The baseline control is simple: separate untrusted content from instructions, limit
tool authority, validate outputs before use, and require human approval for sensitive
actions.
