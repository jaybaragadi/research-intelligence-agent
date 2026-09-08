from dataclasses import dataclass

from src.config import settings
from src.ingestion.json_writer import save_extracted_paper
from src.ingestion.paper_discovery import discover_pdfs
from src.ingestion.pdf_loader import (
    PDFExtractionError,
    extract_pdf,
)
from src.ingestion.statistics import total_characters

@dataclass
class IngestionSummary:
    discovered: int = 0
    successful: int = 0
    failed: int = 0


def run_ingestion() -> IngestionSummary:
    """
    Run the complete Phase 2 ingestion pipeline.
    """

    pdf_files = discover_pdfs(
        settings.papers_dir
    )

    summary = IngestionSummary(
        discovered=len(pdf_files)
    )

    print()
    print(
        f"Found {len(pdf_files)} PDF file(s)."
    )
    print()

    if not pdf_files:
        print(
            "No PDFs found in "
            f"{settings.papers_dir}"
        )
        return summary

    for index, pdf_path in enumerate(
        pdf_files,
        start=1,
    ):
        print(
            f"[{index}/{len(pdf_files)}] "
            f"Processing {pdf_path.name}"
        )

        try:
            paper = extract_pdf(pdf_path)

            output_path = save_extracted_paper(
                paper,
                settings.processed_dir,
            )

            summary.successful += 1

            print(
                f"    Pages       : "
                f"{paper.total_pages}"
            )

            print(
                f"    Extracted   : "
                f"{paper.extracted_pages}"
            )

            print(
                f"    Empty pages : "
                f"{paper.empty_pages}"
            )
            print(
                f"    Characters  : "
                f"{total_characters(paper):,}"
            )

            print(
                f"    Saved       : "
                f"{output_path.name}"
            )

        except PDFExtractionError as exc:
            summary.failed += 1

            print(
                f"    FAILED: {exc}"
            )

        print()

    return summary