import argparse

from src.generation.answer_service import (
    GroundedAnswerService,
)


def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "Generate a validated grounded "
            "research answer"
        )
    )

    parser.add_argument(
        "query",
        type=str,
    )

    parser.add_argument(
        "--papers",
        nargs="*",
        default=None,
        help=(
            "Optional paper IDs for comparison"
        ),
    )

    args = (
        parser.parse_args()
    )

    service = (
        GroundedAnswerService()
    )

    if (
        args.papers
        and len(args.papers) >= 2
    ):

        answer = (
            service.answer_comparison(
                paper_ids=(
                    args.papers
                ),

                query=(
                    args.query
                ),
            )
        )

    else:

        answer = (
            service.answer_search(
                query=(
                    args.query
                )
            )
        )

    print()
    print("=" * 70)
    print("GROUNDED RESEARCH ANSWER")
    print("=" * 70)

    print(
        f"Query: {answer.query}"
    )

    print()
    print("ANSWER")
    print("-" * 70)
    print(
        answer.answer_text
    )

    print()
    print("CLAIMS")
    print("-" * 70)

    for claim in (
        answer.claims
    ):

        print(
            f"{claim.claim_id}: "
            f"{claim.text}"
        )

        print(
            "Evidence: "
            + ", ".join(
                claim.evidence_ids
            )
        )

    used_evidence_ids = {
        evidence_id

        for claim in answer.claims

        for evidence_id
        in claim.evidence_ids
    }

    print()
    print("SOURCES")
    print("-" * 70)

    for evidence in (
        answer.evidence
    ):

        if (
            evidence.evidence_id
            not in used_evidence_ids
        ):
            continue

        print(
            f"[{evidence.label}] "
            f"{evidence.citation_text}"
        )

    print()
    print("GROUNDING VALIDATION")
    print("-" * 70)

    print(
        f"Valid claims : "
        f"{answer.validation.validated_claim_count}"
    )

    print(
        f"Issues       : "
        f"{answer.validation.issue_count}"
    )

    print(
        f"Valid        : "
        f"{answer.validation.is_valid}"
    )

    if answer.validation.issues:

        for issue in (
            answer.validation.issues
        ):

            print(
                f"- {issue.issue_type}: "
                f"{issue.message}"
            )

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()