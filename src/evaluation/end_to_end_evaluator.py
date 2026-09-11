from src.analysis.comparative_service import (
    ComparativeAnalysisService,
)
from src.analysis.gap_analysis_service import (
    ResearchGapAnalysisService,
)
from src.analysis.literature_review_service import (
    LiteratureReviewService,
)
from src.evaluation.models import (
    EndToEndBenchmarkCase,
    EndToEndEvaluationResult,
)
from src.generation.answer_service import (
    GroundedAnswerService,
)


class EndToEndEvaluator:

    def __init__(
        self,
        answer_service: GroundedAnswerService | None = None,
        comparison_service: ComparativeAnalysisService | None = None,
        gap_service: ResearchGapAnalysisService | None = None,
        review_service: LiteratureReviewService | None = None,
    ) -> None:

        self.answer_service = (
            answer_service if answer_service is not None else GroundedAnswerService()
        )

        self.comparison_service = (
            comparison_service
            if comparison_service is not None
            else ComparativeAnalysisService()
        )

        self.gap_service = (
            gap_service if gap_service is not None else ResearchGapAnalysisService()
        )

        self.review_service = (
            review_service if review_service is not None else LiteratureReviewService()
        )

    def evaluate_case(
        self,
        case: EndToEndBenchmarkCase,
        top_k: int = 8,
        evidence_per_paper: int = 8,
    ) -> EndToEndEvaluationResult:

        requested_set = set(case.paper_ids)

        answer = self.answer_service.answer_search(
            query=case.query,
            top_k=top_k,
        )

        comparison = self.comparison_service.analyze(
            paper_ids=case.paper_ids,
            query=case.query,
            evidence_per_paper=evidence_per_paper,
        )

        gap_analysis = self.gap_service.analyze(
            paper_ids=case.paper_ids,
            query=case.query,
            evidence_per_paper=evidence_per_paper,
        )

        review = self.review_service.generate(
            query=case.query,
            paper_ids=case.paper_ids,
            title=case.title,
            evidence_per_paper=evidence_per_paper,
        )

        answer_generated = bool(answer.answer_text.strip())

        answer_validation_valid = answer.validation.is_valid

        comparison_generated = bool(comparison.profiles or comparison.matrix)

        comparison_papers = {profile.paper_id for profile in comparison.profiles}

        comparison_paper_coverage = (
            len(requested_set & comparison_papers) / len(requested_set)
            if requested_set
            else 0.0
        )

        invalid_comparison_paper_references = set()

        for finding in comparison.findings:

            for paper_id in finding.paper_ids:

                if paper_id not in requested_set:

                    invalid_comparison_paper_references.add(paper_id)

        gap_analysis_generated = bool(
            gap_analysis.paper_signals or gap_analysis.candidates
        )

        gap_papers = {
            paper_signals.paper_id for paper_signals in gap_analysis.paper_signals
        }

        gap_paper_coverage = (
            len(requested_set & gap_papers) / len(requested_set)
            if requested_set
            else 0.0
        )

        gap_validation_valid = (
            gap_analysis.validation.is_valid
            if gap_analysis.validation is not None
            else False
        )

        invalid_gap_paper_references = set()

        for candidate in gap_analysis.candidates:

            for paper_id in candidate.paper_ids:

                if paper_id not in requested_set:

                    invalid_gap_paper_references.add(paper_id)

        literature_review_generated = bool(review.sections)

        review_papers = set(review.paper_ids)

        literature_review_paper_coverage = (
            len(requested_set & review_papers) / len(requested_set)
            if requested_set
            else 0.0
        )

        literature_review_validation_valid = (
            review.validation.valid if review.validation is not None else False
        )

        invalid_review_paper_references = set()

        for section in review.sections:

            for finding in section.findings:

                for paper_id in finding.paper_ids:

                    if paper_id not in requested_set:

                        invalid_review_paper_references.add(paper_id)

        gap_signal_count = sum(
            len(paper_signals.signals) for paper_signals in gap_analysis.paper_signals
        )

        literature_review_finding_count = sum(
            len(section.findings) for section in review.sections
        )

        answer_evidence_ids = {evidence.evidence_id for evidence in answer.evidence}

        comparison_evidence_ids = set()

        for profile in comparison.profiles:

            for dimension in profile.dimensions:

                for evidence in dimension.evidence:

                    comparison_evidence_ids.add(evidence.evidence_id)

        gap_evidence_ids = set()

        for paper_signals in gap_analysis.paper_signals:

            for signal in paper_signals.signals:

                gap_evidence_ids.add(signal.evidence_id)

        review_evidence_ids = set()

        for section in review.sections:

            for evidence in section.evidence:

                review_evidence_ids.add(evidence.evidence_id)

        all_evidence_sets = [
            answer_evidence_ids,
            comparison_evidence_ids,
            gap_evidence_ids,
            review_evidence_ids,
        ]

        evidence_occurrence_count = {}

        for evidence_set in all_evidence_sets:

            for evidence_id in evidence_set:

                evidence_occurrence_count[evidence_id] = (
                    evidence_occurrence_count.get(
                        evidence_id,
                        0,
                    )
                    + 1
                )

        shared_evidence_id_count = sum(
            1 for count in evidence_occurrence_count.values() if count >= 2
        )

        stage_results = [
            (answer_generated and answer_validation_valid),
            (
                comparison_generated
                and comparison_paper_coverage == 1.0
                and not invalid_comparison_paper_references
            ),
            (
                gap_analysis_generated
                and gap_validation_valid
                and gap_paper_coverage == 1.0
                and not invalid_gap_paper_references
            ),
            (
                literature_review_generated
                and literature_review_validation_valid
                and literature_review_paper_coverage == 1.0
                and not invalid_review_paper_references
            ),
        ]

        stage_success_count = sum(stage_results)

        total_stage_count = len(stage_results)

        stage_success_rate = (
            stage_success_count / total_stage_count if total_stage_count else 0.0
        )

        structural_valid = stage_success_count == total_stage_count

        return EndToEndEvaluationResult(
            workflow_id=case.workflow_id,
            query=case.query,
            requested_papers=case.paper_ids,
            answer_generated=(answer_generated),
            answer_claim_count=len(answer.claims),
            answer_evidence_count=len(answer.evidence),
            answer_validation_valid=(answer_validation_valid),
            comparison_generated=(comparison_generated),
            comparison_profile_count=len(comparison.profiles),
            comparison_matrix_row_count=len(comparison.matrix),
            comparison_finding_count=len(comparison.findings),
            comparison_paper_coverage=(comparison_paper_coverage),
            gap_analysis_generated=(gap_analysis_generated),
            gap_signal_count=(gap_signal_count),
            gap_candidate_count=len(gap_analysis.candidates),
            gap_validation_valid=(gap_validation_valid),
            gap_paper_coverage=(gap_paper_coverage),
            literature_review_generated=(literature_review_generated),
            literature_review_section_count=len(review.sections),
            literature_review_finding_count=(literature_review_finding_count),
            literature_review_citation_count=len(review.citations),
            literature_review_validation_valid=(literature_review_validation_valid),
            literature_review_paper_coverage=(literature_review_paper_coverage),
            shared_evidence_id_count=(shared_evidence_id_count),
            invalid_comparison_paper_references=sorted(
                invalid_comparison_paper_references
            ),
            invalid_gap_paper_references=sorted(invalid_gap_paper_references),
            invalid_review_paper_references=sorted(invalid_review_paper_references),
            stage_success_count=(stage_success_count),
            total_stage_count=(total_stage_count),
            stage_success_rate=(stage_success_rate),
            structural_valid=(structural_valid),
        )
