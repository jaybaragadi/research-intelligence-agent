from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from src.ingestion.text_cleaner import clean_text
from src.models import ExtractedPage, ExtractedPaper


class PDFExtractionError(Exception):
    """Raised when a PDF cannot be processed safely."""


def build_paper_id(pdf_path: Path) -> str:
    """
    Convert filename into a stable paper identifier.

    Example:
        01_testpilot.pdf
        ->
        01_testpilot
    """

    return pdf_path.stem.lower()


def validate_pdf(pdf_path: Path) -> None:
    """Validate that a path points to a readable PDF."""

    if not pdf_path.exists():
        raise PDFExtractionError(
            f"PDF does not exist: {pdf_path}"
        )

    if not pdf_path.is_file():
        raise PDFExtractionError(
            f"Path is not a file: {pdf_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise PDFExtractionError(
            f"Not a PDF file: {pdf_path.name}"
        )

    if pdf_path.stat().st_size == 0:
        raise PDFExtractionError(
            f"PDF file is empty: {pdf_path.name}"
        )


def extract_pdf(pdf_path: Path) -> ExtractedPaper:
    """
    Extract text page-by-page from a PDF while preserving
    page-level provenance.
    """

    validate_pdf(pdf_path)

    try:
        reader = PdfReader(str(pdf_path))
    except PdfReadError as exc:
        raise PDFExtractionError(
            f"Unable to read PDF: {pdf_path.name}"
        ) from exc

    except Exception as exc:
        raise PDFExtractionError(
            f"Unexpected PDF error: {pdf_path.name}"
        ) from exc

    extracted_pages: list[ExtractedPage] = []

    empty_pages = 0

    for page_index, page in enumerate(
        reader.pages,
        start=1,
    ):
        try:
            raw_text = page.extract_text() or ""
        except Exception:
            raw_text = ""

        cleaned_text = clean_text(raw_text)

        if not cleaned_text:
            empty_pages += 1
            continue

        extracted_pages.append(
            ExtractedPage(
                page_number=page_index,
                text=cleaned_text,
                character_count=len(cleaned_text),
            )
        )

    return ExtractedPaper(
        paper_id=build_paper_id(pdf_path),
        filename=pdf_path.name,
        source_path=pdf_path.resolve(),
        total_pages=len(reader.pages),
        extracted_pages=len(extracted_pages),
        empty_pages=empty_pages,
        pages=extracted_pages,
    )