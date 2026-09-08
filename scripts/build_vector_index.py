from src.retrieval.index_builder import (
    build_vector_index,
)


def main() -> None:

    print("=" * 70)

    print(
        "Research Intelligence Agent"
    )

    print(
        "Phase 5 - Semantic Vector Index"
    )

    print("=" * 70)
    print()

    summary = build_vector_index()

    print()
    print("=" * 70)

    print(
        "Vector Index Summary"
    )

    print("=" * 70)

    print(
        f"Chunks indexed : "
        f"{summary.chunk_count}"
    )

    print(
        f"Dimensions     : "
        f"{summary.embedding_dimension}"
    )

    print(
        f"FAISS index    : "
        f"{summary.index_path}"
    )

    print(
        f"Metadata       : "
        f"{summary.metadata_path}"
    )


if __name__ == "__main__":
    main()