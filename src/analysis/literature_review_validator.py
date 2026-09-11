from __future__ import annotations

from src.analysis.literature_review_models import (
    LiteratureReviewEvidenceAggregation,
    LiteratureReviewSynthesis,
    LiteratureReviewValidationIssue,
    LiteratureReviewValidationIssueCode,
    LiteratureReviewValidationResult,
)


class LiteratureReviewGroundingValidator:
    """
    Validate structural grounding for literature-review synthesis.

    This validator confirms provenance consistency.
    It does not determine semantic entailment.
    """

    def validate(
        self,
        aggregation: LiteratureReviewEvidenceAggregation,
        synthesis: LiteratureReviewSynthesis,
    ) -> LiteratureReviewValidationResult:

        issues: list[LiteratureReviewValidationIssue] = []

        evidence_by_id = self._build_evidence_index(aggregation)

        requested_papers = set(aggregation.paper_ids)

        seen_finding_ids: set[str] = set()

        for finding in synthesis.findings:

            if finding.finding_id in seen_finding_ids:
                issues.append(
                    LiteratureReviewValidationIssue(
                        code=(LiteratureReviewValidationIssueCode.DUPLICATE_FINDING_ID),
                        message=("Duplicate finding ID: " f"{finding.finding_id}"),
                        section_type=finding.section_type,
                        finding_id=finding.finding_id,
                    )
                )

            seen_finding_ids.add(finding.finding_id)

            if not finding.statement.strip():
                issues.append(
                    LiteratureReviewValidationIssue(
                        code=(
                            LiteratureReviewValidationIssueCode.EMPTY_FINDING_STATEMENT
                        ),
                        message=("Finding statement must not be empty."),
                        section_type=finding.section_type,
                        finding_id=finding.finding_id,
                    )
                )

            if not finding.evidence_ids:
                issues.append(
                    LiteratureReviewValidationIssue(
                        code=(
                            LiteratureReviewValidationIssueCode.FINDING_WITHOUT_EVIDENCE
                        ),
                        message=("Finding has no supporting evidence."),
                        section_type=finding.section_type,
                        finding_id=finding.finding_id,
                    )
                )

                continue

            supporting_papers: list[str] = []
            supporting_seen: set[str] = set()

            for evidence_id in finding.evidence_ids:

                evidence = evidence_by_id.get(evidence_id)

                if evidence is None:
                    issues.append(
                        LiteratureReviewValidationIssue(
                            code=(
                                LiteratureReviewValidationIssueCode.UNKNOWN_EVIDENCE_ID
                            ),
                            message=("Unknown evidence ID: " f"{evidence_id}"),
                            section_type=finding.section_type,
                            finding_id=finding.finding_id,
                        )
                    )

                    continue

                if evidence.paper_id not in requested_papers:
                    issues.append(
                        LiteratureReviewValidationIssue(
                            code=(
                                LiteratureReviewValidationIssueCode.EVIDENCE_OUTSIDE_CORPUS
                            ),
                            message=(
                                "Evidence "
                                f"{evidence_id} belongs to "
                                f"{evidence.paper_id}, which is "
                                "outside the requested corpus."
                            ),
                            section_type=finding.section_type,
                            finding_id=finding.finding_id,
                        )
                    )

                if evidence.paper_id not in supporting_seen:
                    supporting_seen.add(evidence.paper_id)

                    supporting_papers.append(evidence.paper_id)

            claimed_papers = self._unique_nonempty(finding.paper_ids)

            if set(claimed_papers) != set(supporting_papers):
                issues.append(
                    LiteratureReviewValidationIssue(
                        code=(
                            LiteratureReviewValidationIssueCode.PAPER_SUPPORT_MISMATCH
                        ),
                        message=(
                            "Finding paper_ids do not match "
                            "the papers represented by its "
                            "supporting evidence."
                        ),
                        section_type=finding.section_type,
                        finding_id=finding.finding_id,
                    )
                )

            actual_support_count = len(supporting_papers)

            if finding.support_count != actual_support_count:
                issues.append(
                    LiteratureReviewValidationIssue(
                        code=(
                            LiteratureReviewValidationIssueCode.SUPPORT_COUNT_MISMATCH
                        ),
                        message=(
                            "Finding support_count does not "
                            "match the number of unique "
                            "supporting papers."
                        ),
                        section_type=finding.section_type,
                        finding_id=finding.finding_id,
                    )
                )

            if finding.is_cross_paper and actual_support_count < 2:
                issues.append(
                    LiteratureReviewValidationIssue(
                        code=(
                            LiteratureReviewValidationIssueCode.CROSS_PAPER_SUPPORT_TOO_LOW
                        ),
                        message=(
                            "Cross-paper finding requires "
                            "support from at least two "
                            "distinct papers."
                        ),
                        section_type=finding.section_type,
                        finding_id=finding.finding_id,
                    )
                )

            if not finding.is_cross_paper and actual_support_count > 1:
                issues.append(
                    LiteratureReviewValidationIssue(
                        code=(
                            LiteratureReviewValidationIssueCode.SINGLE_PAPER_FLAG_MISMATCH
                        ),
                        message=(
                            "Finding is marked as single-paper "
                            "but is supported by multiple papers."
                        ),
                        section_type=finding.section_type,
                        finding_id=finding.finding_id,
                    )
                )

        return LiteratureReviewValidationResult(
            valid=not issues,
            issues=issues,
        )

    def _build_evidence_index(
        self,
        aggregation: LiteratureReviewEvidenceAggregation,
    ) -> dict[str, object]:

        evidence_by_id = {}

        for bundle in aggregation.bundles:

            for evidence in bundle.evidence:

                if evidence.evidence_id not in evidence_by_id:
                    evidence_by_id[evidence.evidence_id] = evidence

        return evidence_by_id

    def _unique_nonempty(
        self,
        values: list[str],
    ) -> list[str]:

        cleaned = []
        seen = set()

        for value in values:

            normalized = value.strip()

            if not normalized:
                continue

            if normalized in seen:
                continue

            seen.add(normalized)

            cleaned.append(normalized)

        return cleaned
