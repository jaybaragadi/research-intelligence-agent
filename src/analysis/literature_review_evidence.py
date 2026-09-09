from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from src.analysis.literature_review_models import (
    LiteratureReviewEvidence,
    LiteratureReviewEvidenceAggregation,
    LiteratureReviewEvidenceBundle,
    LiteratureReviewSectionType,
)


DIMENSION_TO_REVIEW_SECTIONS = {
    "generation_strategy": (
        LiteratureReviewSectionType.RESEARCH_LANDSCAPE,
        LiteratureReviewSectionType.GENERATION_STRATEGIES,
    ),

    "feedback_signal": (
        LiteratureReviewSectionType.FEEDBACK_AND_ITERATION,
    ),

    "iteration_strategy": (
        LiteratureReviewSectionType.FEEDBACK_AND_ITERATION,
    ),

    "quality_objective": (
        LiteratureReviewSectionType.QUALITY_AND_EVALUATION,
    ),

    "evaluation_method": (
        LiteratureReviewSectionType.QUALITY_AND_EVALUATION,
    ),

    "limitations": (
        LiteratureReviewSectionType.LIMITATIONS_AND_GAPS,
    ),
}


class LiteratureReviewEvidenceAggregator:
    """
    Normalize validated Phase 9 and Phase 10 evidence
    into section-specific literature-review evidence.

    This component does not perform retrieval,
    semantic inference, or prose generation.
    """

    def aggregate(
        self,
        query: str,
        paper_ids: list[str],
        dimension_evidence: Iterable[object],
        explicit_gap_evidence: Iterable[object],
    ) -> LiteratureReviewEvidenceAggregation:

        cleaned_query = query.strip()

        if not cleaned_query:
            raise ValueError(
                "query must not be empty"
            )

        cleaned_paper_ids = (
            self._clean_paper_ids(
                paper_ids
            )
        )

        if not cleaned_paper_ids:
            raise ValueError(
                "paper_ids must not be empty"
            )

        allowed_paper_ids = set(
            cleaned_paper_ids
        )

        section_evidence: dict[
            LiteratureReviewSectionType,
            list[LiteratureReviewEvidence],
        ] = defaultdict(list)

        section_seen_ids: dict[
            LiteratureReviewSectionType,
            set[str],
        ] = defaultdict(set)

        self._add_dimension_evidence(
            evidence_items=dimension_evidence,
            allowed_paper_ids=allowed_paper_ids,
            section_evidence=section_evidence,
            section_seen_ids=section_seen_ids,
        )

        self._add_gap_evidence(
            evidence_items=explicit_gap_evidence,
            allowed_paper_ids=allowed_paper_ids,
            section_evidence=section_evidence,
            section_seen_ids=section_seen_ids,
        )

        bundles = []

        for section_type in (
            LiteratureReviewSectionType
        ):
            evidence = section_evidence.get(
                section_type,
                [],
            )

            if not evidence:
                continue

            bundles.append(
                LiteratureReviewEvidenceBundle(
                    section_type=section_type,
                    evidence=evidence,
                )
            )

        return LiteratureReviewEvidenceAggregation(
            query=cleaned_query,
            paper_ids=cleaned_paper_ids,
            bundles=bundles,
        )

    def _add_dimension_evidence(
        self,
        evidence_items: Iterable[object],
        allowed_paper_ids: set[str],
        section_evidence: dict,
        section_seen_ids: dict,
    ) -> None:

        for item in evidence_items:

            dimension = getattr(
                item,
                "dimension",
                None,
            )

            if dimension is None:
                continue

            dimension_value = (
                dimension.value
                if hasattr(
                    dimension,
                    "value",
                )
                else str(dimension)
            )

            target_sections = (
                DIMENSION_TO_REVIEW_SECTIONS.get(
                    dimension_value,
                    (),
                )
            )

            if not target_sections:
                continue

            normalized = (
                self._normalize_evidence(
                    item
                )
            )

            if normalized is None:
                continue

            if (
                normalized.paper_id
                not in allowed_paper_ids
            ):
                continue

            for section_type in target_sections:

                self._append_unique(
                    section_type=section_type,
                    evidence=normalized,
                    section_evidence=section_evidence,
                    section_seen_ids=section_seen_ids,
                )

    def _add_gap_evidence(
        self,
        evidence_items: Iterable[object],
        allowed_paper_ids: set[str],
        section_evidence: dict,
        section_seen_ids: dict,
    ) -> None:

        for item in evidence_items:

            signal_type = getattr(
                item,
                "signal_type",
                None,
            )

            if signal_type is None:
                continue

            signal_value = (
                signal_type.value
                if hasattr(
                    signal_type,
                    "value",
                )
                else str(signal_type)
            )

            target_sections = (
                self._gap_sections(
                    signal_value
                )
            )

            if not target_sections:
                continue

            normalized = (
                self._normalize_evidence(
                    item
                )
            )

            if normalized is None:
                continue

            if (
                normalized.paper_id
                not in allowed_paper_ids
            ):
                continue

            for section_type in target_sections:

                self._append_unique(
                    section_type=section_type,
                    evidence=normalized,
                    section_evidence=section_evidence,
                    section_seen_ids=section_seen_ids,
                )

    def _gap_sections(
        self,
        signal_type: str,
    ) -> tuple[
        LiteratureReviewSectionType,
        ...,
    ]:

        if signal_type == "limitation":
            return (
                LiteratureReviewSectionType.LIMITATIONS_AND_GAPS,
            )

        if signal_type == "future_work":
            return (
                LiteratureReviewSectionType.FUTURE_DIRECTIONS,
            )

        if signal_type == "unresolved_problem":
            return (
                LiteratureReviewSectionType.LIMITATIONS_AND_GAPS,
                LiteratureReviewSectionType.FUTURE_DIRECTIONS,
            )

        return ()

    def _normalize_evidence(
        self,
        item: object,
    ) -> LiteratureReviewEvidence | None:

        evidence_id = getattr(
            item,
            "evidence_id",
            None,
        )

        paper_id = getattr(
            item,
            "paper_id",
            None,
        )

        page_number = getattr(
            item,
            "page_number",
            None,
        )

        text = getattr(
            item,
            "text",
            None,
        )

        citation_text = getattr(
            item,
            "citation_text",
            None,
        )

        if not evidence_id:
            return None

        if not paper_id:
            return None

        if page_number is None:
            return None

        if not text:
            return None

        if not citation_text:
            return None

        return LiteratureReviewEvidence(
            evidence_id=str(
                evidence_id
            ),
            paper_id=str(
                paper_id
            ),
            page_number=int(
                page_number
            ),
            section=getattr(
                item,
                "section",
                None,
            ),
            text=str(
                text
            ),
            citation_text=str(
                citation_text
            ),
        )

    def _append_unique(
        self,
        section_type: LiteratureReviewSectionType,
        evidence: LiteratureReviewEvidence,
        section_evidence: dict,
        section_seen_ids: dict,
    ) -> None:

        if (
            evidence.evidence_id
            in section_seen_ids[
                section_type
            ]
        ):
            return

        section_seen_ids[
            section_type
        ].add(
            evidence.evidence_id
        )

        section_evidence[
            section_type
        ].append(
            evidence
        )

    def _clean_paper_ids(
        self,
        paper_ids: list[str],
    ) -> list[str]:

        cleaned = []
        seen = set()

        for paper_id in paper_ids:

            value = paper_id.strip()

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

        return cleaned