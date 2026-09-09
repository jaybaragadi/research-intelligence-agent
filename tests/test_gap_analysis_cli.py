from src.analysis.gap_models import (
    DimensionCoverage,
    GapCandidate,
    GapConfidence,
    GapEvidence,
    GapSignalType,
    GapType,
    GapValidationResult,
    PaperGapSignals,
    ResearchGapAnalysis,
)

from scripts.analyze_gaps import (
    build_parser,
    print_analysis,
)


def make_analysis() -> ResearchGapAnalysis:

    signal = GapEvidence(
        evidence_id="e1",

        paper_id="paper_a",

        page_number=3,

        section="discussion",

        signal_type=(
            GapSignalType.FUTURE_WORK
        ),

        text=(
            "In future work, we plan to "
            "investigate additional datasets."
        ),

        citation_text=(
            "Paper A (2025), p. 3"
        ),

        relevance_score=2.5,
    )

    candidate = GapCandidate(
        gap_id="G1",

        gap_type=(
            GapType.EXPLICIT
        ),

        title=(
            "Explicit future-work direction"
        ),

        description=(
            "Paper 'paper_a' contains "
            "validated future-work evidence."
        ),

        confidence=(
            GapConfidence.HIGH
        ),

        paper_ids=[
            "paper_a"
        ],

        evidence_ids=[
            "e1"
        ],

        dimensions=[],

        reason=(
            "Explicit future-work language "
            "was found."
        ),
    )

    return ResearchGapAnalysis(
        query=(
            "Find research gaps"
        ),

        corpus_papers=[
            "paper_a",
            "paper_b",
        ],

        paper_signals=[
            PaperGapSignals(
                paper_id="paper_a",
                signals=[signal],
            ),

            PaperGapSignals(
                paper_id="paper_b",
                signals=[],
            ),
        ],

        dimension_coverage=[
            DimensionCoverage(
                dimension=(
                    "quality_objective"
                ),

                paper_count=2,

                evidence_count=3,

                paper_ids=[
                    "paper_a",
                    "paper_b",
                ],

                evidence_ids=[
                    "q1",
                    "q2",
                    "q3",
                ],
            )
        ],

        candidates=[
            candidate
        ],

        validation=(
            GapValidationResult(
                is_valid=True,

                validated_gap_count=1,

                issue_count=0,

                issues=[],
            )
        ),
    )


def test_parser_reads_papers():

    parser = build_parser()

    args = parser.parse_args(
        [
            "Find research gaps",

            "--papers",
            "paper_a",
            "paper_b",
        ]
    )

    assert args.query == (
        "Find research gaps"
    )

    assert args.papers == [
        "paper_a",
        "paper_b",
    ]


def test_parser_default_evidence_count():

    parser = build_parser()

    args = parser.parse_args(
        [
            "Find gaps",

            "--papers",
            "paper_a",
            "paper_b",
        ]
    )

    assert (
        args.evidence_per_paper
        == 8
    )


def test_prints_candidate_gap(
    capsys,
):

    print_analysis(
        make_analysis()
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert (
        "RESEARCH GAP ANALYSIS"
        in output
    )

    assert (
        "Explicit future-work direction"
        in output
    )

    assert (
        "Confidence: HIGH"
        in output
    )

    assert (
        "Evidence: e1"
        in output
    )


def test_prints_dimension_coverage(
    capsys,
):

    print_analysis(
        make_analysis()
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert (
        "quality_objective: "
        "2/2 papers"
        in output
    )


def test_prints_corpus_scope_warning(
    capsys,
):

    print_analysis(
        make_analysis()
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert (
        "indexed corpus only"
        in output
    )

    assert (
        "do not prove"
        in output
    )