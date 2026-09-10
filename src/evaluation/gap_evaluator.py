from src.analysis.gap_analysis_service import (
    ResearchGapAnalysisService,
)

from src.analysis.gap_models import (
    GapType,
)

from src.evaluation.models import (
    GapBenchmarkCase,
    GapEvaluationResult,
)


class GapEvaluator:

    def __init__(
        self,
        gap_service: ResearchGapAnalysisService | None = None,
    ) -> None:

        self.gap_service = (
            gap_service
            if gap_service is not None
            else ResearchGapAnalysisService()
        )

    def evaluate_case(
        self,
        case: GapBenchmarkCase,
        evidence_per_paper: int = 8,
    ) -> GapEvaluationResult:

        analysis = self.gap_service.analyze(
            paper_ids=case.paper_ids,
            query=case.query,
            evidence_per_paper=evidence_per_paper,
        )

        requested_set = set(
            case.paper_ids
        )

        signal_papers = self._unique_in_order(
            [
                paper_signals.paper_id
                for paper_signals
                in analysis.paper_signals
            ]
        )

        missing_signal_papers = [
            paper_id
            for paper_id in case.paper_ids
            if paper_id not in signal_papers
        ]

        signal_paper_coverage = (
            len(
                requested_set
                & set(signal_papers)
            )
            / len(requested_set)
            if requested_set
            else 0.0
        )

        signal_evidence_ids = set()

        signal_count = 0

        for paper_signals in analysis.paper_signals:

            for signal in paper_signals.signals:

                signal_count += 1

                signal_evidence_ids.add(
                    signal.evidence_id
                )

        candidate_evidence_reference_count = 0

        missing_candidate_evidence_references = set()

        invalid_candidate_paper_references = set()

        explicit_candidate_count = 0
        corpus_imbalance_candidate_count = 0
        insufficient_evidence_candidate_count = 0

        for candidate in analysis.candidates:

            if candidate.gap_type == GapType.EXPLICIT:

                explicit_candidate_count += 1

            elif (
                candidate.gap_type
                == GapType.CORPUS_IMBALANCE
            ):

                corpus_imbalance_candidate_count += 1

            elif (
                candidate.gap_type
                == GapType.INSUFFICIENT_EVIDENCE
            ):

                insufficient_evidence_candidate_count += 1

            for evidence_id in candidate.evidence_ids:

                candidate_evidence_reference_count += 1

                if (
                    evidence_id
                    not in signal_evidence_ids
                ):

                    missing_candidate_evidence_references.add(
                        evidence_id
                    )

            for paper_id in candidate.paper_ids:

                if paper_id not in requested_set:

                    invalid_candidate_paper_references.add(
                        paper_id
                    )

        candidate_evidence_reference_integrity = (
            self._reference_integrity(
                total_references=(
                    candidate_evidence_reference_count
                ),
                missing_reference_count=len(
                    missing_candidate_evidence_references
                ),
            )
        )

        dimension_coverage_count = len(
            analysis.dimension_coverage
        )

        populated_dimension_count = sum(
            1
            for coverage
            in analysis.dimension_coverage
            if coverage.evidence_count > 0
        )

        dimension_population_rate = (
            populated_dimension_count
            / dimension_coverage_count
            if dimension_coverage_count
            else 0.0
        )

        backend_validation_valid = (
            analysis.validation.is_valid
            if analysis.validation is not None
            else False
        )

        backend_validation_issue_count = (
            analysis.validation.issue_count
            if analysis.validation is not None
            else 0
        )

        structural_valid = (
            not missing_signal_papers
            and not missing_candidate_evidence_references
            and not invalid_candidate_paper_references
            and backend_validation_valid
        )

        return GapEvaluationResult(
            gap_id=case.gap_id,
            query=case.query,

            requested_papers=case.paper_ids,

            signal_papers=signal_papers,

            missing_signal_papers=(
                missing_signal_papers
            ),

            signal_paper_coverage=(
                signal_paper_coverage
            ),

            signal_count=signal_count,

            candidate_count=len(
                analysis.candidates
            ),

            explicit_candidate_count=(
                explicit_candidate_count
            ),

            corpus_imbalance_candidate_count=(
                corpus_imbalance_candidate_count
            ),

            insufficient_evidence_candidate_count=(
                insufficient_evidence_candidate_count
            ),

            candidate_evidence_reference_count=(
                candidate_evidence_reference_count
            ),

            missing_candidate_evidence_references=sorted(
                missing_candidate_evidence_references
            ),

            candidate_evidence_reference_integrity=(
                candidate_evidence_reference_integrity
            ),

            invalid_candidate_paper_references=sorted(
                invalid_candidate_paper_references
            ),

            dimension_coverage_count=(
                dimension_coverage_count
            ),

            populated_dimension_count=(
                populated_dimension_count
            ),

            dimension_population_rate=(
                dimension_population_rate
            ),

            backend_validation_valid=(
                backend_validation_valid
            ),

            backend_validation_issue_count=(
                backend_validation_issue_count
            ),

            structural_valid=(
                structural_valid
            ),
        )

    def _reference_integrity(
        self,
        total_references: int,
        missing_reference_count: int,
    ) -> float:

        if total_references == 0:

            return 1.0

        return (
            total_references
            - missing_reference_count
        ) / total_references

    def _unique_in_order(
        self,
        values: list[str],
    ) -> list[str]:

        seen = set()
        unique = []

        for value in values:

            if value not in seen:

                unique.append(
                    value
                )

                seen.add(
                    value
                )

        return unique