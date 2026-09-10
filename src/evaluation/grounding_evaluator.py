from src.evaluation.models import (
    GroundingBenchmarkCase,
    GroundingEvaluationResult,
)

from src.generation.answer_service import (
    GroundedAnswerService,
)


class GroundingEvaluator:

    def __init__(
        self,
        answer_service: GroundedAnswerService | None = None,
    ) -> None:

        self.answer_service = (
            answer_service
            if answer_service is not None
            else GroundedAnswerService()
        )

    def evaluate_case(
        self,
        case: GroundingBenchmarkCase,
        top_k: int = 8,
    ) -> GroundingEvaluationResult:

        answer = self.answer_service.answer_search(
            query=case.query,
            top_k=top_k,
        )

        evidence_by_id = {
            evidence.evidence_id: evidence
            for evidence in answer.evidence
        }

        claims_with_evidence = 0
        claims_without_evidence = 0

        referenced_evidence_ids = set()
        missing_evidence_references = set()

        for claim in answer.claims:

            if claim.evidence_ids:

                claims_with_evidence += 1

            else:

                claims_without_evidence += 1

            for evidence_id in claim.evidence_ids:

                referenced_evidence_ids.add(
                    evidence_id
                )

                if evidence_id not in evidence_by_id:

                    missing_evidence_references.add(
                        evidence_id
                    )

        complete_provenance = 0
        incomplete_provenance = 0

        for evidence in answer.evidence:

            if self._has_complete_provenance(
                evidence
            ):

                complete_provenance += 1

            else:

                incomplete_provenance += 1

        evidence_papers = self._unique_in_order(
            [
                evidence.paper_id
                for evidence in answer.evidence
            ]
        )

        expected = set(
            case.expected_papers
        )

        matched_expected_papers = [
            paper_id
            for paper_id in evidence_papers
            if paper_id in expected
        ]

        claim_count = len(
            answer.claims
        )

        evidence_count = len(
            answer.evidence
        )

        claim_evidence_coverage = (
            claims_with_evidence / claim_count
            if claim_count
            else 0.0
        )

        provenance_completeness = (
            complete_provenance / evidence_count
            if evidence_count
            else 0.0
        )

        expected_paper_recall = (
            len(
                set(
                    matched_expected_papers
                )
            )
            / len(expected)
            if expected
            else 0.0
        )

        return GroundingEvaluationResult(
            question_id=case.question_id,
            query=case.query,

            claim_count=claim_count,
            evidence_count=evidence_count,

            claims_with_evidence=(
                claims_with_evidence
            ),

            claims_without_evidence=(
                claims_without_evidence
            ),

            referenced_evidence_count=len(
                referenced_evidence_ids
            ),

            missing_evidence_references=sorted(
                missing_evidence_references
            ),

            evidence_with_complete_provenance=(
                complete_provenance
            ),

            evidence_with_incomplete_provenance=(
                incomplete_provenance
            ),

            backend_validation_valid=(
                answer.validation.is_valid
            ),

            backend_validation_issue_count=(
                answer.validation.issue_count
            ),

            evidence_papers=evidence_papers,
            expected_papers=(
                case.expected_papers
            ),

            matched_expected_papers=(
                matched_expected_papers
            ),

            claim_evidence_coverage=(
                claim_evidence_coverage
            ),

            provenance_completeness=(
                provenance_completeness
            ),

            expected_paper_recall=(
                expected_paper_recall
            ),
        )

    def _has_complete_provenance(
        self,
        evidence,
    ) -> bool:

        return bool(
            evidence.evidence_id
            and evidence.paper_id
            and evidence.page_number is not None
            and evidence.text.strip()
            and evidence.citation_text.strip()
        )

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