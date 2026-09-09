import argparse

from src.tools.compare_papers import (
    ComparePapersTool,
)


def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "Compare research papers using "
            "retrieved evidence"
        )
    )

    parser.add_argument(
        "query",
        type=str,
        help="Comparison research question",
    )

    parser.add_argument(
        "--papers",
        nargs="+",
        required=True,
        help=(
            "Paper IDs to compare, for example "
            "03_mutap 05_coverup"
        ),
    )

    parser.add_argument(
        "--evidence-per-paper",
        type=int,
        default=3,
        help=(
            "Maximum evidence chunks "
            "per paper"
        ),
    )

    args = parser.parse_args()

    tool = ComparePapersTool()

    response = tool.compare(
        paper_ids=args.papers,
        query=args.query,
        evidence_per_paper=(
            args.evidence_per_paper
        ),
    )

    print()
    print("=" * 70)
    print("PAPER COMPARISON")
    print("=" * 70)

    print(
        f"Query   : {response.query}"
    )

    print(
        "Papers  : "
        + ", ".join(
            response.requested_papers
        )
    )

    print(
        "Matched : "
        + (
            ", ".join(
                response.matched_papers
            )
            if response.matched_papers
            else "None"
        )
    )

    if response.missing_papers:

        print(
            "Missing : "
            + ", ".join(
                response.missing_papers
            )
        )

    for comparison in (
        response.comparisons
    ):

        print()
        print("=" * 70)

        print(
            f"PAPER: "
            f"{comparison.paper_id}"
        )

        print("=" * 70)

        if not comparison.evidence:

            print(
                "No relevant evidence found."
            )

            continue

        for evidence in (
            comparison.evidence
        ):

            print()

            print(
                "-" * 70
            )

            print(
                f"Page          : "
                f"{evidence.page_number}"
            )

            print(
                f"Section       : "
                f"{evidence.section}"
            )

            print(
                f"Score         : "
                f"{evidence.score:.4f}"
            )

            print(
                f"Raw score     : "
                f"{evidence.raw_score:.4f}"
            )

            print(
                f"Lexical score : "
                f"{evidence.lexical_score:.4f}"
            )

            print(
                f"Chunk         : "
                f"{evidence.chunk_id}"
            )

            print()

            print(
                evidence.text
            )

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()