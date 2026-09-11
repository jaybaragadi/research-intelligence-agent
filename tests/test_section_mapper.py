from src.chunking.section_mapper import (
    section_for_page,
)
from src.models import (
    PaperProfile,
    SectionLocation,
)


def create_profile() -> PaperProfile:

    return PaperProfile(
        paper_id="test",
        filename="test.pdf",
        title="Test Paper",
        sections=[
            SectionLocation(
                canonical_name="introduction",
                matched_heading="introduction",
                page_number=1,
            ),
            SectionLocation(
                canonical_name="methodology",
                matched_heading="methodology",
                page_number=3,
            ),
            SectionLocation(
                canonical_name="results",
                matched_heading="results",
                page_number=5,
            ),
        ],
    )


def test_section_for_exact_page():

    profile = create_profile()

    result = section_for_page(
        3,
        profile,
    )

    assert result == "methodology"


def test_section_carries_forward():

    profile = create_profile()

    result = section_for_page(
        4,
        profile,
    )

    assert result == "methodology"


def test_section_before_first_heading():

    profile = PaperProfile(
        paper_id="test",
        filename="test.pdf",
        title="Test Paper",
        sections=[
            SectionLocation(
                canonical_name="methodology",
                matched_heading="methodology",
                page_number=3,
            )
        ],
    )

    result = section_for_page(
        1,
        profile,
    )

    assert result is None
