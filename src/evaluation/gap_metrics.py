from dataclasses import dataclass

from src.evaluation.models import (
    GapEvaluationResult,
)


@dataclass
class GapAggregateMetrics:
    case_count: int

    structural_pass_rate: float

    mean_signal_paper_coverage: float

    backend_validation_pass_rate: float

    candidate_evidence_reference_integrity: float

    mean_dimension_population_rate: float

    total_candidates: int

    total_explicit_candidates: int
    total_corpus_imbalance_candidates: int
    total_insufficient_evidence_candidates: int


def calculate_gap_metrics(
    results: list[
        GapEvaluationResult
    ],
) -> GapAggregateMetrics:

    if not results:

        return GapAggregateMetrics(
            case_count=0,

            structural_pass_rate=0.0,

            mean_signal_paper_coverage=0.0,

            backend_validation_pass_rate=0.0,

            candidate_evidence_reference_integrity=0.0,

            mean_dimension_population_rate=0.0,

            total_candidates=0,

            total_explicit_candidates=0,

            total_corpus_imbalance_candidates=0,

            total_insufficient_evidence_candidates=0,
        )

    count = len(
        results
    )

    total_candidate_references = sum(
        result.candidate_evidence_reference_count
        for result in results
    )

    total_missing_candidate_references = sum(
        len(
            result.missing_candidate_evidence_references
        )
        for result in results
    )

    if total_candidate_references:

        evidence_integrity = (
            total_candidate_references
            - total_missing_candidate_references
        ) / total_candidate_references

    else:

        evidence_integrity = 1.0

    return GapAggregateMetrics(
        case_count=count,

        structural_pass_rate=sum(
            result.structural_valid
            for result in results
        ) / count,

        mean_signal_paper_coverage=sum(
            result.signal_paper_coverage
            for result in results
        ) / count,

        backend_validation_pass_rate=sum(
            result.backend_validation_valid
            for result in results
        ) / count,

        candidate_evidence_reference_integrity=(
            evidence_integrity
        ),

        mean_dimension_population_rate=sum(
            result.dimension_population_rate
            for result in results
        ) / count,

        total_candidates=sum(
            result.candidate_count
            for result in results
        ),

        total_explicit_candidates=sum(
            result.explicit_candidate_count
            for result in results
        ),

        total_corpus_imbalance_candidates=sum(
            result.corpus_imbalance_candidate_count
            for result in results
        ),

        total_insufficient_evidence_candidates=sum(
            result.insufficient_evidence_candidate_count
            for result in results
        ),
    )