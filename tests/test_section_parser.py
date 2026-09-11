from pathlib import Path

from src.metadata.section_parser import (
    discover_sections,
)
from src.models import (
    ExtractedPage,
    ExtractedPaper,
)


def test_discover_sections():

    text = (
        "Abstract This is the abstract. "
        "1. Introduction This is the introduction. "
        "2. Related Work Prior research exists. "
        "3. Methodology Our approach is described here. "
        "4. Results Results are presented here. "
        "5. Conclusion We conclude the study."
    )

    paper = ExtractedPaper(
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

    sections = discover_sections(paper)

    names = {section.canonical_name for section in sections}

    assert "introduction" in names
    assert "related_work" in names
    assert "methodology" in names
    assert "results" in names
    assert "conclusion" in names
