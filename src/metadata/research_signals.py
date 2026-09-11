import re

from src.models import (
    ExtractedPaper,
    ResearchSignal,
)

RESEARCH_QUESTION_PATTERN = re.compile(
    r"\bRQ\s*([0-9]+)" r"\s*[:.\-–—]\s*" r"(.{15,400}?[?])",
    flags=re.IGNORECASE,
)

RQ_LABEL_PATTERN = re.compile(
    r"\bRQ\s*([0-9]+)"
    r"\s*[:.\-–—]\s*"
    r"(.{15,220}?)(?="
    r"\bRQ\s*[0-9]+"
    r"|(?:\.\s+[A-Z])"
    r"|$"
    r")",
    flags=re.IGNORECASE,
)


SIGNAL_KEYWORDS: dict[
    str,
    list[str],
] = {
    "methodology": [
        "methodology",
        "our approach",
        "our method",
        "framework",
        "technique",
        "pipeline",
    ],
    "datasets": [
        "dataset",
        "datasets",
        "benchmark",
        "benchmarks",
        "corpus",
        "projects",
        "subject programs",
    ],
    "metrics": [
        "statement coverage",
        "branch coverage",
        "code coverage",
        "mutation score",
        "precision",
        "recall",
        "pass rate",
        "success rate",
    ],
    "findings": [
        "our results show",
        "results show",
        "we found",
        "we observe",
        "outperforms",
        "improves",
        "improvement",
    ],
    "limitations": [
        "limitation",
        "limitations",
        "threat to validity",
        "threats to validity",
    ],
    "future_work": [
        "future work",
        "future research",
        "future direction",
        "future directions",
        "further research",
    ],
}


def extract_research_questions(
    paper: ExtractedPaper,
) -> list[str]:
    """
    Extract unique explicit research-question definitions.
    """

    questions_by_number: dict[
        int,
        str,
    ] = {}

    # Pass 1: strong matches ending in ?
    for page in paper.pages:

        for match in RESEARCH_QUESTION_PATTERN.finditer(page.text):
            number = int(match.group(1))

            if number in questions_by_number:
                continue

            question_text = re.sub(
                r"\s+",
                " ",
                match.group(2),
            ).strip()

            questions_by_number[number] = f"RQ{number}: " f"{question_text}"

    # Pass 2: labelled RQs without question marks.
    for page in paper.pages:

        for match in RQ_LABEL_PATTERN.finditer(page.text):
            number = int(match.group(1))

            if number in questions_by_number:
                continue

            question_text = re.sub(
                r"\s+",
                " ",
                match.group(2),
            ).strip()

            if not (15 <= len(question_text) <= 220):
                continue

            questions_by_number[number] = f"RQ{number}: " f"{question_text}"

    return [questions_by_number[number] for number in sorted(questions_by_number)]


def split_sentences(
    text: str,
) -> list[str]:
    """
    Lightweight sentence splitting suitable for research
    signal extraction.
    """

    return re.split(
        r"(?<=[.!?])\s+",
        text,
    )


def extract_research_signals(
    paper: ExtractedPaper,
    max_per_category: int = 3,
) -> list[ResearchSignal]:
    """
    Find evidence candidates related to methodology,
    datasets, metrics, findings, limitations and future work.

    This does not claim the snippets are final answers.
    They are evidence candidates for later reasoning.
    """

    signals: list[ResearchSignal] = []

    category_counts = {category: 0 for category in SIGNAL_KEYWORDS}

    for page in paper.pages:

        sentences = split_sentences(page.text)

        for sentence in sentences:

            normalized = sentence.lower()

            for category, keywords in SIGNAL_KEYWORDS.items():

                if category_counts[category] >= max_per_category:
                    continue

                matched_keyword = next(
                    (keyword for keyword in keywords if keyword in normalized),
                    None,
                )

                if not matched_keyword:
                    continue

                snippet = re.sub(
                    r"\s+",
                    " ",
                    sentence,
                ).strip()

                if len(snippet) < 30:
                    continue

                if len(snippet) > 700:
                    snippet = snippet[:700].rsplit(" ", 1)[0]

                signals.append(
                    ResearchSignal(
                        category=category,
                        page_number=page.page_number,
                        snippet=snippet,
                        matched_keyword=matched_keyword,
                    )
                )

                category_counts[category] += 1

    return signals
