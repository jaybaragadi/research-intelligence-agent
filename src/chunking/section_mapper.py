from src.models import (
    PaperProfile,
    SectionLocation,
)


def section_for_page(
    page_number: int,
    profile: PaperProfile,
) -> str | None:
    """
    Determine the most likely active section for a page.

    The latest recognized section starting on or before the
    current page is treated as the active section.
    """

    eligible_sections: list[
        SectionLocation
    ] = [
        section
        for section in profile.sections
        if section.page_number
        <= page_number
    ]

    if not eligible_sections:
        return None

    active_section = max(
        eligible_sections,
        key=lambda section: (
            section.page_number
        ),
    )

    return active_section.canonical_name