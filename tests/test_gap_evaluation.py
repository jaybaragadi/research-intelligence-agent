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

from src.evaluation.gap_evaluator import (
    GapEvaluator,
)

from src.evaluation.gap_metrics import (
    calculate_gap_metrics,
)

from src.evaluation.models import (
    GapBenchmarkCase,
)


class FakeGapService:

    def analyze(
        self,
        paper_ids: list[str],
        query: str,
        evidence_per_paper: int = 8,
    ) -> ResearchGapAnalysis:

        evidence = GapEvidence(
            evidence_id="E1",
            paper_id="03_mutap",
            page_number=5,
            section="Limitations",
            signal_type=(
                GapSignalType.LIMITATION
            ),
            text="The approach has a limitation.",
            citation_text="03_mutap, page 5",
            relevance_score=1.0,
        )

        paper_signals = [
            PaperGapSignals(
                paper_id="03_mutap",
                signals=[
                    evidence
                ],
            ),
            PaperGapSignals(
                paper_id="05_coverup",
                signals=[],
            ),
        ]

        dimension_coverage = [
            DimensionCoverage(
                dimension="limitations",
                paper_count=1,
                evidence_count=1,
                paper_ids=[
                    "03_mutap"
                ],
                evidence_ids=[
                    "E1"
                ],
            ),
            DimensionCoverage(
                dimension="feedback_signal",
                paper_count=0,
                evidence_count=0,
                paper_ids=[],
                evidence_ids=[],
            ),
        ]

        candidates = [
            GapCandidate(
                gap_id="G1",
                gap_type=GapType.EXPLICIT,
                title="Reported limitation",
                description=(
                    "A reported limitation "
                    "was found."
                ),
                confidence=GapConfidence.HIGH,
                paper_ids=[
                    "03_mutap"
                ],
                evidence_ids=[
                    "E1"
                ],
                dimensions=[
                    "limitations"
                ],
                reason="Explicit limitation evidence.",
            )
        ]

        validation = GapValidationResult(
            is_valid=True,
            validated_gap_count=1,
            issue_count=0,
            issues=[],
        )

        return ResearchGapAnalysis(
            query=query,
            corpus_papers=paper_ids,
            paper_signals=paper_signals,
            dimension_coverage=dimension_coverage,
            candidates=candidates,
            validation=validation,
        )


def test_gap_evaluator_valid_case():

    case = GapBenchmarkCase(
        gap_id="GAP1",
        query="research limitations",
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    evaluator = GapEvaluator(
        gap_service=FakeGapService()
    )

    result = evaluator.evaluate_case(
        case
    )

    assert (
        result.signal_paper_coverage
        == 1.0
    )

    assert result.signal_count == 1

    assert result.candidate_count == 1

    assert (
        result.explicit_candidate_count
        == 1
    )

    assert (
        result.corpus_imbalance_candidate_count
        == 0
    )

    assert (
        result.insufficient_evidence_candidate_count
        == 0
    )

    assert (
        result.candidate_evidence_reference_integrity
        == 1.0
    )

    assert (
        result.missing_candidate_evidence_references
        == []
    )

    assert (
        result.invalid_candidate_paper_references
        == []
    )

    assert (
        result.dimension_population_rate
        == 0.5
    )

    assert (
        result.backend_validation_valid
        is True
    )

    assert (
        result.structural_valid
        is True
    )


def test_gap_metrics():

    case = GapBenchmarkCase(
        gap_id="GAP1",
        query="research limitations",
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    result = GapEvaluator(
        gap_service=FakeGapService()
    ).evaluate_case(
        case
    )

    metrics = calculate_gap_metrics(
        [
            result,
        ]
    )

    assert metrics.case_count == 1

    assert (
        metrics.structural_pass_rate
        == 1.0
    )

    assert (
        metrics.mean_signal_paper_coverage
        == 1.0
    )

    assert (
        metrics.backend_validation_pass_rate
        == 1.0
    )

    assert (
        metrics.candidate_evidence_reference_integrity
        == 1.0
    )

    assert (
        metrics.mean_dimension_population_rate
        == 0.5
    )

    assert metrics.total_candidates == 1

    assert (
        metrics.total_explicit_candidates
        == 1
    )