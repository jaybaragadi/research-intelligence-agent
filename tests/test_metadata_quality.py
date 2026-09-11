from pathlib import Path

from src.metadata.pipeline import (
    clean_title,
)
from src.metadata.research_signals import (
    extract_research_questions,
)
from src.models import (
    ExtractedPage,
    ExtractedPaper,
)


def create_paper(
    text: str,
) -> ExtractedPaper:
    return ExtractedPaper(
        paper_id="test",
        filename="test.pdf",
        source_path=Path("test.pdf"),
        total_pages=1,
        extracted_pages=1,
        empty_pages=0,
        pages=[
            ExtractedPage(
                page_number=1,
                text=text,
                character_count=len(text),
            )
        ],
    )


def test_clean_title_removes_leading_number():

    title = "1 An Empirical Evaluation " "of Large Language Models"

    assert clean_title(title) == ("An Empirical Evaluation " "of Large Language Models")


def test_rq_is_not_duplicated():

    text = (
        "RQ1: How effective is automated test generation? "
        "The results for RQ1 are shown in Table 2. "
        "We later discuss RQ1 again."
    )

    paper = create_paper(text)

    questions = extract_research_questions(paper)

    assert len(questions) == 1


def test_multiple_unique_rqs():

    text = (
        "RQ1: How effective is the generated test suite? "
        "RQ2: How much branch coverage is achieved? "
        "Results for RQ1 and RQ2 are presented later."
    )

    paper = create_paper(text)

    questions = extract_research_questions(paper)

    assert len(questions) == 2

    assert questions[0].startswith("RQ1:")

    assert questions[1].startswith("RQ2:")
