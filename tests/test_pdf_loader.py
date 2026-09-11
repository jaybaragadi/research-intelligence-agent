import pytest

from src.ingestion.pdf_loader import (
    PDFExtractionError,
    build_paper_id,
    validate_pdf,
)


def test_build_paper_id(tmp_path):
    pdf_path = tmp_path / "01_TestPilot.pdf"

    assert build_paper_id(pdf_path) == "01_testpilot"


def test_validate_missing_pdf(tmp_path):
    missing_file = tmp_path / "missing.pdf"

    with pytest.raises(PDFExtractionError):
        validate_pdf(missing_file)


def test_validate_non_pdf(tmp_path):
    text_file = tmp_path / "notes.txt"

    text_file.write_text(
        "hello",
        encoding="utf-8",
    )

    with pytest.raises(PDFExtractionError):
        validate_pdf(text_file)


def test_validate_empty_pdf(tmp_path):
    empty_pdf = tmp_path / "empty.pdf"

    empty_pdf.touch()

    with pytest.raises(PDFExtractionError):
        validate_pdf(empty_pdf)
