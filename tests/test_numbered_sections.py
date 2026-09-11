from pathlib import Path

from src.metadata.section_parser import (
    discover_sections,
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


def test_numbered_sections_after_flattening():

    text = (
        "Some previous text. "
        "1. Introduction The study begins here. "
        "2. Related Work Prior studies are discussed. "
        "3. Methodology Our proposed technique is described. "
        "4. Evaluation We evaluate the system. "
        "5. Results The results are presented. "
        "6. Conclusion We conclude the study."
    )

    paper = create_paper(text)

    sections = discover_sections(paper)

    names = {section.canonical_name for section in sections}

    assert "introduction" in names
    assert "related_work" in names
    assert "methodology" in names
    assert "evaluation" in names
    assert "results" in names
    assert "conclusion" in names


def test_roman_numeral_sections():

    text = (
        "I. INTRODUCTION Intro text. "
        "II. BACKGROUND Background text. "
        "III. EVALUATION Evaluation text. "
        "IV. RESULTS Result text. "
        "V. CONCLUSION Final text."
    )

    paper = create_paper(text)

    sections = discover_sections(paper)

    names = {section.canonical_name for section in sections}

    assert "introduction" in names
    assert "background" in names
    assert "evaluation" in names
    assert "results" in names
    assert "conclusion" in names
