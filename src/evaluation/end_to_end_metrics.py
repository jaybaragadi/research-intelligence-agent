from dataclasses import dataclass

from src.evaluation.models import (
    EndToEndEvaluationResult,
)


@dataclass
class EndToEndAggregateMetrics:
    case_count: int

    structural_pass_rate: float
    mean_stage_success_rate: float

    answer_success_rate: float
    comparison_success_rate: float
    gap_analysis_success_rate: float
    literature_review_success_rate: float

    mean_comparison_paper_coverage: float
    mean_gap_paper_coverage: float
    mean_literature_review_paper_coverage: float

    total_answer_claims: int
    total_answer_evidence: int
    total_comparison_findings: int
    total_gap_candidates: int
    total_review_findings: int
    total_review_citations: int

    total_shared_evidence_ids: int


def calculate_end_to_end_metrics(
    results: list[
        EndToEndEvaluationResult
    ],
) -> EndToEndAggregateMetrics:

    if not results:

        return EndToEndAggregateMetrics(
            case_count=0,
            structural_pass_rate=0.0,
            mean_stage_success_rate=0.0,
            answer_success_rate=0.0,
            comparison_success_rate=0.0,
            gap_analysis_success_rate=0.0,
            literature_review_success_rate=0.0,
            mean_comparison_paper_coverage=0.0,
            mean_gap_paper_coverage=0.0,
            mean_literature_review_paper_coverage=0.0,
            total_answer_claims=0,
            total_answer_evidence=0,
            total_comparison_findings=0,
            total_gap_candidates=0,
            total_review_findings=0,
            total_review_citations=0,
            total_shared_evidence_ids=0,
        )

    count = len(
        results
    )

    answer_successes = sum(
        (
            result.answer_generated
            and result.answer_validation_valid
        )
        for result in results
    )

    comparison_successes = sum(
        (
            result.comparison_generated
            and result.comparison_paper_coverage == 1.0
            and not result.invalid_comparison_paper_references
        )
        for result in results
    )

    gap_successes = sum(
        (
            result.gap_analysis_generated
            and result.gap_validation_valid
            and result.gap_paper_coverage == 1.0
            and not result.invalid_gap_paper_references
        )
        for result in results
    )

    review_successes = sum(
        (
            result.literature_review_generated
            and result.literature_review_validation_valid
            and result.literature_review_paper_coverage == 1.0
            and not result.invalid_review_paper_references
        )
        for result in results
    )

    return EndToEndAggregateMetrics(
        case_count=count,

        structural_pass_rate=sum(
            result.structural_valid
            for result in results
        ) / count,

        mean_stage_success_rate=sum(
            result.stage_success_rate
            for result in results
        ) / count,

        answer_success_rate=(
            answer_successes / count
        ),

        comparison_success_rate=(
            comparison_successes / count
        ),

        gap_analysis_success_rate=(
            gap_successes / count
        ),

        literature_review_success_rate=(
            review_successes / count
        ),

        mean_comparison_paper_coverage=sum(
            result.comparison_paper_coverage
            for result in results
        ) / count,

        mean_gap_paper_coverage=sum(
            result.gap_paper_coverage
            for result in results
        ) / count,

        mean_literature_review_paper_coverage=sum(
            result.literature_review_paper_coverage
            for result in results
        ) / count,

        total_answer_claims=sum(
            result.answer_claim_count
            for result in results
        ),

        total_answer_evidence=sum(
            result.answer_evidence_count
            for result in results
        ),

        total_comparison_findings=sum(
            result.comparison_finding_count
            for result in results
        ),

        total_gap_candidates=sum(
            result.gap_candidate_count
            for result in results
        ),

        total_review_findings=sum(
            result.literature_review_finding_count
            for result in results
        ),

        total_review_citations=sum(
            result.literature_review_citation_count
            for result in results
        ),

        total_shared_evidence_ids=sum(
            result.shared_evidence_id_count
            for result in results
        ),
    )