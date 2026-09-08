from pathlib import Path

from src.metadata.abstract_extractor import (
    extract_abstract,
)

from src.models import (
    ExtractedPage,
    ExtractedPaper,
)


def create_test_paper(
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


def test_extract_abstract():

    paper = create_test_paper(
        "Test Paper. "
        "Abstract "
        "Large language models can generate software tests. "
        "This study evaluates their effectiveness. "
        "1 Introduction "
        "Software testing is important."
    )

    abstract = extract_abstract(
        paper
    )

    assert abstract is not None

    assert (
        "Large language models"
        in abstract
    )


def test_missing_abstract():

    paper = create_test_paper(
        "Introduction. "
        "This paper studies testing."
    )

    assert (
        extract_abstract(paper)
        is None
    )