from src.models import ExtractedPaper


def total_characters(
    paper: ExtractedPaper,
) -> int:
    """Return total extracted characters."""

    return sum(
        page.character_count
        for page in paper.pages
    )


def average_characters_per_page(
    paper: ExtractedPaper,
) -> float:
    """Return average characters per extracted page."""

    if not paper.pages:
        return 0.0

    return (
        total_characters(paper)
        / len(paper.pages)
    )