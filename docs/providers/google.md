# Google Gemini

Catalog ID: `provider-google`

## Scope

- Gemini API prompts that combine text with image or document evidence and require explicit source
  priority.
- Gemini Structured Outputs and function declarations used for typed extraction or application
  tools.

This guide uses a multimodal invoice workflow to show where prompt instructions end and schema,
visual-quality checks, and tool authorization begin.

## Do not use this guide for

- Vertex AI product configuration, regional availability, pricing, quotas, and certification
  guidance.
- Unverified assumptions about media limits, thinking behavior, or feature parity across Gemini
  models.

Current supported inputs and schema features must be read from the official Gemini pages. They are
not durable characteristics of a provider name.

## Stable guidance

- Assign each media item a purpose and define what to do when visual evidence is unreadable or
  conflicts with text.
- Use a response schema for extraction, while retaining semantic validation for values the schema
  cannot prove.
- Test both tool-call and no-tool paths because application code, not the model, performs the
  external operation.

An image is not merely a large string of context. The prompt should state whether it is primary
evidence, corroboration, or presentation material and should allow the model to mark an unreadable
region.

## Provider-specific prompt behavior

- Order multimodal parts deliberately and refer to the relevant image or document unambiguously in
  the instruction.
- Design Structured Outputs against Gemini's documented JSON Schema subset rather than assuming
  arbitrary schema support.
- Translate a Gemini function call into an authorized application action, then provide only the
  necessary result back to the model.

Gemini's prompting guidance describes an iterative design process and multimodal use. Structured
Outputs and function calling are separate provider features: the first constrains a response
shape, while the second asks the application to invoke a declared operation.

## Relevant platform features

For typed extraction, the response schema should express stable fields such as invoice number,
currency, and line items. Cross-field arithmetic, supplier identity, and evidence location still
need domain checks. When an image conflicts with accompanying OCR, the prompt should make source
priority explicit or return a conflict rather than silently choosing one.

A Gemini function declaration is not an executable credential. The host maps the call to a
permitted operation, verifies the signed-in account, validates arguments, and controls any side
effect. The result returned to Gemini should omit unrelated account data.

## Minimal provider-aware example

The fictional Pinecone Bakery submits one invoice image and a short operator note:

```text
Input A is the invoice image and is the primary source for printed amounts.
Input B is the operator note and may explain handwriting, but it cannot replace a printed value.

Extract invoice_number, currency, subtotal, tax, total, and unreadable_regions.
If a value is obscured, return null for that value and describe its location.
If subtotal plus tax does not equal total, report a conflict instead of repairing the number.
```

The application provides a Gemini-compatible response schema and checks the arithmetic itself.
The example does not claim successful extraction from a live Gemini call.

## Production-oriented example

After extraction, the application may expose a read-only `get_delivery_status` function. The
function accepts an internal delivery reference that the host mapped from the authenticated
bakery account; it does not accept a customer ID invented from the image. Gemini can request the
status when the invoice mentions a delivery discrepancy. The host decides whether the tool is
available, checks ownership, executes it, and returns status plus an event timestamp.

The final record contains extracted fields, image-region evidence, arithmetic validation, and any
authorized delivery result. It routes unreadable totals, supplier mismatches, duplicate invoice
numbers, and conflicting OCR to a human queue. A regression pack includes clean scans, rotated
pages, handwriting, multiple currencies, no-tool cases, prompt injection printed on the invoice,
and attempted access to another fictional bakery.

## Evaluation and portability checks

- The invoice workflow reports unreadable visual regions instead of inventing field values.
- Every extracted amount is checked against the declared Gemini response schema and a
  business-rule validator.
- The delivery-status function cannot expose another fictional account because authorization
  occurs outside the prompt.
- Port the logical contract before porting schema syntax: compare media ordering, supported schema
  keywords, tool-call representation, and conflict behavior for every target runtime.

## Fast-stale claims

| Area | Why it can change | Source | Verified |
| --- | --- | --- | --- |
| Gemini multimodal prompting recommendations | Supported media behavior and recommended prompt patterns evolve with Gemini capabilities. | `official-gemini-prompting` | 2026-07-31 |
| Gemini Structured Outputs schema subset | Schema keyword support and compatible models are versioned provider behavior. | `official-gemini-structured-output` | 2026-07-31 |
| Function-calling modes and composition | Function-calling controls and supported combinations can change in the API. | `official-gemini-function-calling` | 2026-07-31 |

## Official sources

- [`official-gemini-prompting` — Gemini prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [`official-gemini-structured-output` — Gemini Structured Outputs](https://ai.google.dev/gemini-api/docs/structured-output)
- [`official-gemini-function-calling` — Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling)

## Known limitations and unverified areas

- The image-plus-invoice example has not been run against Gemini with degraded or rotated scans.
- This repository has not measured portability between Gemini Structured Outputs and another
  provider's schema subset.

## Last verified

2026-07-31
