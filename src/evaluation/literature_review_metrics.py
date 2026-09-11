from dataclasses import dataclass

from src.evaluation.models import (
    LiteratureReviewEvaluationResult,
)


@dataclass
class LiteratureReviewAggregateMetrics:
    case_count: int

    structural_pass_rate: float
    backend_validation_pass_rate: float

    mean_review_paper_coverage: float
    section_structure_pass_rate: float

    mean_finding_evidence_coverage: float
    finding_evidence_reference_integrity: float
    mean_provenance_completeness: float

    corpus_scope_note_pass_rate: float

    total_findings: int
    total_evidence_placements: int
    total_citations: int


def calculate_literature_review_metrics(
    results: list[LiteratureReviewEvaluationResult],
) -> LiteratureReviewAggregateMetrics:

    if not results:

        return LiteratureReviewAggregateMetrics(
            case_count=0,
            structural_pass_rate=0.0,
            backend_validation_pass_rate=0.0,
            mean_review_paper_coverage=0.0,
            section_structure_pass_rate=0.0,
            mean_finding_evidence_coverage=0.0,
            finding_evidence_reference_integrity=0.0,
            mean_provenance_completeness=0.0,
            corpus_scope_note_pass_rate=0.0,
            total_findings=0,
            total_evidence_placements=0,
            total_citations=0,
        )

    count = len(results)

    total_finding_references = sum(
        result.finding_evidence_reference_count for result in results
    )

    total_missing_finding_references = sum(
        len(result.missing_finding_evidence_references) for result in results
    )

    if total_finding_references:

        finding_reference_integrity = (
            total_finding_references - total_missing_finding_references
        ) / total_finding_references

    else:

        finding_reference_integrity = 1.0

    return LiteratureReviewAggregateMetrics(
        case_count=count,
        structural_pass_rate=sum(result.structural_valid for result in results) / count,
        backend_validation_pass_rate=sum(
            result.backend_validation_valid for result in results
        )
        / count,
        mean_review_paper_coverage=sum(
            result.review_paper_coverage for result in results
        )
        / count,
        section_structure_pass_rate=sum(
            result.section_structure_complete for result in results
        )
        / count,
        mean_finding_evidence_coverage=sum(
            result.finding_evidence_coverage for result in results
        )
        / count,
        finding_evidence_reference_integrity=(finding_reference_integrity),
        mean_provenance_completeness=sum(
            result.provenance_completeness for result in results
        )
        / count,
        corpus_scope_note_pass_rate=sum(
            result.corpus_scope_note_present for result in results
        )
        / count,
        total_findings=sum(result.finding_count for result in results),
        total_evidence_placements=sum(result.evidence_count for result in results),
        total_citations=sum(result.citation_count for result in results),
    )
