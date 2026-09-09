from src.analysis.gap_models import (
    DimensionCoverage,
    GapCandidate,
    GapConfidence,
    GapEvidence,
    GapSignalType,
    GapType,
    ResearchGapAnalysis,
)


def test_gap_type_values_are_stable():

    assert (
        GapType.EXPLICIT.value
        == "explicit"
    )

    assert (
        GapType.CORPUS_IMBALANCE.value
        == "corpus_imbalance"
    )

    assert (
        GapType.INSUFFICIENT_EVIDENCE.value
        == "insufficient_evidence"
    )


def test_gap_evidence_preserves_provenance():

    evidence = GapEvidence(
        evidence_id=(
            "03_mutap_chunk_0001"
        ),

        paper_id="03_mutap",

        page_number=1,

        section="methodology",

        signal_type=(
            GapSignalType.LIMITATION
        ),

        text=(
            "A limitation of the "
            "approach is..."
        ),

        citation_text=(
            "MuTAP citation"
        ),

        relevance_score=2.0,
    )

    assert (
        evidence.paper_id
        == "03_mutap"
    )

    assert (
        evidence.page_number
        == 1
    )

    assert (
        evidence.evidence_id
        == "03_mutap_chunk_0001"
    )


def test_gap_candidate_preserves_support():

    candidate = GapCandidate(
        gap_id="G1",

        gap_type=(
            GapType.EXPLICIT
        ),

        title=(
            "Limited evaluation scope"
        ),

        description=(
            "The paper reports a "
            "restricted evaluation."
        ),

        confidence=(
            GapConfidence.HIGH
        ),

        paper_ids=[
            "03_mutap"
        ],

        evidence_ids=[
            "03_mutap_chunk_0001"
        ],

        dimensions=[
            "evaluation_method"
        ],

        reason=(
            "Explicit limitation "
            "language was found."
        ),
    )

    assert candidate.gap_id == "G1"

    assert candidate.evidence_ids == [
        "03_mutap_chunk_0001"
    ]

    assert (
        candidate.confidence
        == GapConfidence.HIGH
    )


def test_research_gap_analysis_can_start_empty():

    result = ResearchGapAnalysis(
        query="Find research gaps",

        corpus_papers=[
            "03_mutap",
            "05_coverup",
        ],

        paper_signals=[],

        dimension_coverage=[],

        candidates=[],
    )

    assert (
        result.validation
        is None
    )

    assert (
        result.candidates
        == []
    )


def test_dimension_coverage_tracks_papers():

    coverage = DimensionCoverage(
        dimension=(
            "quality_objective"
        ),

        paper_count=2,

        evidence_count=4,

        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],

        evidence_ids=[
            "m1",
            "m2",
            "c1",
            "c2",
        ],
    )

    assert coverage.paper_count == 2

    assert coverage.evidence_count == 4