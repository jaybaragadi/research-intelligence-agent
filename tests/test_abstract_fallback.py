from pathlib import Path

from src.metadata.abstract_extractor import (
    extract_abstract,
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


def test_front_matter_abstract_fallback():

    text = (
        "A Research Paper Title. "
        "Author Name University Example. "
        "Large language models have recently been used "
        "for automated software testing. "
        "This study evaluates their ability to generate "
        "high-quality unit tests across multiple projects. "
        "Our evaluation measures coverage and correctness "
        "and identifies several important limitations. "
        "1. Introduction Software testing remains an "
        "important software engineering activity."
    )

    paper = create_paper(text)

    abstract = extract_abstract(paper)

    assert abstract is not None

    assert "software testing" in abstract.lower()
