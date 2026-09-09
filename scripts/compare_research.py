import argparse

from src.analysis.comparative_service import (
    ComparativeAnalysisService,
)


def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "Run structured evidence-grounded "
            "comparative research analysis"
        )
    )

    parser.add_argument(
        "query",
        type=str,
    )

    parser.add_argument(
        "--papers",
        nargs="+",
        required=True,
    )

    args = (
        parser.parse_args()
    )

    service = (
        ComparativeAnalysisService()
    )

    result = (
        service.analyze(
            paper_ids=(
                args.papers
            ),

            query=(
                args.query
            ),
        )
    )

    print()
    print("=" * 78)
    print("COMPARATIVE RESEARCH ANALYSIS")
    print("=" * 78)

    print(
        f"Query: {result.query}"
    )

    print(
        "Papers: "
        + ", ".join(
            result.requested_papers
        )
    )

    print()
    print("COMPARISON MATRIX")
    print("-" * 78)

    for row in (
        result.matrix
    ):

        print()
        print(
            f"[{row.dimension}]"
        )

        for cell in (
            row.cells
        ):

            print(
                f"  {cell.paper_id}:"
            )

            if cell.summary:

                print(
                    f"    {cell.summary}"
                )

                print(
                    "    Evidence: "
                    + ", ".join(
                        cell.evidence_ids
                    )
                )

            else:

                print(
                    "    No matching "
                    "validated evidence."
                )

    print()
    print("CROSS-PAPER FINDINGS")
    print("-" * 78)

    if not result.findings:

        print(
            "No shared analytical dimensions "
            "were identified."
        )

    for finding in (
        result.findings
    ):

        print(
            f"{finding.finding_id}: "
            f"{finding.text}"
        )

        print(
            "  Papers: "
            + ", ".join(
                finding.paper_ids
            )
        )

        print(
            "  Evidence: "
            + ", ".join(
                finding.evidence_ids
            )
        )

    print()
    print("=" * 78)


if __name__ == "__main__":
    main()