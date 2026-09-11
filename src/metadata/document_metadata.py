import re
from pathlib import Path

from pypdf import PdfReader

YEAR_PATTERN = re.compile(r"\b(19\d{2}|20\d{2})\b")


def normalize_value(
    value: object | None,
) -> str | None:
    """Convert PDF metadata values into clean strings."""

    if value is None:
        return None

    value_string = str(value).strip()

    if not value_string:
        return None

    return value_string


def split_authors(
    author_text: str | None,
) -> list[str]:
    """
    Convert a PDF author metadata string into a list.

    We deliberately avoid splitting on commas because many
    academic names use 'Last, First' formatting.
    """

    if not author_text:
        return []

    parts = re.split(
        r"\s*;\s*|\s+\band\b\s+",
        author_text,
        flags=re.IGNORECASE,
    )

    return [author.strip() for author in parts if author.strip()]


def extract_year(
    *values: str | None,
) -> int | None:
    """
    Find the first plausible publication/document year.
    """

    for value in values:
        if not value:
            continue

        match = YEAR_PATTERN.search(value)

        if match:
            year = int(match.group(1))

            if 1990 <= year <= 2035:
                return year

    return None


def read_pdf_document_metadata(
    pdf_path: Path,
) -> tuple[
    str | None,
    list[str],
    int | None,
]:
    """
    Read title, authors and year from PDF document properties.
    """

    reader = PdfReader(str(pdf_path))

    metadata = reader.metadata

    if not metadata:
        return None, [], None

    title = normalize_value(getattr(metadata, "title", None))

    author_text = normalize_value(getattr(metadata, "author", None))

    creation_date = normalize_value(getattr(metadata, "creation_date", None))

    modification_date = normalize_value(getattr(metadata, "modification_date", None))

    authors = split_authors(author_text)

    year = extract_year(
        creation_date,
        modification_date,
    )

    return title, authors, year
