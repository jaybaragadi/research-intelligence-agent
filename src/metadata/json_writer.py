import json
from pathlib import Path

from src.models import PaperProfile


def save_paper_profile(
    profile: PaperProfile,
    output_directory: Path,
) -> Path:
    """
    Save a Phase 3 paper profile to JSON.
    """

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_directory / f"{profile.paper_id}.json"

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            profile.model_dump(mode="json"),
            file,
            indent=2,
            ensure_ascii=False,
        )

    return output_path
