from src.evaluation.end_to_end_metrics import (
    calculate_end_to_end_metrics,
)

from src.evaluation.models import (
    EndToEndEvaluationResult,
)


def build_valid_result():
    return EndToEndEvaluationResult(
        workflow_id="E2E1",
        query="test query",
        requested_papers=[
            "03_mutap",
            "05_coverup",
        ],

        answer_generated=True,
        answer_claim_count=5,
        answer_evidence_count=8,
        answer_validation_valid=True,

        comparison_generated=True,
        comparison_profile_count=2,
        comparison_matrix_row_count=6,
        comparison_finding_count=4,
        comparison_paper_coverage=1.0,

        gap_analysis_generated=True,
        gap_signal_count=3,
        gap_candidate_count=2,
        gap_validation_valid=True,
        gap_paper_coverage=1.0,

        literature_review_generated=True,
        literature_review_section_count=8,
        literature_review_finding_count=5,
        literature_review_citation_count=20,
        literature_review_validation_valid=True,
        literature_review_paper_coverage=1.0,

        shared_evidence_id_count=4,

        invalid_comparison_paper_references=[],
        invalid_gap_paper_references=[],
        invalid_review_paper_references=[],

        stage_success_count=4,
        total_stage_count=4,
        stage_success_rate=1.0,

        structural_valid=True,
    )


def test_end_to_end_metrics_valid_result():

    result = build_valid_result()

    metrics = calculate_end_to_end_metrics(
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
        metrics.mean_stage_success_rate
        == 1.0
    )

    assert (
        metrics.answer_success_rate
        == 1.0
    )

    assert (
        metrics.comparison_success_rate
        == 1.0
    )

    assert (
        metrics.gap_analysis_success_rate
        == 1.0
    )

    assert (
        metrics.literature_review_success_rate
        == 1.0
    )

    assert (
        metrics.mean_comparison_paper_coverage
        == 1.0
    )

    assert (
        metrics.mean_gap_paper_coverage
        == 1.0
    )

    assert (
        metrics.mean_literature_review_paper_coverage
        == 1.0
    )


def test_end_to_end_metrics_totals():

    result = build_valid_result()

    metrics = calculate_end_to_end_metrics(
        [
            result,
        ]
    )

    assert (
        metrics.total_answer_claims
        == 5
    )

    assert (
        metrics.total_answer_evidence
        == 8
    )

    assert (
        metrics.total_comparison_findings
        == 4
    )

    assert (
        metrics.total_gap_candidates
        == 2
    )

    assert (
        metrics.total_review_findings
        == 5
    )

    assert (
        metrics.total_review_citations
        == 20
    )

    assert (
        metrics.total_shared_evidence_ids
        == 4
    )