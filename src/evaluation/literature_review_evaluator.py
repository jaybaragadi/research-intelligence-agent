from collections import Counter

from src.analysis.literature_review_models import (
    LiteratureReviewSectionType,
)
from src.analysis.literature_review_service import (
    LiteratureReviewService,
)
from src.evaluation.models import (
    LiteratureReviewBenchmarkCase,
    LiteratureReviewEvaluationResult,
)


class LiteratureReviewEvaluator:

    def __init__(
        self,
        review_service: LiteratureReviewService | None = None,
    ) -> None:

        self.review_service = (
            review_service if review_service is not None else LiteratureReviewService()
        )

    def evaluate_case(
        self,
        case: LiteratureReviewBenchmarkCase,
        evidence_per_paper: int = 8,
    ) -> LiteratureReviewEvaluationResult:

        review = self.review_service.generate(
            query=case.query,
            paper_ids=case.paper_ids,
            title=case.title,
            evidence_per_paper=evidence_per_paper,
        )

        requested_set = set(case.paper_ids)

        review_papers = self._unique_in_order(review.paper_ids)

        missing_review_papers = [
            paper_id for paper_id in case.paper_ids if paper_id not in review_papers
        ]

        invalid_review_papers = [
            paper_id for paper_id in review_papers if paper_id not in requested_set
        ]

        review_paper_coverage = (
            len(requested_set & set(review_papers)) / len(requested_set)
            if requested_set
            else 0.0
        )

        expected_section_types = [
            section_type.value for section_type in LiteratureReviewSectionType
        ]

        actual_section_types = [
            section.section_type.value for section in review.sections
        ]

        section_counts = Counter(actual_section_types)

        missing_section_types = [
            section_type
            for section_type in expected_section_types
            if section_type not in section_counts
        ]

        duplicate_section_types = [
            section_type for section_type, count in section_counts.items() if count > 1
        ]

        section_structure_complete = (
            not missing_section_types
            and not duplicate_section_types
            and len(review.sections) == len(expected_section_types)
        )

        evidence_by_id = {}

        for section in review.sections:

            for evidence in section.evidence:

                evidence_by_id[evidence.evidence_id] = evidence

        finding_count = 0
        findings_with_evidence = 0
        findings_without_evidence = 0

        finding_evidence_reference_count = 0

        missing_finding_evidence_references = set()

        invalid_finding_paper_references = set()

        for section in review.sections:

            for finding in section.findings:

                finding_count += 1

                if finding.evidence_ids:

                    findings_with_evidence += 1

                else:

                    findings_without_evidence += 1

                for evidence_id in finding.evidence_ids:

                    finding_evidence_reference_count += 1

                    if evidence_id not in evidence_by_id:

                        missing_finding_evidence_references.add(evidence_id)

                for paper_id in finding.paper_ids:

                    if paper_id not in requested_set:

                        invalid_finding_paper_references.add(paper_id)

        finding_evidence_coverage = (
            findings_with_evidence / finding_count if finding_count else 1.0
        )

        evidence_items = list(evidence_by_id.values())

        evidence_with_complete_provenance = sum(
            1 for evidence in evidence_items if self._has_complete_provenance(evidence)
        )

        evidence_with_incomplete_provenance = (
            len(evidence_items) - evidence_with_complete_provenance
        )

        provenance_completeness = (
            evidence_with_complete_provenance / len(evidence_items)
            if evidence_items
            else 1.0
        )

        finding_evidence_reference_integrity = self._reference_integrity(
            total_references=(finding_evidence_reference_count),
            missing_reference_count=len(missing_finding_evidence_references),
        )

        backend_validation_valid = (
            review.validation.valid if review.validation is not None else False
        )

        backend_validation_issue_count = (
            len(review.validation.issues) if review.validation is not None else 0
        )

        corpus_scope_note_present = bool(
            review.corpus_scope_note and review.corpus_scope_note.strip()
        )

        structural_valid = (
            not missing_review_papers
            and not invalid_review_papers
            and section_structure_complete
            and not missing_finding_evidence_references
            and not invalid_finding_paper_references
            and evidence_with_incomplete_provenance == 0
            and backend_validation_valid
            and corpus_scope_note_present
        )

        return LiteratureReviewEvaluationResult(
            review_id=case.review_id,
            title=review.title,
            query=case.query,
            requested_papers=case.paper_ids,
            review_papers=review_papers,
            missing_review_papers=(missing_review_papers),
            invalid_review_papers=(invalid_review_papers),
            review_paper_coverage=(review_paper_coverage),
            section_count=len(review.sections),
            expected_section_count=len(expected_section_types),
            section_structure_complete=(section_structure_complete),
            missing_section_types=(missing_section_types),
            duplicate_section_types=(duplicate_section_types),
            finding_count=finding_count,
            findings_with_evidence=(findings_with_evidence),
            findings_without_evidence=(findings_without_evidence),
            finding_evidence_coverage=(finding_evidence_coverage),
            evidence_count=sum(len(section.evidence) for section in review.sections),
            unique_evidence_count=len(evidence_items),
            finding_evidence_reference_count=(finding_evidence_reference_count),
            missing_finding_evidence_references=sorted(
                missing_finding_evidence_references
            ),
            finding_evidence_reference_integrity=(finding_evidence_reference_integrity),
            invalid_finding_paper_references=sorted(invalid_finding_paper_references),
            evidence_with_complete_provenance=(evidence_with_complete_provenance),
            evidence_with_incomplete_provenance=(evidence_with_incomplete_provenance),
            provenance_completeness=(provenance_completeness),
            citation_count=len(review.citations),
            backend_validation_valid=(backend_validation_valid),
            backend_validation_issue_count=(backend_validation_issue_count),
            corpus_scope_note_present=(corpus_scope_note_present),
            structural_valid=(structural_valid),
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

    def _reference_integrity(
        self,
        total_references: int,
        missing_reference_count: int,
    ) -> float:

        if total_references == 0:

            return 1.0

        return (total_references - missing_reference_count) / total_references

    def _unique_in_order(
        self,
        values: list[str],
    ) -> list[str]:

        seen = set()
        unique = []

        for value in values:

            if value not in seen:

                unique.append(value)

                seen.add(value)

        return unique
