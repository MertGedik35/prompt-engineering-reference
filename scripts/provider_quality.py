from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from itertools import combinations
from pathlib import Path
from typing import Any

try:
    from .check_freshness import utc_today
except ImportError:  # pragma: no cover - used when run as a script
    from check_freshness import utc_today  # type: ignore[import-not-found,no-redef]

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PROVIDERS = {
    "provider-openai": "openai",
    "provider-anthropic": "anthropic",
    "provider-google": "google",
    "provider-microsoft": "microsoft",
    "provider-aws": "aws",
    "provider-meta": "meta",
    "provider-mistral": "mistral",
    "provider-open-models": "open-models",
}
REQUIRED_HEADINGS = (
    "Scope",
    "Do not use this guide for",
    "Stable guidance",
    "Provider-specific prompt behavior",
    "Relevant platform features",
    "Minimal provider-aware example",
    "Production-oriented example",
    "Evaluation and portability checks",
    "Fast-stale claims",
    "Official sources",
    "Known limitations and unverified areas",
    "Last verified",
)
INDEX_HEADINGS = (
    "Stable guidance and fast-stale claims",
    "Where to start",
    "Supported is not tested here",
    "Portability checklist",
    "Repository boundary",
)
PROVIDER_MIN_WORDS = 450
INDEX_MIN_WORDS = 300

# Seven-token shingles ignore unavoidable shared headings but expose copied explanatory prose.
# 0.38 means more than a third of all distinct seven-word sequences are shared, which is too high
# for guides whose products, boundaries, examples, and failure modes are intentionally different.
PROVIDER_SHINGLE_SIZE = 7
PROVIDER_SIMILARITY_LIMIT = 0.38
LONG_PARAGRAPH_WORDS = 35
GENERIC_PHRASES = (
    "provider guidance goes here",
    "check the official docs for details",
    "this section will be expanded",
    "generic provider example",
)
PROVIDER_SOURCE_LESSONS = {
    "official-openai-prompt-engineering": {
        "02-prompt-anatomy",
        "08-context-engineering",
    },
    "official-openai-structured-outputs": {"05-structured-outputs"},
    "official-openai-function-calling": {"07-agents-and-tools"},
    "official-openai-evals": {"06-evaluation", "11-production-operations"},
    "official-claude-prompting-overview": {"02-prompt-anatomy", "06-evaluation"},
    "official-claude-tool-use": {"07-agents-and-tools"},
    "official-claude-code-prompts": {
        "02-prompt-anatomy",
        "11-production-operations",
    },
    "official-gemini-prompting": {
        "02-prompt-anatomy",
        "04-grounding-and-long-context",
        "10-multimodal",
    },
    "official-gemini-structured-output": {"05-structured-outputs"},
    "official-gemini-function-calling": {"07-agents-and-tools"},
    "official-azure-prompt-engineering": {
        "02-prompt-anatomy",
        "04-grounding-and-long-context",
    },
    "official-azure-function-calling": {"07-agents-and-tools", "09-security"},
    "official-copilot-prompt-gallery": {"02-prompt-anatomy"},
    "official-bedrock-prompt-guidelines": {
        "02-prompt-anatomy",
        "08-context-engineering",
    },
    "official-bedrock-agents": {"07-agents-and-tools", "11-production-operations"},
    "official-bedrock-guardrails": {"09-security"},
    "official-llama-docs": {"02-prompt-anatomy", "11-production-operations"},
    "repo-meta-llama-cookbook": {
        "02-prompt-anatomy",
        "07-agents-and-tools",
        "11-production-operations",
    },
    "official-llama-prompt-format": {
        "02-prompt-anatomy",
        "07-agents-and-tools",
        "11-production-operations",
    },
    "official-mistral-prompting": {"02-prompt-anatomy"},
    "official-mistral-function-calling": {"07-agents-and-tools"},
    "official-mistral-structured-output": {"05-structured-outputs"},
    "official-huggingface-chat-templates": {
        "02-prompt-anatomy",
        "08-context-engineering",
        "11-production-operations",
    },
    "official-vllm-quantization": {"11-production-operations"},
    "official-vllm-openai-compatible-server": {
        "07-agents-and-tools",
        "11-production-operations",
    },
    "repo-llamaindex": {
        "04-grounding-and-long-context",
        "07-agents-and-tools",
        "08-context-engineering",
    },
}


