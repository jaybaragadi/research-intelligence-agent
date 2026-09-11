from __future__ import annotations

from collections import defaultdict

from src.analysis.literature_review_models import (
    LiteratureReviewEvidence,
    LiteratureReviewEvidenceAggregation,
    LiteratureReviewSectionType,
    LiteratureReviewSynthesis,
    LiteratureReviewSynthesisFinding,
)


class LiteratureReviewSynthesisBuilder:
    """
    Build structured, evidence-backed findings from
    literature-review evidence bundles.

    This component does not generate free-form prose.
    """

    def build(
        self,
        aggregation: LiteratureReviewEvidenceAggregation,
    ) -> LiteratureReviewSynthesis:

        findings: list[LiteratureReviewSynthesisFinding] = []

        next_finding_number = 1

        for bundle in aggregation.bundles:

            section_findings = self._build_section_findings(
                section_type=bundle.section_type,
                evidence=bundle.evidence,
                starting_index=next_finding_number,
            )

            findings.extend(section_findings)

            next_finding_number += len(section_findings)

        return LiteratureReviewSynthesis(
            query=aggregation.query,
            paper_ids=list(aggregation.paper_ids),
            findings=findings,
        )

    def _build_section_findings(
        self,
        section_type: LiteratureReviewSectionType,
        evidence: list[LiteratureReviewEvidence],
        starting_index: int,
    ) -> list[LiteratureReviewSynthesisFinding]:

        if not evidence:
            return []

        grouped_by_paper = self._group_by_paper(evidence)

        if len(grouped_by_paper) >= 2:
            finding = self._build_cross_paper_finding(
                section_type=section_type,
                grouped_by_paper=grouped_by_paper,
                finding_id=(f"SF{starting_index}"),
            )

            return [finding]

        paper_id = next(iter(grouped_by_paper))

        paper_evidence = grouped_by_paper[paper_id]

        finding = self._build_single_paper_finding(
            section_type=section_type,
            paper_id=paper_id,
            evidence=paper_evidence,
            finding_id=(f"SF{starting_index}"),
        )

        return [finding]

    def _group_by_paper(
        self,
        evidence: list[LiteratureReviewEvidence],
    ) -> dict[
        str,
        list[LiteratureReviewEvidence],
    ]:

        grouped: dict[
            str,
            list[LiteratureReviewEvidence],
        ] = defaultdict(list)

        seen_ids: dict[
            str,
            set[str],
        ] = defaultdict(set)

        for item in evidence:

            if item.evidence_id in seen_ids[item.paper_id]:
                continue

            seen_ids[item.paper_id].add(item.evidence_id)

            grouped[item.paper_id].append(item)

        return dict(grouped)

    def _build_cross_paper_finding(
        self,
        section_type: LiteratureReviewSectionType,
        grouped_by_paper: dict[
            str,
            list[LiteratureReviewEvidence],
        ],
        finding_id: str,
    ) -> LiteratureReviewSynthesisFinding:

        paper_ids = list(grouped_by_paper.keys())

        evidence_ids = []

        for paper_id in paper_ids:

            for item in grouped_by_paper[paper_id]:
                evidence_ids.append(item.evidence_id)

        statement = self._cross_paper_statement(
            section_type=section_type,
            paper_count=len(paper_ids),
        )

        return LiteratureReviewSynthesisFinding(
            finding_id=finding_id,
            section_type=section_type,
            statement=statement,
            paper_ids=paper_ids,
            evidence_ids=evidence_ids,
            support_count=len(paper_ids),
            is_cross_paper=True,
        )

    def _build_single_paper_finding(
        self,
        section_type: LiteratureReviewSectionType,
        paper_id: str,
        evidence: list[LiteratureReviewEvidence],
        finding_id: str,
    ) -> LiteratureReviewSynthesisFinding:

        evidence_ids = [item.evidence_id for item in evidence]

        statement = self._single_paper_statement(
            section_type=section_type,
            paper_id=paper_id,
        )

        return LiteratureReviewSynthesisFinding(
            finding_id=finding_id,
            section_type=section_type,
            statement=statement,
            paper_ids=[paper_id],
            evidence_ids=evidence_ids,
            support_count=1,
            is_cross_paper=False,
        )

    def _cross_paper_statement(
        self,
        section_type: LiteratureReviewSectionType,
        paper_count: int,
    ) -> str:

        templates = {
            LiteratureReviewSectionType.RESEARCH_LANDSCAPE: (
                "Multiple indexed studies represent "
                "distinct methodological approaches "
                "to LLM-based automated test generation."
            ),
            LiteratureReviewSectionType.GENERATION_STRATEGIES: (
                "Multiple indexed studies use structured "
                "strategies to guide or improve "
                "LLM-generated tests."
            ),
            LiteratureReviewSectionType.FEEDBACK_AND_ITERATION: (
                "Multiple indexed studies incorporate "
                "feedback or iterative refinement into "
                "LLM-based test generation."
            ),
            LiteratureReviewSectionType.QUALITY_AND_EVALUATION: (
                "Multiple indexed studies evaluate "
                "generated tests using explicit quality "
                "objectives or empirical evaluation methods."
            ),
            LiteratureReviewSectionType.LIMITATIONS_AND_GAPS: (
                "Multiple indexed studies report "
                "limitations or unresolved research "
                "constraints."
            ),
            LiteratureReviewSectionType.FUTURE_DIRECTIONS: (
                "Multiple indexed studies identify " "future research directions."
            ),
        }

        return templates.get(
            section_type,
            (
                f"Evidence from {paper_count} indexed "
                "papers contributes to this review section."
            ),
        )

    def _single_paper_statement(
        self,
        section_type: LiteratureReviewSectionType,
        paper_id: str,
    ) -> str:

        templates = {
            LiteratureReviewSectionType.RESEARCH_LANDSCAPE: (
                f"{paper_id} contributes methodological "
                "evidence to the indexed research landscape."
            ),
            LiteratureReviewSectionType.GENERATION_STRATEGIES: (
                f"{paper_id} provides evidence about "
                "an LLM-based test-generation strategy."
            ),
            LiteratureReviewSectionType.FEEDBACK_AND_ITERATION: (
                f"{paper_id} provides evidence about "
                "feedback or iterative refinement."
            ),
            LiteratureReviewSectionType.QUALITY_AND_EVALUATION: (
                f"{paper_id} provides evidence about "
                "test-quality objectives or evaluation."
            ),
            LiteratureReviewSectionType.LIMITATIONS_AND_GAPS: (
                f"{paper_id} reports a limitation or " "unresolved research constraint."
            ),
            LiteratureReviewSectionType.FUTURE_DIRECTIONS: (
                f"{paper_id} reports an explicit " "future research direction."
            ),
        }

        return templates.get(
            section_type,
            (f"{paper_id} contributes evidence " "to this review section."),
        )
