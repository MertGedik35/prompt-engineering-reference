from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

# Curriculum thresholds are intentionally above the former 21–25 word lessons.
LESSON_MIN_WORDS = 900
EXERCISE_MIN_WORDS = 300
SOLUTION_MIN_WORDS = 500
LESSON_SHINGLE_SIZE = 5
LESSON_SIMILARITY_LIMIT = 0.72
GENERIC_EXERCISE = "rewrite a weak prompt using the module concept"

LESSON_HEADINGS = (
    "Learning objectives",
    "Why this matters",
    "Prerequisites",
    "Core concepts",
    "Mental models",
    "Key terminology",
    "Minimal example",
    "Production example",
    "Bad example",
    "Why the bad example fails",
    "Worked example",
    "Provider-specific considerations",
    "Hands-on exercise",
    "Evaluation rubric",
    "Common failure modes",
    "Official sources",
    "Research sources",
    "Completion checklist",
    "Next module",
)
EXERCISE_HEADINGS = (
    "Scenario",
    "Objective",
    "Provided inputs",
    "Constraints",
    "Required deliverables",
    "Normal case",
    "Edge case",
    "Failure or adversarial case",
    "Evaluation rubric",
    "Passing conditions",
    "Optional extension",
    "Solution link",
)
SOLUTION_HEADINGS = (
    "Exercise reasoning criteria",
    "Example acceptable submission",
    "Common mistakes",
    "Rubric interpretation",
    "Acceptable alternatives",
    "Failing responses",
    "Quiz answers and explanations",
)


@dataclass
class QualityReport:
    metrics: dict[str, int] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    details: list[str] = field(default_factory=list)


def load(root: Path, path: str) -> list[dict[str, Any]]:
    return json.loads((root / path).read_text(encoding="utf-8"))


