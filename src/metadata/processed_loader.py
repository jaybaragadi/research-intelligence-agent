from pathlib import Path

from src.models import ExtractedPaper


def load_extracted_paper(
    json_path: Path,
) -> ExtractedPaper:
    """
    Load a Phase 2 processed-paper JSON file.
    """

    if not json_path.exists():
        raise FileNotFoundError(f"Processed paper not found: {json_path}")

    raw_json = json_path.read_text(encoding="utf-8")

    return ExtractedPaper.model_validate_json(raw_json)


def discover_processed_papers(
    processed_directory: Path,
) -> list[Path]:
    """
    Discover Phase 2 JSON files.
    """

    if not processed_directory.exists():
        return []

    return sorted(
        processed_directory.glob("*.json"),
        key=lambda path: path.name.lower(),
    )
