from src.evaluation.grounding_evaluator import (
    GroundingEvaluator,
)

from src.evaluation.grounding_metrics import (
    calculate_grounding_metrics,
)

from src.evaluation.models import (
    GroundingBenchmarkCase,
)

from src.generation.models import (
    GeneratedClaim,
    GroundedAnswer,
    GroundingEvidence,
    GroundingValidationResult,
)


class FakeAnswerService:

    def answer_search(
        self,
        query: str,
        top_k: int = 5,
    ) -> GroundedAnswer:

        evidence = [
            GroundingEvidence(
                evidence_id="E1",
                label="Evidence 1",
                paper_id="03_mutap",
                page_number=5,
                section="Method",
                text="Mutation feedback improves generated tests.",
                citation_text="03_mutap, page 5",
            )
        ]

        claims = [
            GeneratedClaim(
                claim_id="C1",
                text=(
                    "Mutation feedback can improve "
                    "generated tests."
                ),
                evidence_ids=[
                    "E1",
                ],
            )
        ]

        validation = GroundingValidationResult(
            is_valid=True,
            validated_claim_count=1,
            issue_count=0,
            issues=[],
        )

        return GroundedAnswer(
            query=query,
            answer_text=(
                "Mutation feedback can improve "
                "generated tests."
            ),
            claims=claims,
            evidence=evidence,
            validation=validation,
        )


def test_grounding_evaluator_valid_case():

    case = GroundingBenchmarkCase(
        question_id="G1",
        query="mutation testing",
        expected_papers=[
            "03_mutap",
        ],
    )

    evaluator = GroundingEvaluator(
        answer_service=FakeAnswerService()
    )

    result = evaluator.evaluate_case(
        case
    )

    assert result.claim_count == 1
    assert result.evidence_count == 1

    assert (
        result.claim_evidence_coverage
        == 1.0
    )

    assert (
        result.provenance_completeness
        == 1.0
    )

    assert (
        result.backend_validation_valid
        is True
    )

    assert (
        result.missing_evidence_references
        == []
    )

    assert (
        result.expected_paper_recall
        == 1.0
    )


def test_grounding_metrics():

    case = GroundingBenchmarkCase(
        question_id="G1",
        query="mutation testing",
        expected_papers=[
            "03_mutap",
        ],
    )

    result = GroundingEvaluator(
        answer_service=FakeAnswerService()
    ).evaluate_case(
        case
    )

    metrics = calculate_grounding_metrics(
        [
            result,
        ]
    )

    assert metrics.case_count == 1

    assert (
        metrics.backend_validation_pass_rate
        == 1.0
    )

    assert (
        metrics.mean_claim_evidence_coverage
        == 1.0
    )

    assert (
        metrics.mean_provenance_completeness
        == 1.0
    )

    assert (
        metrics.evidence_reference_integrity
        == 1.0
    )

    assert (
        metrics.mean_expected_paper_recall
        == 1.0
    )