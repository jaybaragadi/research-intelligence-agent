from dataclasses import dataclass
from pathlib import Path

from src.config import settings

from src.metadata.abstract_extractor import (
    extract_abstract,
)

from src.metadata.document_metadata import (
    extract_year,
    read_pdf_document_metadata,
)

from src.metadata.json_writer import (
    save_paper_profile,
)

from src.metadata.processed_loader import (
    discover_processed_papers,
    load_extracted_paper,
)

from src.metadata.research_signals import (
    extract_research_questions,
    extract_research_signals,
)

from src.metadata.section_parser import (
    discover_sections,
)

from src.models import PaperProfile


@dataclass
class MetadataSummary:
    discovered: int = 0
    successful: int = 0
    failed: int = 0


def fallback_title(
    first_page_text: str,
    filename: str,
) -> str:
    """
    Attempt a conservative title fallback when PDF properties
    do not contain a title.
    """

    abstract_position = (
        first_page_text.lower()
        .find("abstract")
    )

    if abstract_position > 0:
        candidate = (
            first_page_text[
                :abstract_position
            ]
            .strip()
        )

        candidate = " ".join(
            candidate.split()
        )

        if 10 <= len(candidate) <= 500:
            return candidate

    return (
        Path(filename)
        .stem
        .replace("_", " ")
        .strip()
    )


def build_profile(
    processed_path: Path,
) -> PaperProfile:
    """
    Build the complete Phase 3 profile for one paper.
    """

    paper = load_extracted_paper(
        processed_path
    )

    pdf_path = Path(
        paper.source_path
    )

    title: str | None = None
    authors: list[str] = []
    year: int | None = None

    if pdf_path.exists():

        title, authors, year = (
            read_pdf_document_metadata(
                pdf_path
            )
        )

    first_page_text = (
        paper.pages[0].text
        if paper.pages
        else ""
    )

    if not title:
        title = fallback_title(
            first_page_text,
            paper.filename,
        )

    # Fallback year search from opening page.
    if year is None:
        year = extract_year(
            first_page_text
        )

    abstract = extract_abstract(
        paper
    )

    sections = discover_sections(
        paper
    )

    research_questions = (
        extract_research_questions(
            paper
        )
    )

    research_signals = (
        extract_research_signals(
            paper
        )
    )

    return PaperProfile(
        paper_id=paper.paper_id,
        filename=paper.filename,
        title=title,
        authors=authors,
        year=year,
        abstract=abstract,
        sections=sections,
        research_questions=research_questions,
        research_signals=research_signals,
    )


def run_metadata_extraction(
) -> MetadataSummary:
    """
    Run Phase 3 across all processed research papers.
    """

    processed_files = (
        discover_processed_papers(
            settings.processed_dir
        )
    )

    summary = MetadataSummary(
        discovered=len(
            processed_files
        )
    )

    print()
    print(
        f"Found {len(processed_files)} "
        "processed paper(s)."
    )
    print()

    for index, processed_path in enumerate(
        processed_files,
        start=1,
    ):

        print(
            f"[{index}/{len(processed_files)}] "
            f"Profiling {processed_path.name}"
        )

        try:
            profile = build_profile(
                processed_path
            )

            output_path = (
                save_paper_profile(
                    profile,
                    settings.metadata_dir,
                )
            )

            summary.successful += 1

            print(
                f"    Title      : "
                f"{profile.title[:80]}"
            )

            print(
                f"    Authors    : "
                f"{len(profile.authors)}"
            )

            print(
                f"    Year       : "
                f"{profile.year}"
            )

            print(
                f"    Abstract   : "
                f"{'Yes' if profile.abstract else 'No'}"
            )

            print(
                f"    Sections   : "
                f"{len(profile.sections)}"
            )

            print(
                f"    RQs        : "
                f"{len(profile.research_questions)}"
            )

            print(
                f"    Signals    : "
                f"{len(profile.research_signals)}"
            )

            print(
                f"    Saved      : "
                f"{output_path.name}"
            )

        except Exception as exc:

            summary.failed += 1

            print(
                f"    FAILED: "
                f"{type(exc).__name__}: "
                f"{exc}"
            )

        print()

    return summary