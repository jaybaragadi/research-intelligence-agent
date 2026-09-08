from pathlib import Path

from src.metadata.research_signals import (
    extract_research_questions,
    extract_research_signals,
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
        source_path=Path(
            "test.pdf"
        ),
        total_pages=1,
        extracted_pages=1,
        empty_pages=0,
        pages=[
            ExtractedPage(
                page_number=1,
                text=text,
                character_count=len(
                    text
                ),
            )
        ],
    )


def test_extract_research_question():

    paper = create_paper(
        "RQ1: How effective are large language models "
        "for automated unit test generation?"
    )

    questions = (
        extract_research_questions(
            paper
        )
    )

    assert len(questions) == 1
    assert questions[0].startswith(
        "RQ1:"
    )


def test_extract_metric_signal():

    paper = create_paper(
        "The generated test suite achieved "
        "82 percent branch coverage."
    )

    signals = extract_research_signals(
        paper
    )

    categories = {
        signal.category
        for signal in signals
    }

    assert "metrics" in categories


def test_extract_limitation_signal():

    paper = create_paper(
        "One limitation of our approach "
        "is its dependence on source-code context."
    )

    signals = extract_research_signals(
        paper
    )

    categories = {
        signal.category
        for signal in signals
    }

    assert "limitations" in categories