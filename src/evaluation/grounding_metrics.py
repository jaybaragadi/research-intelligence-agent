from dataclasses import dataclass

from src.evaluation.models import (
    GroundingEvaluationResult,
)


@dataclass
class GroundingAggregateMetrics:
    case_count: int

    backend_validation_pass_rate: float

    mean_claim_evidence_coverage: float

    mean_provenance_completeness: float

    evidence_reference_integrity: float

    mean_expected_paper_recall: float


def calculate_grounding_metrics(
    results: list[GroundingEvaluationResult],
) -> GroundingAggregateMetrics:

    if not results:

        return GroundingAggregateMetrics(
            case_count=0,
            backend_validation_pass_rate=0.0,
            mean_claim_evidence_coverage=0.0,
            mean_provenance_completeness=0.0,
            evidence_reference_integrity=0.0,
            mean_expected_paper_recall=0.0,
        )

    count = len(results)

    total_references = sum(result.referenced_evidence_count for result in results)

    missing_references = sum(
        len(result.missing_evidence_references) for result in results
    )

    if total_references:

        reference_integrity = (total_references - missing_references) / total_references

    else:

        reference_integrity = 0.0

    return GroundingAggregateMetrics(
        case_count=count,
        backend_validation_pass_rate=sum(
            result.backend_validation_valid for result in results
        )
        / count,
        mean_claim_evidence_coverage=sum(
            result.claim_evidence_coverage for result in results
        )
        / count,
        mean_provenance_completeness=sum(
            result.provenance_completeness for result in results
        )
        / count,
        evidence_reference_integrity=(reference_integrity),
        mean_expected_paper_recall=sum(
            result.expected_paper_recall for result in results
        )
        / count,
    )
