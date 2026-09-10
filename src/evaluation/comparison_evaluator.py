from src.analysis.comparative_service import (
    ComparativeAnalysisService,
)

from src.evaluation.models import (
    ComparisonBenchmarkCase,
    ComparisonEvaluationResult,
)


class ComparisonEvaluator:

    def __init__(
        self,
        comparison_service: ComparativeAnalysisService | None = None,
    ) -> None:

        self.comparison_service = (
            comparison_service
            if comparison_service is not None
            else ComparativeAnalysisService()
        )

    def evaluate_case(
        self,
        case: ComparisonBenchmarkCase,
        evidence_per_paper: int = 6,
    ) -> ComparisonEvaluationResult:

        analysis = self.comparison_service.analyze(
            paper_ids=case.paper_ids,
            query=case.query,
            evidence_per_paper=evidence_per_paper,
        )

        requested_set = set(
            case.paper_ids
        )

        profile_papers = self._unique_in_order(
            [
                profile.paper_id
                for profile in analysis.profiles
            ]
        )

        matrix_papers = self._matrix_papers(
            analysis
        )

        missing_profile_papers = [
            paper_id
            for paper_id in case.paper_ids
            if paper_id not in profile_papers
        ]

        missing_matrix_papers = [
            paper_id
            for paper_id in case.paper_ids
            if paper_id not in matrix_papers
        ]

        profile_paper_coverage = (
            len(
                requested_set
                & set(profile_papers)
            )
            / len(requested_set)
            if requested_set
            else 0.0
        )

        matrix_paper_coverage = (
            len(
                requested_set
                & set(matrix_papers)
            )
            / len(requested_set)
            if requested_set
            else 0.0
        )

        profile_evidence_ids = (
            self._profile_evidence_ids(
                analysis
            )
        )

        profile_evidence_set = set(
            profile_evidence_ids
        )

        matrix_cell_count = 0
        populated_cell_count = 0

        cell_evidence_reference_count = 0
        missing_cell_evidence_references = set()

        for row in analysis.matrix:

            for cell in row.cells:

                matrix_cell_count += 1

                if (
                    cell.summary
                    or cell.evidence_ids
                ):

                    populated_cell_count += 1

                for evidence_id in cell.evidence_ids:

                    cell_evidence_reference_count += 1

                    if (
                        evidence_id
                        not in profile_evidence_set
                    ):

                        missing_cell_evidence_references.add(
                            evidence_id
                        )

        empty_cell_count = (
            matrix_cell_count
            - populated_cell_count
        )

        matrix_population_rate = (
            populated_cell_count
            / matrix_cell_count
            if matrix_cell_count
            else 0.0
        )

        finding_evidence_reference_count = 0
        missing_finding_evidence_references = set()

        invalid_finding_paper_references = set()

        for finding in analysis.findings:

            for evidence_id in finding.evidence_ids:

                finding_evidence_reference_count += 1

                if (
                    evidence_id
                    not in profile_evidence_set
                ):

                    missing_finding_evidence_references.add(
                        evidence_id
                    )

            for paper_id in finding.paper_ids:

                if paper_id not in requested_set:

                    invalid_finding_paper_references.add(
                        paper_id
                    )

        cell_evidence_reference_integrity = (
            self._reference_integrity(
                total_references=(
                    cell_evidence_reference_count
                ),
                missing_reference_count=len(
                    missing_cell_evidence_references
                ),
            )
        )

        finding_evidence_reference_integrity = (
            self._reference_integrity(
                total_references=(
                    finding_evidence_reference_count
                ),
                missing_reference_count=len(
                    missing_finding_evidence_references
                ),
            )
        )

        structural_valid = (
            not missing_profile_papers
            and not missing_matrix_papers
            and not missing_cell_evidence_references
            and not missing_finding_evidence_references
            and not invalid_finding_paper_references
        )

        return ComparisonEvaluationResult(
            comparison_id=case.comparison_id,
            query=case.query,

            requested_papers=case.paper_ids,
            profile_papers=profile_papers,
            matrix_papers=matrix_papers,

            missing_profile_papers=(
                missing_profile_papers
            ),

            missing_matrix_papers=(
                missing_matrix_papers
            ),

            profile_paper_coverage=(
                profile_paper_coverage
            ),

            matrix_paper_coverage=(
                matrix_paper_coverage
            ),

            dimension_count=len(
                analysis.matrix
            ),

            matrix_cell_count=(
                matrix_cell_count
            ),

            populated_cell_count=(
                populated_cell_count
            ),

            empty_cell_count=(
                empty_cell_count
            ),

            matrix_population_rate=(
                matrix_population_rate
            ),

            profile_evidence_count=len(
                profile_evidence_ids
            ),

            profile_evidence_ids=(
                profile_evidence_ids
            ),

            populated_cell_evidence_reference_count=(
                cell_evidence_reference_count
            ),

            missing_cell_evidence_references=sorted(
                missing_cell_evidence_references
            ),

            cell_evidence_reference_integrity=(
                cell_evidence_reference_integrity
            ),

            finding_count=len(
                analysis.findings
            ),

            finding_evidence_reference_count=(
                finding_evidence_reference_count
            ),

            missing_finding_evidence_references=sorted(
                missing_finding_evidence_references
            ),

            finding_evidence_reference_integrity=(
                finding_evidence_reference_integrity
            ),

            invalid_finding_paper_references=sorted(
                invalid_finding_paper_references
            ),

            structural_valid=(
                structural_valid
            ),
        )

    def _profile_evidence_ids(
        self,
        analysis,
    ) -> list[str]:

        evidence_ids = []

        for profile in analysis.profiles:

            for dimension in profile.dimensions:

                for evidence in dimension.evidence:

                    evidence_ids.append(
                        evidence.evidence_id
                    )

        return self._unique_in_order(
            evidence_ids
        )

    def _matrix_papers(
        self,
        analysis,
    ) -> list[str]:

        paper_ids = []

        for row in analysis.matrix:

            for cell in row.cells:

                paper_ids.append(
                    cell.paper_id
                )

        return self._unique_in_order(
            paper_ids
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