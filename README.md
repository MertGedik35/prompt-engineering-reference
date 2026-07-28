# Prompt Engineering Reference

Prompt Engineering Reference is a practical, provider-aware reference for designing,
evaluating, and operating reusable prompts. It combines a Prompt Contract framework,
a pattern catalog, reusable templates, evaluation examples, provider notes, security
controls, and a machine-readable catalog that can be validated locally.

The repository is intentionally more than a prompt collection. Each prompt asset is
connected to acceptance criteria, failure modes, version data, review dates, and
validation scripts so teams can copy a template, adapt it, and test whether it still
meets its contract.

## Positioning

Prompt Engineering Reference uses five layers:

1. Learn: understand the Prompt Contract and the pattern catalog.
2. Choose: select a pattern, template, provider guide, or diagnostic path.
3. Copy: reuse a template with stable variables and expected outputs.
4. Test: score outputs with the rubric and evaluation examples.
5. Operate: apply context engineering, security controls, provenance, and review gates.

This makes the project different from a random prompt collection, a simple awesome
list, a provider-specific tutorial, or a static list of external links. The core unit
is a testable prompt asset, not a clever phrase.

## Five-minute quick start

```bash
python -m pip install -e ".[dev,docs]"
python scripts/validate_catalog.py
python scripts/generate_docs_indexes.py --check
python scripts/check_internal_links.py
python -m pytest
python -m mkdocs build --strict
```

## Choose by what you want to achieve

| Goal | Start here |
| --- | --- |
| Design a prompt from scratch | [Prompt Contract](docs/prompt-contract.md) |
| Pick a reusable technique | [Pattern catalog](docs/patterns.md) |
| Copy a working template | [Template library](docs/templates.md) |
| Improve a failing prompt | [Prompt Doctor](docs/prompt-doctor.md) |
| Compare model providers | [Provider guides](docs/providers/index.md) |
| Build an evaluation habit | [Prompt evaluations](docs/evaluations.md) |
| Manage context in agents | [Context engineering](docs/context-engineering.md) |
| Reduce prompt and tool risk | [Security](docs/security.md) |

## Reader paths

- New practitioner: Prompt Contract, patterns, then templates.
- Product builder: provider guides, context engineering, security, then evals.
- Coding-agent user: coding-agent Prompt Contract, tool-use patterns, and CI examples.
- Maintainer: catalog schemas, validation scripts, contribution guide, and governance.

## Catalog and documentation

The JSON files in `catalog/` are the source of truth. The files in
`docs/generated/` are generated from those catalogs by
`scripts/generate_docs_indexes.py`.

## Validation

The local quality path checks catalog integrity, generated index drift, internal
Markdown links, unit tests, formatting, linting, type checking, and MkDocs output.

## Contributing

Use [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules and the issue forms in
`.github/ISSUE_TEMPLATE/` for structured changes.

## License

Code and automation are MIT licensed. Original documentation, taxonomies, and
templates are dedicated to the public domain under CC0-1.0. External linked
resources keep their own licenses and terms.
