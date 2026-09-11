from pathlib import Path


def discover_pdfs(
    papers_directory: Path,
) -> list[Path]:
    """
    Discover PDF files in the configured papers directory.

    Files are sorted alphabetically to keep processing
    deterministic.
    """

    if not papers_directory.exists():
        return []

    pdf_files = [
        path
        for path in papers_directory.iterdir()
        if path.is_file() and path.suffix.lower() == ".pdf"
    ]

    return sorted(
        pdf_files,
        key=lambda path: path.name.lower(),
    )
