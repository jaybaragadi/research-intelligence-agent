import argparse

from src.analysis.gap_analysis_service import (
    ResearchGapAnalysisService,
)
from src.analysis.gap_models import (
    ResearchGapAnalysis,
)


def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line parser for
    evidence-grounded research-gap analysis.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Analyze evidence-grounded research-gap "
            "candidates across an indexed paper corpus."
        )
    )

    parser.add_argument(
        "query",
        help=("Research-gap question or analysis focus."),
    )

    parser.add_argument(
        "--papers",
        nargs="+",
        required=True,
        help=("Paper IDs to include in the corpus."),
    )

    parser.add_argument(
        "--evidence-per-paper",
        type=int,
        default=8,
        help=(
            "Maximum comparative evidence passages " "retrieved per paper. Default: 8."
        ),
    )

    return parser


def print_analysis(
    analysis: ResearchGapAnalysis,
) -> None:
    """
    Print one research-gap analysis in a
    human-readable evidence-oriented format.
    """

    print("=" * 70)

    print("RESEARCH GAP ANALYSIS")

    print("=" * 70)

    print()

    print(f"Query: {analysis.query}")

    print("Corpus size: " f"{len(analysis.corpus_papers)} papers")

    print("Papers: " + ", ".join(analysis.corpus_papers))

    print()

    _print_explicit_signals(analysis)

    _print_dimension_coverage(analysis)

    _print_candidates(analysis)

    _print_validation(analysis)

    print()

    print("NOTE")

    print(
        "Results describe evidence patterns in the "
        "indexed corpus only. They do not prove that "
        "a gap exists across all published literature."
    )


def _print_explicit_signals(
    analysis: ResearchGapAnalysis,
) -> None:
    """
    Print explicit limitation, future-work,
    and unresolved-problem signals by paper.
    """

    print("EXPLICIT GAP SIGNALS")

    print("-" * 70)

    signal_count = sum(len(paper.signals) for paper in analysis.paper_signals)

    if signal_count == 0:

        print("No explicit gap signals found.")

        print()

        return

    for paper in analysis.paper_signals:

        if not paper.signals:
            continue

        print(paper.paper_id)

        for signal in paper.signals:

            print("  Signal: " f"{signal.signal_type.value}")

            print("  Evidence: " f"{signal.evidence_id}")

            print("  Page: " f"{signal.page_number}")

            if signal.section:

                print("  Section: " f"{signal.section}")

            print("  Score: " f"{signal.relevance_score:.2f}")

            print("  Text: " f"{signal.text}")

            print("  Citation: " f"{signal.citation_text}")

            print()

    print()


def _print_dimension_coverage(
    analysis: ResearchGapAnalysis,
) -> None:
    """
    Print corpus evidence coverage for each
    analytical dimension.
    """

    print("DIMENSION COVERAGE")

    print("-" * 70)

    corpus_size = len(analysis.corpus_papers)

    for coverage in analysis.dimension_coverage:

        print(
            f"{coverage.dimension}: "
            f"{coverage.paper_count}/"
            f"{corpus_size} papers, "
            f"{coverage.evidence_count} "
            "evidence passages"
        )

        if coverage.paper_ids:

            print("  Papers: " + ", ".join(coverage.paper_ids))

    print()


def _print_candidates(
    analysis: ResearchGapAnalysis,
) -> None:
    """
    Print candidate research gaps.

    Candidate wording remains deliberately
    corpus-scoped.
    """

    print("CANDIDATE GAPS")

    print("-" * 70)

    if not analysis.candidates:

        print("No evidence-supported gap candidates " "were produced.")

        print()

        return

    for candidate in analysis.candidates:

        print(candidate.gap_id)

        print("  Type: " f"{candidate.gap_type.value}")

        print("  Confidence: " f"{candidate.confidence.value.upper()}")

        print("  Title: " f"{candidate.title}")

        print("  Description: " f"{candidate.description}")

        print("  Reason: " f"{candidate.reason}")

        if candidate.dimensions:

            print("  Dimensions: " + ", ".join(candidate.dimensions))

        if candidate.paper_ids:

            print("  Papers: " + ", ".join(candidate.paper_ids))

        if candidate.evidence_ids:

            print("  Evidence: " + ", ".join(candidate.evidence_ids))

        print()


def _print_validation(
    analysis: ResearchGapAnalysis,
) -> None:
    """
    Print structural/provenance validation result.
    """

    print("VALIDATION")

    print("-" * 70)

    if analysis.validation is None:

        print("Validation was not run.")

        print()

        return

    print("Valid: " f"{analysis.validation.is_valid}")

    print("Validated candidates: " f"{analysis.validation.validated_gap_count}")

    print("Issues: " f"{analysis.validation.issue_count}")

    for issue in analysis.validation.issues:

        print("  " f"{issue.issue_type}: " f"{issue.message}")


def main() -> None:
    """
    Run research-gap analysis from the command line.
    """

    parser = build_parser()

    args = parser.parse_args()

    service = ResearchGapAnalysisService()

    analysis = service.analyze(
        paper_ids=args.papers,
        query=args.query,
        evidence_per_paper=(args.evidence_per_paper),
    )

    print_analysis(analysis)


if __name__ == "__main__":
    main()
