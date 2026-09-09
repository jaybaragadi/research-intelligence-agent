import argparse

from src.tools.search_papers import (
    SearchPapersTool,
)


def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "Search research papers and return "
            "evidence-backed results"
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
            "Maximum number of evidence "
            "results"
        ),
    )

    args = parser.parse_args()

    tool = SearchPapersTool()

    response = tool.search(
        query=args.query,
        top_k=args.top_k,
    )

    print()
    print("=" * 70)
    print("RESEARCH EVIDENCE SEARCH")
    print("=" * 70)

    print(
        f"Query   : {response.query}"
    )

    print(
        f"Results : {response.result_count}"
    )

    for result in response.results:

        print()
        print("-" * 70)

        print(
            f"Rank          : "
            f"{result.rank}"
        )

        print(
            f"Paper         : "
            f"{result.paper_id}"
        )

        print(
            f"Page          : "
            f"{result.page_number}"
        )

        print(
            f"Section       : "
            f"{result.section}"
        )

        print(
            f"Score         : "
            f"{result.score:.4f}"
        )

        print(
            f"Raw score     : "
            f"{result.raw_score:.4f}"
        )

        print(
            f"Lexical score : "
            f"{result.lexical_score:.4f}"
        )

        print(
            f"Chunk         : "
            f"{result.chunk_id}"
        )

        print()

        print(
            result.text
        )

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()