import json

from src.config import settings


def main() -> None:

    files = sorted(
        settings.chunks_dir.glob(
            "*.json"
        )
    )

    total_chunks = 0
    warnings: list[str] = []

    seen_ids: set[str] = set()

    for path in files:

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        paper_id = data[
            "paper_id"
        ]

        chunks = data[
            "chunks"
        ]

        total_chunks += len(
            chunks
        )

        if not chunks:

            warnings.append(
                f"{paper_id}: no chunks generated"
            )

            continue

        for chunk in chunks:

            chunk_id = chunk[
                "chunk_id"
            ]

            text = chunk[
                "text"
            ]

            page_number = chunk[
                "page_number"
            ]

            character_count = chunk[
                "character_count"
            ]

            if chunk_id in seen_ids:

                warnings.append(
                    f"{paper_id}: duplicate chunk id "
                    f"{chunk_id}"
                )

            seen_ids.add(
                chunk_id
            )

            if not text.strip():

                warnings.append(
                    f"{chunk_id}: empty text"
                )

            if page_number < 1:

                warnings.append(
                    f"{chunk_id}: invalid page number"
                )

            if character_count != len(
                text
            ):

                warnings.append(
                    f"{chunk_id}: character count mismatch"
                )

            if character_count > (
                settings.chunk_size
                * 1.5
            ):

                warnings.append(
                    f"{chunk_id}: unusually large chunk "
                    f"({character_count} chars)"
                )

    print("=" * 70)
    print("Chunk Validation")
    print("=" * 70)

    print(
        f"Paper files   : {len(files)}"
    )

    print(
        f"Total chunks  : {total_chunks}"
    )

    print(
        f"Warnings      : {len(warnings)}"
    )

    if not warnings:

        print()
        print(
            "Chunk validation passed."
        )

        return

    print()

    for warning in warnings[
        :50
    ]:

        print(
            f"WARNING: {warning}"
        )

    if len(warnings) > 50:

        print()
        print(
            f"... {len(warnings) - 50} "
            "additional warning(s)"
        )


if __name__ == "__main__":
    main()