from src.analysis.comparison_models import (
    DimensionEvidence,
)

from src.analysis.corpus_coverage import (
    CorpusCoverageAnalyzer,
)


def make_evidence(
    evidence_id: str,
    paper_id: str,
    dimension: str,
) -> DimensionEvidence:

    return DimensionEvidence(
        evidence_id=evidence_id,

        paper_id=paper_id,

        dimension=dimension,

        page_number=1,

        section="methodology",

        text="Evidence text",

        citation_text="Citation",

        relevance_score=2.0,
    )


def test_analyzes_dimension_coverage():

    evidence = [
        make_evidence(
            "e1",
            "paper_a",
            "quality_objective",
        ),

        make_evidence(
            "e2",
            "paper_b",
            "quality_objective",
        ),

        make_evidence(
            "e3",
            "paper_a",
            "evaluation_method",
        ),
    ]

    results = (
        CorpusCoverageAnalyzer()
        .analyze(
            evidence
        )
    )

    lookup = {
        result.dimension: result
        for result in results
    }

    quality = lookup[
        "quality_objective"
    ]

    assert (
        quality.paper_count
        == 2
    )

    assert (
        quality.evidence_count
        == 2
    )


def test_same_paper_is_counted_once():

    evidence = [
        make_evidence(
            "e1",
            "paper_a",
            "feedback_signal",
        ),

        make_evidence(
            "e2",
            "paper_a",
            "feedback_signal",
        ),
    ]

    results = (
        CorpusCoverageAnalyzer()
        .analyze(
            evidence
        )
    )

    assert len(results) == 1

    coverage = results[0]

    assert (
        coverage.paper_count
        == 1
    )

    assert (
        coverage.evidence_count
        == 2
    )


def test_duplicate_evidence_id_is_counted_once():

    evidence = [
        make_evidence(
            "e1",
            "paper_a",
            "feedback_signal",
        ),

        make_evidence(
            "e1",
            "paper_a",
            "feedback_signal",
        ),
    ]

    results = (
        CorpusCoverageAnalyzer()
        .analyze(
            evidence
        )
    )

    assert (
        results[0].evidence_count
        == 1
    )


def test_requested_missing_dimension_is_preserved():

    evidence = [
        make_evidence(
            "e1",
            "paper_a",
            "quality_objective",
        )
    ]

    results = (
        CorpusCoverageAnalyzer()
        .analyze_for_dimensions(
            evidence=evidence,

            dimensions=[
                "quality_objective",
                "limitations",
            ],
        )
    )

    lookup = {
        result.dimension: result
        for result in results
    }

    missing = lookup[
        "limitations"
    ]

    assert (
        missing.paper_count
        == 0
    )

    assert (
        missing.evidence_count
        == 0
    )

    assert (
        missing.paper_ids
        == []
    )


def test_requested_dimension_order_is_preserved():

    results = (
        CorpusCoverageAnalyzer()
        .analyze_for_dimensions(
            evidence=[],

            dimensions=[
                "limitations",
                "feedback_signal",
                "quality_objective",
            ],
        )
    )

    assert [
        result.dimension
        for result in results
    ] == [
        "limitations",
        "feedback_signal",
        "quality_objective",
    ]


def test_dimension_evidence_ids_preserve_order():

    evidence = [
        make_evidence(
            "e2",
            "paper_b",
            "evaluation_method",
        ),

        make_evidence(
            "e1",
            "paper_a",
            "evaluation_method",
        ),

        make_evidence(
            "e2",
            "paper_b",
            "evaluation_method",
        ),
    ]

    results = (
        CorpusCoverageAnalyzer()
        .analyze(
            evidence
        )
    )

    assert (
        results[0].evidence_ids
        == [
            "e2",
            "e1",
        ]
    )