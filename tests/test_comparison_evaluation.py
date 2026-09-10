from src.analysis.comparison_models import (
    ComparativeAnalysis,
    ComparativeFinding,
    ComparisonCell,
    ComparisonRow,
    DimensionEvidence,
    PaperAnalysisProfile,
    PaperDimensionAnalysis,
)

from src.evaluation.comparison_evaluator import (
    ComparisonEvaluator,
)

from src.evaluation.comparison_metrics import (
    calculate_comparison_metrics,
)

from src.evaluation.models import (
    ComparisonBenchmarkCase,
)


class FakeComparisonService:

    def analyze(
        self,
        paper_ids: list[str],
        query: str,
        evidence_per_paper: int = 6,
    ) -> ComparativeAnalysis:

        evidence_one = DimensionEvidence(
            evidence_id="E1",
            paper_id="03_mutap",
            dimension="feedback_signal",
            page_number=5,
            section="Method",
            text="Mutation feedback is used.",
            citation_text="03_mutap, page 5",
            relevance_score=1.0,
        )

        evidence_two = DimensionEvidence(
            evidence_id="E2",
            paper_id="05_coverup",
            dimension="feedback_signal",
            page_number=4,
            section="Method",
            text="Coverage feedback is used.",
            citation_text="05_coverup, page 4",
            relevance_score=1.0,
        )

        profiles = [
            PaperAnalysisProfile(
                paper_id="03_mutap",
                dimensions=[
                    PaperDimensionAnalysis(
                        dimension="feedback_signal",
                        evidence=[
                            evidence_one
                        ],
                    )
                ],
            ),
            PaperAnalysisProfile(
                paper_id="05_coverup",
                dimensions=[
                    PaperDimensionAnalysis(
                        dimension="feedback_signal",
                        evidence=[
                            evidence_two
                        ],
                    )
                ],
            ),
        ]

        matrix = [
            ComparisonRow(
                dimension="feedback_signal",
                cells=[
                    ComparisonCell(
                        paper_id="03_mutap",
                        dimension="feedback_signal",
                        summary="Mutation feedback.",
                        evidence_ids=[
                            "E1"
                        ],
                    ),
                    ComparisonCell(
                        paper_id="05_coverup",
                        dimension="feedback_signal",
                        summary="Coverage feedback.",
                        evidence_ids=[
                            "E2"
                        ],
                    ),
                ],
            )
        ]

        findings = [
            ComparativeFinding(
                finding_id="F1",
                finding_type="shared_dimension",
                text=(
                    "Both papers contain "
                    "feedback-related evidence."
                ),
                paper_ids=[
                    "03_mutap",
                    "05_coverup",
                ],
                evidence_ids=[
                    "E1",
                    "E2",
                ],
            )
        ]

        return ComparativeAnalysis(
            query=query,
            requested_papers=paper_ids,
            profiles=profiles,
            matrix=matrix,
            findings=findings,
        )


def test_comparison_evaluator_valid_case():

    case = ComparisonBenchmarkCase(
        comparison_id="C1",
        query="compare feedback",
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    evaluator = ComparisonEvaluator(
        comparison_service=(
            FakeComparisonService()
        )
    )

    result = evaluator.evaluate_case(
        case
    )

    assert (
        result.profile_paper_coverage
        == 1.0
    )

    assert (
        result.matrix_paper_coverage
        == 1.0
    )

    assert (
        result.matrix_population_rate
        == 1.0
    )

    assert (
        result.cell_evidence_reference_integrity
        == 1.0
    )

    assert (
        result.finding_evidence_reference_integrity
        == 1.0
    )

    assert (
        result.missing_profile_papers
        == []
    )

    assert (
        result.missing_matrix_papers
        == []
    )

    assert (
        result.invalid_finding_paper_references
        == []
    )

    assert result.structural_valid is True


def test_comparison_metrics():

    case = ComparisonBenchmarkCase(
        comparison_id="C1",
        query="compare feedback",
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    result = ComparisonEvaluator(
        comparison_service=(
            FakeComparisonService()
        )
    ).evaluate_case(
        case
    )

    metrics = calculate_comparison_metrics(
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
        metrics.mean_profile_paper_coverage
        == 1.0
    )

    assert (
        metrics.mean_matrix_paper_coverage
        == 1.0
    )

    assert (
        metrics.mean_matrix_population_rate
        == 1.0
    )

    assert (
        metrics.cell_evidence_reference_integrity
        == 1.0
    )

    assert (
        metrics.finding_evidence_reference_integrity
        == 1.0
    )