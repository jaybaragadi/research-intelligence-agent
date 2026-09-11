import json
from pathlib import Path

from src.models import PaperChunk


def save_chunks(
    paper_id: str,
    chunks: list[PaperChunk],
    output_directory: Path,
) -> Path:
    """
    Save all chunks for one paper.
    """

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_directory / f"{paper_id}.json"

    payload = {
        "paper_id": paper_id,
        "chunk_count": len(chunks),
        "chunks": [chunk.model_dump(mode="json") for chunk in chunks],
    }

    output_path.write_text(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return output_path
