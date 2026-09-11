from src.analysis.literature_review_models import (
    LiteratureReview,
    LiteratureReviewEvidence,
    LiteratureReviewFinding,
    LiteratureReviewSection,
    LiteratureReviewSectionType,
    LiteratureReviewValidationResult,
)
from src.evaluation.literature_review_evaluator import (
    LiteratureReviewEvaluator,
)
from src.evaluation.literature_review_metrics import (
    calculate_literature_review_metrics,
)
from src.evaluation.models import (
    LiteratureReviewBenchmarkCase,
)


class FakeLiteratureReviewService:

    def generate(
        self,
        query: str,
        paper_ids: list[str],
        title: str = ("Evidence-Grounded Literature Review"),
        evidence_per_paper: int = 8,
    ) -> LiteratureReview:

        sections = []

        for index, section_type in enumerate(
            LiteratureReviewSectionType,
            start=1,
        ):

            evidence_id = f"E{index}"

            evidence = LiteratureReviewEvidence(
                evidence_id=evidence_id,
                paper_id="03_mutap",
                page_number=index,
                section="Method",
                text=("Evidence supporting " "the review finding."),
                citation_text=(f"03_mutap, page {index}"),
            )

            finding = LiteratureReviewFinding(
                finding_id=f"F{index}",
                section_type=section_type,
                statement=("Evidence-backed review finding."),
                paper_ids=["03_mutap"],
                evidence_ids=[evidence_id],
            )

            sections.append(
                LiteratureReviewSection(
                    section_type=section_type,
                    title=section_type.value,
                    objective="Evaluate evidence.",
                    findings=[finding],
                    evidence=[evidence],
                    narrative=("Evidence-backed narrative."),
                )
            )

        validation = LiteratureReviewValidationResult(
            valid=True,
            issues=[],
        )

        return LiteratureReview(
            query=query,
            paper_ids=paper_ids,
            title=title,
            sections=sections,
            citations=["03_mutap"],
            validation=validation,
        )


def test_literature_review_evaluator_valid_case():

    case = LiteratureReviewBenchmarkCase(
        review_id="LR1",
        title="Test Review",
        query="review test generation",
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    evaluator = LiteratureReviewEvaluator(
        review_service=(FakeLiteratureReviewService())
    )

    result = evaluator.evaluate_case(case)

    assert result.review_paper_coverage == 1.0

    assert result.section_count == 8

    assert result.section_structure_complete is True

    assert result.finding_count == 8

    assert result.finding_evidence_coverage == 1.0

    assert result.finding_evidence_reference_integrity == 1.0

    assert result.provenance_completeness == 1.0

    assert result.backend_validation_valid is True

    assert result.corpus_scope_note_present is True

    assert result.structural_valid is True


def test_literature_review_metrics():

    case = LiteratureReviewBenchmarkCase(
        review_id="LR1",
        title="Test Review",
        query="review test generation",
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    result = LiteratureReviewEvaluator(
        review_service=(FakeLiteratureReviewService())
    ).evaluate_case(case)

    metrics = calculate_literature_review_metrics(
        [
            result,
        ]
    )

    assert metrics.case_count == 1

    assert metrics.structural_pass_rate == 1.0

    assert metrics.backend_validation_pass_rate == 1.0

    assert metrics.mean_review_paper_coverage == 1.0

    assert metrics.section_structure_pass_rate == 1.0

    assert metrics.mean_finding_evidence_coverage == 1.0

    assert metrics.finding_evidence_reference_integrity == 1.0

    assert metrics.mean_provenance_completeness == 1.0

    assert metrics.corpus_scope_note_pass_rate == 1.0
