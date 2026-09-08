import json
from pathlib import Path

from src.models import ExtractedPaper


def save_extracted_paper(
    paper: ExtractedPaper,
    output_directory: Path,
) -> Path:
    """
    Save one extracted paper as structured JSON.
    """

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_directory
        / f"{paper.paper_id}.json"
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            paper.model_dump(
                mode="json"
            ),
            file,
            ensure_ascii=False,
            indent=2,
        )

    return output_path