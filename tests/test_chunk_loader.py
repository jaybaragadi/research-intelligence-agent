import argparse

from src.retrieval.retriever import (
    SemanticRetriever,
)


def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "Semantic search across "
            "research papers"
        )
    )

    parser.add_argument(
        "query",
        type=str,
        help="Research question",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help=(
            "Number of evidence chunks "
            "to retrieve"
        ),
    )

    args = parser.parse_args()

    retriever = (
        SemanticRetriever()
    )

    results = retriever.search(
        query=args.query,
        top_k=args.top_k,
    )

    print()
    print("=" * 70)

    print(
        f"QUERY: {args.query}"
    )

    print("=" * 70)

    for result in results:

        print()
        print(
            f"Rank     : "
            f"{result.rank}"
        )

        print(
            f"Score    : "
            f"{result.score:.4f}"
        )

        print(
            f"Paper    : "
            f"{result.paper_id}"
        )

        print(
            f"Page     : "
            f"{result.page_number}"
        )

        print(
            f"Section  : "
            f"{result.section}"
        )

        print(
            f"Chunk    : "
            f"{result.chunk_id}"
        )

        print()

        print(
            result.text
        )

        print()
        print("-" * 70)


if __name__ == "__main__":
    main()