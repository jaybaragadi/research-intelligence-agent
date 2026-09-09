import pytest

from src.analysis.gap_models import (
    GapConfidence,
    GapEvidence,
    GapSignalType,
)

from src.analysis.gap_scorer import (
    GapConfidenceScorer,
)


def make_evidence(
    evidence_id: str,
    signal_type: GapSignalType,
    score: float,
) -> GapEvidence:

    return GapEvidence(
        evidence_id=evidence_id,

        paper_id="paper_a",

        page_number=1,

        section="discussion",

        signal_type=signal_type,

        text="Evidence text",

        citation_text="Citation",

        relevance_score=score,
    )


def test_explicit_limitation_can_score_high():

    scorer = GapConfidenceScorer()

    confidence = scorer.score_explicit(
        signal_type=(
            GapSignalType.LIMITATION
        ),

        evidence=[
            make_evidence(
                "e1",
                GapSignalType.LIMITATION,
                2.0,
            )
        ],
    )

    assert (
        confidence
        == GapConfidence.HIGH
    )


def test_future_work_can_score_high():

    scorer = GapConfidenceScorer()

    confidence = scorer.score_explicit(
        signal_type=(
            GapSignalType.FUTURE_WORK
        ),

        evidence=[
            make_evidence(
                "e1",
                GapSignalType.FUTURE_WORK,
                2.5,
            )
        ],
    )

    assert (
        confidence
        == GapConfidence.HIGH
    )


def test_unresolved_problem_is_more_conservative():

    scorer = GapConfidenceScorer()

    confidence = scorer.score_explicit(
        signal_type=(
            GapSignalType.UNRESOLVED_PROBLEM
        ),

        evidence=[
            make_evidence(
                "e1",
                GapSignalType.UNRESOLVED_PROBLEM,
                2.0,
            )
        ],
    )

    assert (
        confidence
        == GapConfidence.MEDIUM
    )


def test_multiple_unresolved_signals_can_score_high():

    scorer = GapConfidenceScorer()

    confidence = scorer.score_explicit(
        signal_type=(
            GapSignalType.UNRESOLVED_PROBLEM
        ),

        evidence=[
            make_evidence(
                "e1",
                GapSignalType.UNRESOLVED_PROBLEM,
                2.0,
            ),

            make_evidence(
                "e2",
                GapSignalType.UNRESOLVED_PROBLEM,
                2.0,
            ),
        ],
    )

    assert (
        confidence
        == GapConfidence.HIGH
    )


def test_empty_explicit_evidence_is_low():

    scorer = GapConfidenceScorer()

    confidence = scorer.score_explicit(
        signal_type=(
            GapSignalType.LIMITATION
        ),

        evidence=[],
    )

    assert (
        confidence
        == GapConfidence.LOW
    )


def test_strong_imbalance_scores_high():

    scorer = GapConfidenceScorer()

    confidence = scorer.score_imbalance(
        high_paper_count=9,
        low_paper_count=1,
        corpus_size=10,
    )

    assert (
        confidence
        == GapConfidence.HIGH
    )


def test_moderate_imbalance_scores_medium():

    scorer = GapConfidenceScorer()

    confidence = scorer.score_imbalance(
        high_paper_count=7,
        low_paper_count=3,
        corpus_size=10,
    )

    assert (
        confidence
        == GapConfidence.MEDIUM
    )


def test_small_difference_scores_low():

    scorer = GapConfidenceScorer()

    confidence = scorer.score_imbalance(
        high_paper_count=6,
        low_paper_count=4,
        corpus_size=10,
    )

    assert (
        confidence
        == GapConfidence.LOW
    )


def test_zero_low_coverage_is_low():

    scorer = GapConfidenceScorer()

    confidence = scorer.score_imbalance(
        high_paper_count=8,
        low_paper_count=0,
        corpus_size=10,
    )

    assert (
        confidence
        == GapConfidence.LOW
    )


def test_invalid_corpus_size_raises():

    scorer = GapConfidenceScorer()

    with pytest.raises(
        ValueError
    ):

        scorer.score_imbalance(
            high_paper_count=1,
            low_paper_count=1,
            corpus_size=0,
        )


def test_paper_count_cannot_exceed_corpus():

    scorer = GapConfidenceScorer()

    with pytest.raises(
        ValueError
    ):

        scorer.score_imbalance(
            high_paper_count=11,
            low_paper_count=1,
            corpus_size=10,
        )