def normalize(value: object) -> str:
    text = json.dumps(value, sort_keys=True) if not isinstance(value, str) else value
    text = re.sub(r"\{[^}]+\}", "{var}", text.lower())
    text = re.sub(r"\b(?:module|lesson|exercise)\s+\d+[a-z-]*\b", " topic ", text)
    text = re.sub(r"\b\d{2}-[a-z0-9-]+\b", " topic ", text)
    text = re.sub(r"template-[a-z0-9-]+|pattern-[a-z0-9-]+", "id", text)
    text = re.sub(r"[^a-z0-9{}]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def meaningful_text(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"^\|.*$", " ", text, flags=re.MULTILINE)
    text = re.sub(r"\[[^\]]+\]\([^)]*\)", " ", text)
    text = re.sub(r"^#{1,6}\s+.*$", " ", text, flags=re.MULTILINE)
    return normalize(text)


def meaningful_word_count(text: str) -> int:
    core = re.split(r"^## Official sources\s*$", text, flags=re.MULTILINE)[0]
    return len(re.findall(r"\b[a-zA-Z][a-zA-Z'-]*\b", meaningful_text(core)))


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


def shingles(text: str, size: int = LESSON_SHINGLE_SIZE) -> set[tuple[str, ...]]:
    tokens = meaningful_text(text).split()
    return {tuple(tokens[index : index + size]) for index in range(len(tokens) - size + 1)}


def jaccard(left: str, right: str) -> float:
    a, b = shingles(left), shingles(right)
    return len(a & b) / len(a | b) if a and b else 0.0


def missing_required(text: str, required: tuple[str, ...]) -> list[str]:
    present = headings(text)
    return [name for name in required if name not in present]


def duplicate_blocks(records: list[dict[str, Any]], field_name: str) -> list[str]:
    counter = Counter(normalize(record.get(field_name, "")) for record in records)
    return [value for value, count in counter.items() if count > 1 and value]


def high_similarity(records: list[dict[str, Any]], field_name: str, threshold: float) -> list[str]:
    pairs: list[str] = []
    normalized = [(record["id"], normalize(record.get(field_name, ""))) for record in records]
    for (left_id, left_text), (right_id, right_text) in combinations(normalized, 2):
        if left_text and right_text:
            score = SequenceMatcher(None, left_text, right_text).ratio()
            if score >= threshold:
                pairs.append(f"{left_id} ~ {right_id}: {score:.3f}")
    return pairs


def check_curriculum(root: Path, report: QualityReport) -> None:
    lesson_files = sorted((root / "curriculum").glob("*/README.md"))
    exercise_files = sorted((root / "curriculum").glob("*/exercise.md"))
    quiz_files = sorted((root / "curriculum").glob("*/quiz.md"))
    solution_files = sorted((root / "labs" / "solutions").glob("*.md"))
    report.metrics.update(
        lessons=len(lesson_files),
        exercises=len(exercise_files),
        quizzes=len(quiz_files),
        solutions=len(solution_files),
    )
    if not all(
        len(group) == 13 for group in (lesson_files, exercise_files, quiz_files, solution_files)
    ):
        report.errors.append(
            "curriculum inventory must contain 13 lessons/exercises/quizzes/solutions"
        )

    lesson_texts: dict[Path, str] = {}
    examples: dict[str, list[tuple[Path, str]]] = {
        name: [] for name in ("Minimal example", "Production example", "Bad example")
    }
    references: list[tuple[Path, str]] = []
    for path in lesson_files:
        text = path.read_text(encoding="utf-8")
        lesson_texts[path] = text
        count = meaningful_word_count(text)
        report.details.append(f"lesson {path.relative_to(root)} words={count}")
        if count < LESSON_MIN_WORDS:
            report.errors.append(
                f"{path.relative_to(root)}: lesson words {count} < {LESSON_MIN_WORDS}"
            )
        for name in missing_required(text, LESSON_HEADINGS):
            report.errors.append(f"{path.relative_to(root)}: missing heading `{name}`")
        for name in examples:
            value = normalize(section(text, name))
            if not value:
                report.errors.append(f"{path.relative_to(root)}: empty `{name}`")
            examples[name].append((path, value))
        references.append(
            (
                path,
                normalize(section(text, "Official sources") + section(text, "Research sources")),
            )
        )

    for (left_path, left), (right_path, right) in combinations(lesson_texts.items(), 2):
        if normalize(left) == normalize(right):
            report.errors.append(f"duplicate lessons: {left_path} ~ {right_path}")
        score = jaccard(left, right)
        if score >= LESSON_SIMILARITY_LIMIT:
            report.errors.append(
                f"high-similarity lessons: {left_path.relative_to(root)} ~ "
                f"{right_path.relative_to(root)} score={score:.3f} "
                f">= {LESSON_SIMILARITY_LIMIT:.2f}"
            )
    for label, values in examples.items():
        for (left_path, left), (right_path, right) in combinations(values, 2):
            if left and left == right:
                report.errors.append(
                    f"duplicate {label.lower()}: {left_path.relative_to(root)} ~ "
                    f"{right_path.relative_to(root)}"
                )
    for (left_path, left), (right_path, right) in combinations(references, 2):
        if left and left == right:
            report.errors.append(
                f"identical reading lists: {left_path.relative_to(root)} ~ "
                f"{right_path.relative_to(root)}"
            )

    exercise_norm: list[tuple[Path, str]] = []
    for path in exercise_files:
        text = path.read_text(encoding="utf-8")
        count = meaningful_word_count(text)
        report.details.append(f"exercise {path.relative_to(root)} words={count}")
        if count < EXERCISE_MIN_WORDS:
            report.errors.append(
                f"{path.relative_to(root)}: exercise words {count} < {EXERCISE_MIN_WORDS}"
            )
        for name in missing_required(text, EXERCISE_HEADINGS):
            report.errors.append(f"{path.relative_to(root)}: missing heading `{name}`")
        if GENERIC_EXERCISE in normalize(text):
            report.errors.append(f"{path.relative_to(root)}: generic rewrite exercise")
        exercise_norm.append((path, normalize(text)))
    for (left_path, left), (right_path, right) in combinations(exercise_norm, 2):
        if left == right:
            report.errors.append(f"duplicate exercises: {left_path} ~ {right_path}")

    all_questions: dict[str, Path] = {}
    for path in quiz_files:
        text = path.read_text(encoding="utf-8")
        questions = re.findall(r"^\d+\.\s+(.+?)(?=^\d+\.|^##|\Z)", text, re.MULTILINE | re.DOTALL)
        report.details.append(f"quiz {path.relative_to(root)} questions={len(questions)}")
        if len(questions) < 8:
            report.errors.append(f"{path.relative_to(root)}: quiz questions {len(questions)} < 8")
        scenario_count = len(re.findall(r"\*\*Scenario analysis", text))
        if scenario_count < 2:
            report.errors.append(
                f"{path.relative_to(root)}: scenario questions {scenario_count} < 2"
            )
        if "solution" not in text.lower() and "answer key" not in text.lower():
            report.errors.append(f"{path.relative_to(root)}: missing answer-key link")
        for question in questions:
            value = normalize(question)
            if value in all_questions:
                report.errors.append(
                    f"duplicate quiz question: {all_questions[value].relative_to(root)} ~ "
                    f"{path.relative_to(root)}"
                )
            all_questions[value] = path

    solution_norm: list[tuple[Path, str]] = []
    for path in solution_files:
        text = path.read_text(encoding="utf-8")
        count = meaningful_word_count(text)
        report.details.append(f"solution {path.relative_to(root)} words={count}")
        if count < SOLUTION_MIN_WORDS:
            report.errors.append(
                f"{path.relative_to(root)}: solution words {count} < {SOLUTION_MIN_WORDS}"
            )
        for name in missing_required(text, SOLUTION_HEADINGS):
            report.errors.append(f"{path.relative_to(root)}: missing heading `{name}`")
        explanations = section(text, "Quiz answers and explanations")
        answer_blocks = re.findall(
            r"^\d+\.\s+(.+?)(?=^\d+\.|\Z)",
            explanations,
            flags=re.MULTILINE | re.DOTALL,
        )
        if len(answer_blocks) < 8:
            report.errors.append(f"{path.relative_to(root)}: fewer than 8 explained quiz answers")
        elif any(len(normalize(answer).split()) < 6 for answer in answer_blocks):
            report.errors.append(f"{path.relative_to(root)}: answer labels lack explanations")
        solution_norm.append((path, normalize(text)))
    for (left_path, left), (right_path, right) in combinations(solution_norm, 2):
        if left == right:
            report.errors.append(f"duplicate solutions: {left_path} ~ {right_path}")


def check_catalogs(root: Path, report: QualityReport) -> None:
    patterns = load(root, "catalog/patterns.json")
    templates = load(root, "catalog/templates.json")
    for field_name in ("acceptance_criteria", "failure_modes"):
        for item in duplicate_blocks(templates, field_name):
            report.errors.append(f"duplicate template {field_name}: {item[:80]}")
    for field_name in ("use_when", "acceptance_criteria", "failure_modes", "verification"):
        for item in duplicate_blocks(patterns, field_name):
            report.errors.append(f"duplicate pattern {field_name}: {item[:80]}")
    report.errors.extend(
        f"high similarity template prompt: {item}"
        for item in high_similarity(templates, "prompt", 0.94)
    )
    report.errors.extend(
        f"high similarity pattern example: {item}"
        for item in high_similarity(patterns, "example_prompt", 0.96)
    )
    for record in templates:
        if len(record.get("prompt", "")) < 250:
            report.errors.append(f"short template prompt: {record['id']}")


def run_checks(root: Path = ROOT) -> QualityReport:
    report = QualityReport()
    check_curriculum(root, report)
    if (root / "catalog" / "patterns.json").exists():
        check_catalogs(root, report)
    report.metrics["errors"] = len(report.errors)
    return report


def main() -> int:
    report = run_checks()
    print("\n".join(report.details))
    if report.errors:
        print("Content quality check failed")
        for error in report.errors:
            print(f"- {error}")
        print(json.dumps(report.metrics, indent=2, sort_keys=True))
        return 1
    print("Content quality check passed")
    print(json.dumps(report.metrics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
