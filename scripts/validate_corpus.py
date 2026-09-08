import json

from src.config import settings


def main() -> None:
    """
    Validate corpus-level metadata quality.

    This script reports warnings rather than failing the
    application because some academic PDFs may legitimately
    have incomplete metadata.
    """

    files = sorted(
        settings.metadata_dir.glob(
            "*.json"
        )
    )

    warnings: list[str] = []

    for path in files:

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        paper_id = data[
            "paper_id"
        ]

        if not data["abstract"]:
            warnings.append(
                f"{paper_id}: abstract missing"
            )

        if len(
            data["sections"]
        ) < 3:
            warnings.append(
                f"{paper_id}: "
                "fewer than 3 sections detected"
            )

        if len(
            data["research_questions"]
        ) > 10:
            warnings.append(
                f"{paper_id}: "
                "suspiciously high RQ count "
                f"({len(data['research_questions'])})"
            )

        if data["year"] is None:
            warnings.append(
                f"{paper_id}: year missing"
            )

        if not data["title"]:
            warnings.append(
                f"{paper_id}: title missing"
            )

    print("=" * 70)
    print("Corpus Validation")
    print("=" * 70)

    print(
        f"Papers checked : {len(files)}"
    )

    print(
        f"Warnings       : {len(warnings)}"
    )

    if not warnings:

        print()
        print(
            "Corpus metadata validation passed."
        )

        return

    print()

    for warning in warnings:

        print(
            f"WARNING: {warning}"
        )


if __name__ == "__main__":
    main()