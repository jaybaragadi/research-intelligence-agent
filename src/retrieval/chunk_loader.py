import json
from pathlib import Path

from src.models import PaperChunk


def discover_chunk_files(
    chunks_directory: Path,
) -> list[Path]:
    """
    Discover Phase-4 chunk files.
    """

    if not chunks_directory.exists():
        return []

    return sorted(
        chunks_directory.glob(
            "*.json"
        )
    )


def load_chunks_from_file(
    path: Path,
) -> list[PaperChunk]:
    """
    Load all chunks for one research paper.
    """

    data = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    raw_chunks = data.get(
        "chunks",
        [],
    )

    return [
        PaperChunk.model_validate(
            chunk
        )
        for chunk in raw_chunks
    ]


def load_all_chunks(
    chunks_directory: Path,
) -> list[PaperChunk]:
    """
    Load the complete searchable research corpus.
    """

    chunk_files = discover_chunk_files(
        chunks_directory
    )

    chunks: list[PaperChunk] = []

    for path in chunk_files:

        chunks.extend(
            load_chunks_from_file(
                path
            )
        )

    return chunks