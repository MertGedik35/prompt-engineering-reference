from __future__ import annotations

from pathlib import Path

from scripts.check_content_quality import (
    EXERCISE_HEADINGS,
    LESSON_HEADINGS,
    LESSON_MIN_WORDS,
    SOLUTION_HEADINGS,
    QualityReport,
    check_curriculum,
    jaccard,
    meaningful_word_count,
    missing_required,
    normalize,
    section,
)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_fixture(tmp_path: Path) -> QualityReport:
    report = QualityReport()
    check_curriculum(tmp_path, report)
    return report


def lesson_text(title: str, marker: str = "distinct") -> str:
    sections = "\n\n".join(
        f"## {heading}\n\n{marker} {heading.lower()} "
        + (f"{marker} evidence reasoning decision boundary mechanism evaluation " * 18)
        for heading in LESSON_HEADINGS
    )
    return f"# {title}\n\nLast verified: 2026-07-30\n\n{sections}"


def exercise_text(marker: str = "exercise") -> str:
    return "\n\n".join(
        [f"# Exercise {marker}"]
        + [
            f"## {heading}\n\n"
            + " ".join(f"{marker}-{heading.replace(' ', '-')}-{index}" for index in range(35))
            for heading in EXERCISE_HEADINGS
        ]
    )


def quiz_text(marker: str = "quiz") -> str:
    questions = "\n\n".join(
        f"{index}. {'**Scenario analysis.**' if index in (5, 6) else '**Design.**'} "
        f"{marker} unique decision {index}?"
        for index in range(1, 9)
    )
    return f"# Quiz\n\n{questions}\n\n## Answer key\n\n[Solution](../../labs/solutions/x.md)"


def solution_text(marker: str = "solution") -> str:
    sections = []
    for heading in SOLUTION_HEADINGS:
        body = " ".join(f"{marker}-{heading.replace(' ', '-')}-{index}" for index in range(75))
        if heading == "Quiz answers and explanations":
            body = "\n".join(
                f"{index}. {marker} because criterion {index} applies." for index in range(1, 9)
            )
        sections.append(f"## {heading}\n\n{body}")
    return "# Solution and answer key\n\n" + "\n\n".join(sections)


def test_title_substitution_lessons_are_detected(tmp_path: Path) -> None:
    body = lesson_text("Alpha", "shared")
    write(tmp_path / "curriculum/a/README.md", body)
    write(tmp_path / "curriculum/b/README.md", body.replace("# Alpha", "# Beta"))
    report = run_fixture(tmp_path)
    assert any("high-similarity lessons" in error for error in report.errors)


def test_twenty_five_word_lesson_is_rejected(tmp_path: Path) -> None:
    write(tmp_path / "curriculum/a/README.md", "# Tiny\n\n" + "word " * 25)
    report = run_fixture(tmp_path)
    assert any("lesson words 25 <" in error for error in report.errors)


def test_identical_minimal_examples_are_rejected(tmp_path: Path) -> None:
    left = lesson_text("One", "left")
    right = lesson_text("Two", "right")
    shared = "A unique shared runnable example with evidence and expected output."
    left = left.replace(section(left, "Minimal example"), shared)
    right = right.replace(section(right, "Minimal example"), shared)
    write(tmp_path / "curriculum/a/README.md", left)
    write(tmp_path / "curriculum/b/README.md", right)
    report = run_fixture(tmp_path)
    assert any("duplicate minimal example" in error for error in report.errors)


def test_generic_rewrite_exercise_is_rejected(tmp_path: Path) -> None:
    text = exercise_text() + "\n\nRewrite a weak prompt using the module concept."
    write(tmp_path / "curriculum/a/exercise.md", text)
    report = run_fixture(tmp_path)
    assert any("generic rewrite exercise" in error for error in report.errors)


def test_three_question_quiz_is_rejected(tmp_path: Path) -> None:
    text = "\n".join(f"{index}. Question?" for index in range(1, 4))
    write(tmp_path / "curriculum/a/quiz.md", text)
    report = run_fixture(tmp_path)
    assert any("quiz questions 3 < 8" in error for error in report.errors)


def test_duplicate_quiz_questions_are_rejected(tmp_path: Path) -> None:
    write(tmp_path / "curriculum/a/quiz.md", quiz_text("shared"))
    write(tmp_path / "curriculum/b/quiz.md", quiz_text("shared"))
    report = run_fixture(tmp_path)
    assert any("duplicate quiz question" in error for error in report.errors)


def test_one_sentence_solution_is_rejected(tmp_path: Path) -> None:
    write(tmp_path / "labs/solutions/a.md", "# Solution\n\nThe answer is correct.")
    report = run_fixture(tmp_path)
    assert any("solution words" in error for error in report.errors)


def test_answer_letters_without_explanations_are_rejected(tmp_path: Path) -> None:
    text = solution_text().replace(
        section(solution_text(), "Quiz answers and explanations"),
        "1. A\n2. B\n3. C\n4. D\n5. A\n6. B\n7. C\n8. D",
    )
    write(tmp_path / "labs/solutions/a.md", text)
    report = run_fixture(tmp_path)
    assert any("answer labels lack explanations" in error for error in report.errors)


def test_missing_lesson_heading_is_reported(tmp_path: Path) -> None:
    text = lesson_text("Missing").replace("## Worked example", "### Worked example")
    write(tmp_path / "curriculum/a/README.md", text)
    report = run_fixture(tmp_path)
    assert any("missing heading `Worked example`" in error for error in report.errors)


def test_identical_references_are_rejected(tmp_path: Path) -> None:
    left = lesson_text("Left", "alpha")
    right = lesson_text("Right", "beta")
    for heading in ("Official sources", "Research sources"):
        common = "Canonical source https example invalid shared research"
        left = left.replace(section(left, heading), common)
        right = right.replace(section(right, heading), common)
    write(tmp_path / "curriculum/a/README.md", left)
    write(tmp_path / "curriculum/b/README.md", right)
    report = run_fixture(tmp_path)
    assert any("identical reading lists" in error for error in report.errors)


def test_valid_representative_lesson_meets_depth_and_structure() -> None:
    text = lesson_text("Representative", "valid")
    assert meaningful_word_count(text) >= LESSON_MIN_WORDS
    assert missing_required(text, LESSON_HEADINGS) == []


def test_distinct_representative_lessons_are_below_similarity_limit() -> None:
    assert jaccard(lesson_text("One", "alpha"), lesson_text("Two", "omega")) < 0.72


def test_normalization_removes_module_identifier_substitutions() -> None:
    assert normalize("Module 02-prompt-anatomy teaches this.") == normalize(
        "Module 09-security teaches this."
    )
