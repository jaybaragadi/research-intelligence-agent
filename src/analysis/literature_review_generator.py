from __future__ import annotations

from collections import defaultdict

from src.analysis.literature_review_models import (
    LiteratureReview,
    LiteratureReviewEvidence,
    LiteratureReviewEvidenceAggregation,
    LiteratureReviewFinding,
    LiteratureReviewSection,
    LiteratureReviewSectionType,
    LiteratureReviewSynthesis,
)

from src.analysis.literature_review_taxonomy import (
    LITERATURE_REVIEW_SECTIONS,
)


class DeterministicLiteratureReviewGenerator:
    """
    Convert structured synthesis findings into a readable
    literature review without introducing new semantic claims.

    The generator:
    - does not retrieve evidence
    - does not classify evidence
    - does not infer superiority
    - does not infer universal research gaps
    - preserves claim-to-evidence traceability
    """

    def generate(
        self,
        aggregation: LiteratureReviewEvidenceAggregation,
        synthesis: LiteratureReviewSynthesis,
        title: str = "Evidence-Grounded Literature Review",
    ) -> LiteratureReview:

        self._validate_inputs(
            aggregation=aggregation,
            synthesis=synthesis,
        )

        evidence_by_section = {
            bundle.section_type: list(bundle.evidence)
            for bundle in aggregation.bundles
        }

        findings_by_section = defaultdict(list)

        for finding in synthesis.findings:
            findings_by_section[
                finding.section_type
            ].append(
                finding
            )

        sections: list[
            LiteratureReviewSection
        ] = []

        for definition in LITERATURE_REVIEW_SECTIONS:

            section_type = (
                definition.section_type
            )

            section_evidence = list(
                evidence_by_section.get(
                    section_type,
                    [],
                )
            )

            synthesis_findings = (
                findings_by_section.get(
                    section_type,
                    [],
                )
            )

            final_findings = [
                LiteratureReviewFinding(
                    finding_id=item.finding_id,
                    section_type=item.section_type,
                    statement=item.statement,
                    paper_ids=list(
                        item.paper_ids
                    ),
                    evidence_ids=list(
                        item.evidence_ids
                    ),
                )
                for item
                in synthesis_findings
            ]

            narrative = (
                self._build_narrative(
                    section_type=section_type,
                    findings=final_findings,
                    paper_count=len(
                        aggregation.paper_ids
                    ),
                )
            )

            sections.append(
                LiteratureReviewSection(
                    section_type=section_type,
                    title=definition.title,
                    objective=definition.objective,
                    findings=final_findings,
                    evidence=section_evidence,
                    narrative=narrative,
                )
            )

        citations = (
            self._collect_citations(
                aggregation
            )
        )

        return LiteratureReview(
            query=aggregation.query,
            paper_ids=list(
                aggregation.paper_ids
            ),
            title=title.strip()
            or "Evidence-Grounded Literature Review",
            sections=sections,
            citations=citations,
        )

    def _validate_inputs(
        self,
        aggregation: LiteratureReviewEvidenceAggregation,
        synthesis: LiteratureReviewSynthesis,
    ) -> None:

        if (
            aggregation.query
            != synthesis.query
        ):
            raise ValueError(
                "aggregation and synthesis "
                "must use the same query"
            )

        if (
            aggregation.paper_ids
            != synthesis.paper_ids
        ):
            raise ValueError(
                "aggregation and synthesis "
                "must use the same paper_ids"
            )

    def _build_narrative(
        self,
        section_type: LiteratureReviewSectionType,
        findings: list[
            LiteratureReviewFinding
        ],
        paper_count: int,
    ) -> str:

        if (
            section_type
            == LiteratureReviewSectionType.INTRODUCTION
        ):
            return self._build_introduction(
                paper_count=paper_count
            )

        if (
            section_type
            == LiteratureReviewSectionType.CONCLUSION
        ):
            return self._build_conclusion(
                findings=findings,
                paper_count=paper_count,
            )

        if not findings:
            return self._empty_section_statement(
                section_type
            )

        sentences = []

        for finding in findings:

            citation_marker = (
                self._evidence_marker(
                    finding.evidence_ids
                )
            )

            sentence = (
                finding.statement.strip()
            )

            if (
                citation_marker
                and sentence
            ):
                sentence = (
                    f"{sentence} "
                    f"{citation_marker}"
                )

            if sentence:
                sentences.append(
                    sentence
                )

        return " ".join(
            sentences
        )

    def _build_introduction(
        self,
        paper_count: int,
    ) -> str:

        return (
            "This evidence-grounded literature review "
            f"synthesizes {paper_count} paper"
            f"{'' if paper_count == 1 else 's'} "
            "from the indexed corpus. "
            "The review organizes validated evidence "
            "around research approaches, generation "
            "strategies, feedback and iteration, "
            "evaluation, reported limitations, and "
            "future research directions."
        )

    def _build_conclusion(
        self,
        findings: list[
            LiteratureReviewFinding
        ],
        paper_count: int,
    ) -> str:

        if findings:
            sentences = []

            for finding in findings:

                marker = (
                    self._evidence_marker(
                        finding.evidence_ids
                    )
                )

                text = (
                    finding.statement.strip()
                )

                if marker:
                    text = (
                        f"{text} {marker}"
                    )

                sentences.append(
                    text
                )

            return " ".join(
                sentences
            )

        return (
            f"Across the {paper_count} indexed "
            "papers, the preceding sections summarize "
            "the validated evidence patterns available "
            "in the corpus. Conclusions should therefore "
            "be interpreted within the boundaries of "
            "this indexed collection rather than as "
            "claims about all published research."
        )

    def _empty_section_statement(
        self,
        section_type: LiteratureReviewSectionType,
    ) -> str:

        labels = {
            LiteratureReviewSectionType.RESEARCH_LANDSCAPE: (
                "No qualifying evidence was available "
                "for this section in the current "
                "evidence aggregation."
            ),

            LiteratureReviewSectionType.GENERATION_STRATEGIES: (
                "No qualifying generation-strategy "
                "evidence was available in the current "
                "evidence aggregation."
            ),

            LiteratureReviewSectionType.FEEDBACK_AND_ITERATION: (
                "No qualifying feedback or iterative-"
                "refinement evidence was available in "
                "the current evidence aggregation."
            ),

            LiteratureReviewSectionType.QUALITY_AND_EVALUATION: (
                "No qualifying quality or evaluation "
                "evidence was available in the current "
                "evidence aggregation."
            ),

            LiteratureReviewSectionType.LIMITATIONS_AND_GAPS: (
                "No qualifying limitation or unresolved-"
                "problem evidence was available in the "
                "current evidence aggregation."
            ),

            LiteratureReviewSectionType.FUTURE_DIRECTIONS: (
                "No qualifying explicit future-work "
                "evidence was available in the current "
                "evidence aggregation."
            ),
        }

        return labels.get(
            section_type,
            (
                "No qualifying evidence was available "
                "for this section."
            ),
        )

    def _evidence_marker(
        self,
        evidence_ids: list[str],
    ) -> str:

        cleaned = []
        seen = set()

        for evidence_id in evidence_ids:

            value = evidence_id.strip()

            if not value:
                continue

            if value in seen:
                continue

            seen.add(
                value
            )

            cleaned.append(
                value
            )

        if not cleaned:
            return ""

        return (
            "["
            + "; ".join(cleaned)
            + "]"
        )

    def _collect_citations(
        self,
        aggregation: LiteratureReviewEvidenceAggregation,
    ) -> list[str]:

        citations = []
        seen = set()

        for bundle in aggregation.bundles:

            for evidence in bundle.evidence:

                citation = (
                    evidence.citation_text.strip()
                )

                if not citation:
                    continue

                if citation in seen:
                    continue

                seen.add(
                    citation
                )

                citations.append(
                    citation
                )

        return citations