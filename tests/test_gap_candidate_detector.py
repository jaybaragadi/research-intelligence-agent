import pytest

from src.analysis.gap_candidate_detector import (
    GapCandidateDetector,
)
from src.analysis.gap_models import (
    DimensionCoverage,
    GapConfidence,
    GapEvidence,
    GapSignalType,
    GapType,
)


def make_signal(
    evidence_id: str,
    paper_id: str,
    signal_type: GapSignalType,
    score: float = 2.0,
) -> GapEvidence:

    return GapEvidence(
        evidence_id=evidence_id,
        paper_id=paper_id,
        page_number=1,
        section="discussion",
        signal_type=signal_type,
        text="Evidence text",
        citation_text="Citation",
        relevance_score=score,
    )


def make_coverage(
    dimension: str,
    paper_ids: list[str],
    evidence_ids: list[str],
) -> DimensionCoverage:

    return DimensionCoverage(
        dimension=dimension,
        paper_count=len(paper_ids),
        evidence_count=len(evidence_ids),
        paper_ids=paper_ids,
        evidence_ids=evidence_ids,
    )


def test_builds_explicit_limitation_candidate():

    detector = GapCandidateDetector()

    signals = [
        make_signal(
            "e1",
            "paper_a",
            GapSignalType.LIMITATION,
            score=2.0,
        )
    ]

    candidates = detector.build_explicit_candidates(signals)

    assert len(candidates) == 1

    candidate = candidates[0]

    assert candidate.gap_type == GapType.EXPLICIT

    assert candidate.confidence == GapConfidence.HIGH

    assert candidate.evidence_ids == ["e1"]


def test_groups_same_signal_for_same_paper():

    detector = GapCandidateDetector()

    signals = [
        make_signal(
            "e1",
            "paper_a",
            GapSignalType.FUTURE_WORK,
        ),
        make_signal(
            "e2",
            "paper_a",
            GapSignalType.FUTURE_WORK,
        ),
    ]

    candidates = detector.build_explicit_candidates(signals)

    assert len(candidates) == 1

    assert candidates[0].evidence_ids == [
        "e1",
        "e2",
    ]


def test_different_signal_types_create_separate_candidates():

    detector = GapCandidateDetector()

    signals = [
        make_signal(
            "e1",
            "paper_a",
            GapSignalType.LIMITATION,
        ),
        make_signal(
            "e2",
            "paper_a",
            GapSignalType.FUTURE_WORK,
        ),
    ]

    candidates = detector.build_explicit_candidates(signals)

    assert len(candidates) == 2


def test_zero_coverage_does_not_create_imbalance_gap():

    detector = GapCandidateDetector()

    coverage = [
        make_coverage(
            "quality_objective",
            [
                "p1",
                "p2",
                "p3",
                "p4",
                "p5",
            ],
            [
                "e1",
                "e2",
                "e3",
                "e4",
                "e5",
            ],
        ),
        make_coverage(
            "limitations",
            [],
            [],
        ),
    ]

    candidates = detector.build_imbalance_candidates(
        coverage=coverage,
        corpus_size=5,
    )

    assert candidates == []


def test_low_nonzero_coverage_can_create_imbalance():

    detector = GapCandidateDetector()

    coverage = [
        make_coverage(
            "quality_objective",
            [
                "p1",
                "p2",
                "p3",
                "p4",
                "p5",
                "p6",
                "p7",
                "p8",
            ],
            [
                "q1",
                "q2",
                "q3",
                "q4",
                "q5",
                "q6",
                "q7",
                "q8",
            ],
        ),
        make_coverage(
            "limitations",
            [
                "p1",
                "p2",
            ],
            [
                "l1",
                "l2",
            ],
        ),
    ]

    candidates = detector.build_imbalance_candidates(
        coverage=coverage,
        corpus_size=10,
    )

    assert len(candidates) == 1

    candidate = candidates[0]

    assert candidate.gap_type == GapType.CORPUS_IMBALANCE

    assert candidate.dimensions == [
        "quality_objective",
        "limitations",
    ]


def test_similar_coverage_does_not_create_candidate():

    detector = GapCandidateDetector()

    coverage = [
        make_coverage(
            "quality_objective",
            [
                "p1",
                "p2",
                "p3",
                "p4",
                "p5",
                "p6",
            ],
            [
                "q1",
                "q2",
                "q3",
                "q4",
                "q5",
                "q6",
            ],
        ),
        make_coverage(
            "feedback_signal",
            [
                "p1",
                "p2",
                "p3",
                "p4",
            ],
            [
                "f1",
                "f2",
                "f3",
                "f4",
            ],
        ),
    ]

    candidates = detector.build_imbalance_candidates(
        coverage=coverage,
        corpus_size=10,
    )

    assert candidates == []


def test_small_corpus_does_not_create_imbalance():

    detector = GapCandidateDetector()

    coverage = [
        make_coverage(
            "quality_objective",
            ["p1"],
            ["e1"],
        ),
        make_coverage(
            "limitations",
            ["p2"],
            ["e2"],
        ),
    ]

    candidates = detector.build_imbalance_candidates(
        coverage=coverage,
        corpus_size=1,
    )

    assert candidates == []


def test_invalid_ratio_configuration_raises():

    detector = GapCandidateDetector()

    with pytest.raises(ValueError):

        detector.build_imbalance_candidates(
            coverage=[],
            corpus_size=10,
            minimum_high_coverage_ratio=0.2,
            maximum_low_coverage_ratio=0.4,
        )


def test_strong_imbalance_gets_high_confidence():

    detector = GapCandidateDetector()

    coverage = [
        make_coverage(
            "evaluation_method",
            [
                "p1",
                "p2",
                "p3",
                "p4",
                "p5",
                "p6",
                "p7",
                "p8",
                "p9",
            ],
            [
                "e1",
                "e2",
                "e3",
                "e4",
                "e5",
                "e6",
                "e7",
                "e8",
                "e9",
            ],
        ),
        make_coverage(
            "limitations",
            ["p1"],
            ["l1"],
        ),
    ]

    candidates = detector.build_imbalance_candidates(
        coverage=coverage,
        corpus_size=10,
    )

    assert len(candidates) == 1

    assert candidates[0].confidence == GapConfidence.HIGH