def load_records(root: Path, path: str) -> list[dict[str, Any]]:
    data = json.loads((root / path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise TypeError(f"{path} must contain a list")
    return [record for record in data if isinstance(record, dict)]


def normalize(value: object) -> str:
    text = (
        json.dumps(value, ensure_ascii=False, sort_keys=True)
        if not isinstance(value, str)
        else value
    )
    text = re.sub(r"https?://\S+", " ", text.lower())
    text = re.sub(r"[`*_#|<>{}\[\]():,.;/\\\"']", " ", text)
    return " ".join(text.split())


def headings(text: str) -> set[str]:
    return {
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE)
    }


def section(text: str, name: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(name)}\s*$\n(.*?)(?=^##\s+|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def word_count(text: str) -> int:
    without_code = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    without_links = re.sub(r"https?://\S+", " ", without_code)
    return len(re.findall(r"\b[\w'-]+\b", without_links, flags=re.UNICODE))


def _identity_normalized(record: dict[str, Any], text: str) -> str:
    value = text.lower()
    for identity in (
        str(record.get("id", "")),
        str(record.get("slug", "")),
        str(record.get("name", "")),
        str(record.get("provider", "")),
    ):
        if identity:
            value = value.replace(identity.lower(), " provider ")
    value = re.sub(r"https?://\S+", " source-url ", value)
    value = re.sub(r"\b(?:official|repo)-[a-z0-9-]+\b", " source-id ", value)
    value = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", " verification-date ", value)
    return normalize(value)


def _shingles(text: str) -> set[tuple[str, ...]]:
    words = text.split()
    return {
        tuple(words[index : index + PROVIDER_SHINGLE_SIZE])
        for index in range(len(words) - PROVIDER_SHINGLE_SIZE + 1)
    }


def similarity(left: str, right: str) -> float:
    left_shingles = _shingles(left)
    right_shingles = _shingles(right)
    if not left_shingles or not right_shingles:
        return 0.0
    return len(left_shingles & right_shingles) / len(left_shingles | right_shingles)


def _duplicate_field_errors(
    providers: list[dict[str, Any]],
    field_name: str,
) -> list[str]:
    seen: dict[str, str] = {}
    errors: list[str] = []
    for record in providers:
        provider_id = str(record.get("id", "<missing-id>"))
        value = normalize(record.get(field_name, []))
        if value and value in seen:
            errors.append(f"duplicate provider {field_name}: {seen[value]} ~ {provider_id}")
        elif value:
            seen[value] = provider_id
    return errors


def provider_record_errors(
    providers: list[dict[str, Any]],
    resources: dict[str, dict[str, Any]],
    *,
    as_of: date,
    enforce_inventory: bool = True,
) -> list[str]:
    errors: list[str] = []
    actual = {str(record.get("id", "")): str(record.get("slug", "")) for record in providers}
    if enforce_inventory and actual != EXPECTED_PROVIDERS:
        errors.append(
            "provider inventory mismatch: "
            f"expected={sorted(EXPECTED_PROVIDERS.items())} actual={sorted(actual.items())}"
        )

    errors.extend(_duplicate_field_errors(providers, "acceptance_criteria"))
    errors.extend(_duplicate_field_errors(providers, "remaining_gaps"))
    for record in providers:
        provider_id = str(record.get("id", "<missing-id>"))
        official_ids = record.get("official_source_ids", [])
        supporting_ids = record.get("supporting_source_ids", [])
        if not isinstance(official_ids, list) or not isinstance(supporting_ids, list):
            continue
        official_set = {str(source_id) for source_id in official_ids}
        supporting_set = {str(source_id) for source_id in supporting_ids}
        overlap = sorted(official_set & supporting_set)
        if overlap:
            errors.append(f"duplicate official/supporting source: {provider_id} -> {overlap}")

        for source_id in official_set:
            source = resources.get(source_id)
            if source is None:
                errors.append(f"unresolved official provider source: {provider_id} -> {source_id}")
            elif source.get("official") is not True:
                errors.append(f"non-official source used as official: {provider_id} -> {source_id}")
        for source_id in supporting_set:
            source = resources.get(source_id)
            if source is None:
                errors.append(
                    f"unresolved supporting provider source: {provider_id} -> {source_id}"
                )
            elif source.get("official") is not False:
                errors.append(
                    f"official source misclassified as supporting: {provider_id} -> {source_id}"
                )

        declared_sources = official_set | supporting_set
        for claim in record.get("fast_stale_areas", []):
            if not isinstance(claim, dict):
                continue
            source_id = str(claim.get("source_id", ""))
            if source_id not in declared_sources:
                errors.append(
                    f"fast-stale source is not declared by provider: "
                    f"{provider_id} -> {source_id or '<missing>'}"
                )
            verified_value = str(claim.get("last_verified", ""))
            try:
                verified = date.fromisoformat(verified_value)
            except ValueError:
                errors.append(
                    f"invalid fast-stale verification date: {provider_id} -> {verified_value!r}"
                )
                continue
            if verified > as_of:
                errors.append(
                    f"future fast-stale verification date: {provider_id} -> {verified_value}"
                )

        verified_value = str(record.get("last_verified", ""))
        try:
            verified = date.fromisoformat(verified_value)
        except ValueError:
            errors.append(
                f"invalid provider verification date: {provider_id} -> {verified_value!r}"
            )
        else:
            if verified > as_of:
                errors.append(
                    f"future provider verification date: {provider_id} -> {verified_value}"
                )

    used_source_ids = {
        str(source_id)
        for record in providers
        for field in ("official_source_ids", "supporting_source_ids")
        for source_id in record.get(field, [])
    }
    for source_id in sorted(used_source_ids):
        source = resources.get(source_id)
        if source is None:
            continue
        expected_lessons = PROVIDER_SOURCE_LESSONS.get(source_id)
        if expected_lessons is None:
            errors.append(f"provider source lacks approved lesson mapping: {source_id}")
            continue
        actual_lessons = set(source.get("related_lessons", []))
        if actual_lessons != expected_lessons:
            errors.append(
                f"provider source lesson mapping mismatch: {source_id} -> "
                f"{sorted(actual_lessons)}; expected {sorted(expected_lessons)}"
            )
    return errors


def provider_document_errors(
    record: dict[str, Any],
    resources: dict[str, dict[str, Any]],
    text: str,
) -> list[str]:
    errors: list[str] = []
    provider_id = str(record.get("id", "<missing-id>"))
    relative_path = f"docs/providers/{record.get('slug', '<missing-slug>')}.md"
    if f"Catalog ID: `{provider_id}`" not in text:
        errors.append(f"{relative_path}: catalog ID does not match {provider_id}")
    for heading in REQUIRED_HEADINGS:
        if heading not in headings(text):
            errors.append(f"{relative_path}: missing heading `{heading}`")
    supporting_ids = record.get("supporting_source_ids", [])
    has_supporting_heading = "Supporting sources" in headings(text)
    if supporting_ids and not has_supporting_heading:
        errors.append(f"{relative_path}: supporting sources exist but heading is missing")
    if not supporting_ids and has_supporting_heading:
        errors.append(f"{relative_path}: empty supporting sources section is not allowed")

    expected_date = str(record.get("last_verified", ""))
    if section(text, "Last verified") != expected_date:
        errors.append(
            f"{relative_path}: last-verified mismatch; "
            f"catalog={expected_date!r} doc={section(text, 'Last verified')!r}"
        )
    normalized_doc = normalize(text)
    synchronized_fields = (
        "scope",
        "out_of_scope",
        "stable_guidance",
        "provider_specific_guidance",
        "remaining_gaps",
        "acceptance_criteria",
    )
    for field_name in synchronized_fields:
        for item in record.get(field_name, []):
            if normalize(item) not in normalized_doc:
                errors.append(
                    f"{relative_path}: catalog {field_name} item is missing from document: "
                    f"{str(item)[:80]}"
                )

    for field_name in ("official_source_ids", "supporting_source_ids"):
        for source_id in record.get(field_name, []):
            source = resources.get(str(source_id))
            if str(source_id) not in text:
                errors.append(f"{relative_path}: catalog source ID is missing: {source_id}")
            if source is not None:
                url = str(source.get("canonical_url", ""))
                if f"]({url})" not in text:
                    errors.append(
                        f"{relative_path}: canonical source URL is missing: {source_id} -> {url}"
                    )

    fast_section = normalize(section(text, "Fast-stale claims"))
    for claim in record.get("fast_stale_areas", []):
        if not isinstance(claim, dict):
            continue
        for field_name in ("area", "why_stale", "source_id", "last_verified"):
            value = normalize(claim.get(field_name, ""))
            if not value or value not in fast_section:
                errors.append(
                    f"{relative_path}: fast-stale claim lacks {field_name}: "
                    f"{claim.get('area', '<missing-area>')}"
                )

    if word_count(text) < PROVIDER_MIN_WORDS:
        errors.append(
            f"{relative_path}: provider guide words {word_count(text)} < {PROVIDER_MIN_WORDS}"
        )
    lowered = normalize(text)
    for phrase in GENERIC_PHRASES:
        if phrase in lowered:
            errors.append(f"{relative_path}: generic provider filler: {phrase}")
    return errors


def provider_cross_document_errors(
    providers: list[dict[str, Any]],
    documents: dict[str, str],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    details: list[str] = []
    record_by_slug = {str(record.get("slug", "")): record for record in providers}

    examples: dict[str, tuple[str, str]] = {}
    paragraphs: dict[str, str] = {}
    normalized_documents: dict[str, str] = {}
    for slug, text in documents.items():
        record = record_by_slug.get(slug, {"id": slug, "slug": slug, "name": slug})
        normalized_documents[slug] = _identity_normalized(record, text)
        for heading_name in (
            "Minimal provider-aware example",
            "Production-oriented example",
        ):
            value = _identity_normalized(record, section(text, heading_name))
            key = f"{heading_name}:{value}"
            if value and key in examples:
                other_slug, _ = examples[key]
                errors.append(
                    f"duplicate provider example: {other_slug} ~ {slug} section={heading_name}"
                )
            elif value:
                examples[key] = (slug, heading_name)

        for paragraph in re.split(r"\n\s*\n", text):
            value = _identity_normalized(record, paragraph)
            if len(value.split()) < LONG_PARAGRAPH_WORDS:
                continue
            if value in paragraphs:
                errors.append(f"reused long provider paragraph: {paragraphs[value]} ~ {slug}")
            else:
                paragraphs[value] = slug

    max_pair = ("<none>", "<none>", 0.0)
    for left_slug, right_slug in combinations(sorted(normalized_documents), 2):
        score = similarity(
            normalized_documents[left_slug],
            normalized_documents[right_slug],
        )
        if score > max_pair[2]:
            max_pair = (left_slug, right_slug, score)
        if score >= PROVIDER_SIMILARITY_LIMIT:
            errors.append(
                f"high-similarity provider guides: {left_slug} ~ {right_slug} "
                f"score={score:.3f} >= {PROVIDER_SIMILARITY_LIMIT:.2f}"
            )
    details.append(
        "provider guide max seven-token-shingle similarity: "
        f"{max_pair[0]} ~ {max_pair[1]} score={max_pair[2]:.3f} "
        f"limit={PROVIDER_SIMILARITY_LIMIT:.2f}"
    )
    return errors, details


def check_provider_quality(
    root: Path = ROOT,
    *,
    as_of: date | None = None,
) -> tuple[list[str], list[str]]:
    effective_date = as_of or utc_today()
    providers = load_records(root, "catalog/provider-guides.json")
    resources = {
        str(record.get("id", "")): record
        for path in ("catalog/official-resources.json", "catalog/repositories.json")
        for record in load_records(root, path)
    }
    errors = provider_record_errors(providers, resources, as_of=effective_date)
    details: list[str] = []
    documents: dict[str, str] = {}
    for record in providers:
        slug = str(record.get("slug", ""))
        path = root / "docs" / "providers" / f"{slug}.md"
        if not path.exists():
            errors.append(f"missing provider page: docs/providers/{slug}.md")
            continue
        text = path.read_text(encoding="utf-8")
        documents[slug] = text
        errors.extend(provider_document_errors(record, resources, text))
        details.append(
            f"provider docs/providers/{slug}.md words={word_count(text)} "
            f"official_sources={len(record.get('official_source_ids', []))} "
            f"supporting_sources={len(record.get('supporting_source_ids', []))}"
        )

    missing_slugs = sorted(set(EXPECTED_PROVIDERS.values()) - set(documents))
    for slug in missing_slugs:
        if not any(error == f"missing provider page: docs/providers/{slug}.md" for error in errors):
            errors.append(f"missing provider page: docs/providers/{slug}.md")
    cross_errors, cross_details = provider_cross_document_errors(providers, documents)
    errors.extend(cross_errors)
    details.extend(cross_details)

    index_path = root / "docs" / "providers" / "index.md"
    if not index_path.exists():
        errors.append("missing provider index: docs/providers/index.md")
    else:
        index_text = index_path.read_text(encoding="utf-8")
        for heading_name in INDEX_HEADINGS:
            if heading_name not in headings(index_text):
                errors.append(f"docs/providers/index.md: missing heading `{heading_name}`")
        if word_count(index_text) < INDEX_MIN_WORDS:
            errors.append(
                f"docs/providers/index.md: words {word_count(index_text)} < {INDEX_MIN_WORDS}"
            )
        for slug in EXPECTED_PROVIDERS.values():
            if f"({slug}.md)" not in index_text:
                errors.append(f"docs/providers/index.md: missing guide link `{slug}.md`")
        details.append(f"provider docs/providers/index.md words={word_count(index_text)}")

    counts = Counter(str(record.get("id", "")) for record in providers)
    for provider_id, count in counts.items():
        if count > 1:
            errors.append(f"duplicate provider ID: {provider_id}")
    return errors, details


def main() -> int:
    errors, details = check_provider_quality()
    print("\n".join(details))
    if errors:
        print("Provider quality check failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Provider quality check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
