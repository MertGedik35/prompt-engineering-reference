from __future__ import annotations

import json
import re
from collections import Counter
from collections.abc import Sequence
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

# Seven-token shingles are a secondary full-document signal. Example sections use exact
# identity-normalized equality plus three-token Jaccard near-copy.
# Calibration on the eight current guides (global identity normalization, 2026-07-31):
#   legit example-section max j3 ≈ 0.014
#   controlled near-paraphrase fixture j3 ≈ 0.178
#   selected SECTION_NEAR_COPY_LIMIT = 0.12 (margin ≈ 0.10 above legit)
PROVIDER_SHINGLE_SIZE = 7
PROVIDER_SIMILARITY_LIMIT = 0.38
SECTION_NEAR_COPY_SHINGLE_SIZE = 3
SECTION_NEAR_COPY_LIMIT = 0.12
LONG_PARAGRAPH_WORDS = 35
LONG_PARAGRAPH_NEAR_COPY_WORDS = 66
GENERIC_PHRASES = (
    "provider guidance goes here",
    "check the official docs for details",
    "this section will be expanded",
    "generic provider example",
)
EXAMPLE_HEADINGS = (
    "Minimal provider-aware example",
    "Production-oriented example",
)


def curriculum_lesson_ids(root: Path = ROOT) -> set[str]:
    return {path.parent.name for path in (root / "curriculum").glob("*/README.md")}


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


def _identity_aliases(providers: list[dict[str, Any]]) -> list[str]:
    aliases: set[str] = set()
    for record in providers:
        for field_name in ("id", "slug", "name", "provider"):
            value = str(record.get(field_name, "")).strip()
            if value:
                aliases.add(value)
    return sorted(aliases, key=lambda item: (-len(item), item.lower()))


def _identity_normalized(text: str, aliases: Sequence[str]) -> str:
    value = text
    for alias in aliases:
        value = re.sub(re.escape(alias), " provider ", value, flags=re.IGNORECASE)
    value = re.sub(r"https?://\S+", " source-url ", value)
    value = re.sub(r"\b(?:official|repo)-[a-z0-9-]+\b", " source-id ", value)
    value = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", " verification-date ", value)
    return normalize(value)


def _shingles(text: str, size: int = PROVIDER_SHINGLE_SIZE) -> set[tuple[str, ...]]:
    words = text.split()
    return {tuple(words[index : index + size]) for index in range(len(words) - size + 1)}


def similarity(
    left: str,
    right: str,
    *,
    size: int = PROVIDER_SHINGLE_SIZE,
) -> float:
    left_shingles = _shingles(left, size)
    right_shingles = _shingles(right, size)
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
    lesson_ids: set[str] | None = None,
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

    known_lessons = lesson_ids if lesson_ids is not None else curriculum_lesson_ids()
    used_source_ids = {
        str(source_id)
        for record in providers
        for field in ("official_source_ids", "supporting_source_ids")
        for source_id in record.get(field, [])
    }
    for source_id in sorted(used_source_ids):
        source = resources.get(source_id)
        if source is None:
            errors.append(f"provider source is unresolved: {source_id}")
            continue
        related = source.get("related_lessons")
        if not isinstance(related, list):
            errors.append(f"provider source related_lessons must be a list: {source_id}")
            continue
        if not related:
            errors.append(f"provider source related_lessons is empty: {source_id}")
            continue
        if len(related) != len(set(related)):
            errors.append(f"provider source related_lessons has duplicates: {source_id}")
        for lesson_id in related:
            lesson = str(lesson_id)
            if lesson not in known_lessons:
                errors.append(
                    f"provider source related_lessons unresolved: {source_id} -> {lesson}"
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
    aliases = _identity_aliases(providers)
    normalized_documents = {
        slug: _identity_normalized(text, aliases) for slug, text in documents.items()
    }

    section_values: dict[str, tuple[str, str]] = {}
    for slug, text in documents.items():
        for heading_name in EXAMPLE_HEADINGS:
            value = _identity_normalized(section(text, heading_name), aliases)
            if not value:
                continue
            if value in section_values:
                other_slug, other_heading = section_values[value]
                errors.append(
                    "duplicate provider example: "
                    f"{other_slug}[{other_heading}] ~ {slug}[{heading_name}]"
                )
            else:
                section_values[value] = (slug, heading_name)

    paragraphs: dict[str, str] = {}
    for slug, text in documents.items():
        for paragraph in re.split(r"\n\s*\n", text):
            value = _identity_normalized(paragraph, aliases)
            word_total = len(value.split())
            if word_total < LONG_PARAGRAPH_WORDS:
                continue
            if value in paragraphs:
                errors.append(f"reused long provider paragraph: {paragraphs[value]} ~ {slug}")
            else:
                paragraphs[value] = slug

    comparable_blocks: list[tuple[str, str, str]] = []
    for slug, text in documents.items():
        for heading_name in EXAMPLE_HEADINGS:
            value = _identity_normalized(section(text, heading_name), aliases)
            if value:
                comparable_blocks.append((slug, heading_name, value))

    for left_index, (left_slug, left_label, left_text) in enumerate(comparable_blocks):
        for right_slug, right_label, right_text in comparable_blocks[left_index + 1 :]:
            if left_slug == right_slug:
                continue
            if left_text == right_text:
                continue
            score = similarity(
                left_text,
                right_text,
                size=SECTION_NEAR_COPY_SHINGLE_SIZE,
            )
            if score >= SECTION_NEAR_COPY_LIMIT:
                errors.append(
                    "near-copy provider prose: "
                    f"{left_slug}[{left_label}] ~ {right_slug}[{right_label}] "
                    f"score={score:.3f} >= {SECTION_NEAR_COPY_LIMIT:.2f}"
                )

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
    errors = provider_record_errors(
        providers,
        resources,
        as_of=effective_date,
        lesson_ids=curriculum_lesson_ids(root),
    )
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
