from dataclasses import dataclass

from src.evaluation.models import (
    ComparisonEvaluationResult,
)


@dataclass
class ComparisonAggregateMetrics:
    case_count: int

    structural_pass_rate: float

    mean_profile_paper_coverage: float
    mean_matrix_paper_coverage: float

    mean_matrix_population_rate: float

    cell_evidence_reference_integrity: float
    finding_evidence_reference_integrity: float


def calculate_comparison_metrics(
    results: list[ComparisonEvaluationResult],
) -> ComparisonAggregateMetrics:

    if not results:

        return ComparisonAggregateMetrics(
            case_count=0,
            structural_pass_rate=0.0,
            mean_profile_paper_coverage=0.0,
            mean_matrix_paper_coverage=0.0,
            mean_matrix_population_rate=0.0,
            cell_evidence_reference_integrity=0.0,
            finding_evidence_reference_integrity=0.0,
        )

    count = len(results)

    total_cell_references = sum(
        result.populated_cell_evidence_reference_count for result in results
    )

    total_missing_cell_references = sum(
        len(result.missing_cell_evidence_references) for result in results
    )

    if total_cell_references:

        cell_integrity = (
            total_cell_references - total_missing_cell_references
        ) / total_cell_references

    else:

        cell_integrity = 1.0

    total_finding_references = sum(
        result.finding_evidence_reference_count for result in results
    )

    total_missing_finding_references = sum(
        len(result.missing_finding_evidence_references) for result in results
    )

    if total_finding_references:

        finding_integrity = (
            total_finding_references - total_missing_finding_references
        ) / total_finding_references

    else:

        finding_integrity = 1.0

    return ComparisonAggregateMetrics(
        case_count=count,
        structural_pass_rate=sum(result.structural_valid for result in results) / count,
        mean_profile_paper_coverage=sum(
            result.profile_paper_coverage for result in results
        )
        / count,
        mean_matrix_paper_coverage=sum(
            result.matrix_paper_coverage for result in results
        )
        / count,
        mean_matrix_population_rate=sum(
            result.matrix_population_rate for result in results
        )
        / count,
        cell_evidence_reference_integrity=(cell_integrity),
        finding_evidence_reference_integrity=(finding_integrity),
    )
