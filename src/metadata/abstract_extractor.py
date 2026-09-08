import re

from src.models import ExtractedPaper


ABSTRACT_PATTERN = re.compile(
    r"\babstract\b"
    r"\s*[:\-—]?\s*"
    r"(.+?)"
    r"(?="
    r"\b(?:1[\.\s]+)?introduction\b"
    r"|\bindex terms\b"
    r"|\bkeywords?\b"
    r")",
    flags=re.IGNORECASE | re.DOTALL,
)


def extract_abstract(
    paper: ExtractedPaper,
) -> str | None:
    """
    Extract an abstract from the opening pages.

    We search only the first three pages to avoid matching
    references to another paper's abstract later in the document.
    """

    opening_pages = paper.pages[:3]

    text = "\n\n".join(
        page.text
        for page in opening_pages
    )

    match = ABSTRACT_PATTERN.search(
        text
    )

    if not match:
        return None

    abstract = match.group(1).strip()

    # Protect against accidental huge matches.
    if len(abstract) > 5000:
        abstract = abstract[:5000].strip()

    return abstract