from dataclasses import dataclass

from src.chunking.chunk_builder import (
    create_page_chunks,
)
from src.chunking.json_writer import (
    save_chunks,
)
from src.config import settings
from src.metadata.processed_loader import (
    discover_processed_papers,
    load_extracted_paper,
)
from src.models import PaperProfile


@dataclass
class ChunkingSummary:
    discovered: int = 0
    successful: int = 0
    failed: int = 0
    total_chunks: int = 0


def load_profile(
    paper_id: str,
) -> PaperProfile:
    """
    Load the Phase 3 profile for a paper.
    """

    metadata_path = settings.metadata_dir / f"{paper_id}.json"

    if not metadata_path.exists():
        raise FileNotFoundError("Metadata profile missing: " f"{metadata_path}")

    return PaperProfile.model_validate_json(metadata_path.read_text(encoding="utf-8"))


def run_chunking() -> ChunkingSummary:
    """
    Run Phase 4 across the complete research corpus.
    """

    processed_files = discover_processed_papers(settings.processed_dir)

    summary = ChunkingSummary(discovered=len(processed_files))

    print()

    print(f"Found {len(processed_files)} " "processed paper(s).")

    print()

    for index, processed_path in enumerate(
        processed_files,
        start=1,
    ):

        print(f"[{index}/{len(processed_files)}] " f"Chunking {processed_path.name}")

        try:

            paper = load_extracted_paper(processed_path)

            profile = load_profile(paper.paper_id)

            chunks = create_page_chunks(
                paper=paper,
                profile=profile,
                chunk_size=settings.chunk_size,
                chunk_overlap=(settings.chunk_overlap),
            )

            output_path = save_chunks(
                paper_id=paper.paper_id,
                chunks=chunks,
                output_directory=(settings.chunks_dir),
            )

            summary.successful += 1

            summary.total_chunks += len(chunks)

            print(f"    Pages       : " f"{paper.total_pages}")

            print(f"    Chunks      : " f"{len(chunks)}")

            if chunks:

                average_size = sum(chunk.character_count for chunk in chunks) / len(
                    chunks
                )

                print(f"    Avg size    : " f"{average_size:.0f} chars")

            print(f"    Saved       : " f"{output_path.name}")

        except Exception as exc:

            summary.failed += 1

            print(f"    FAILED: " f"{type(exc).__name__}: " f"{exc}")

        print()

    return summary
