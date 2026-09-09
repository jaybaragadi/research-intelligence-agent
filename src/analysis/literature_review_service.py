from __future__ import annotations

from src.analysis.literature_review_evidence import (
    LiteratureReviewEvidenceAggregator,
)

from src.analysis.literature_review_generator import (
    DeterministicLiteratureReviewGenerator,
)

from src.analysis.literature_review_models import (
    LiteratureReview,
)

from src.analysis.literature_review_synthesis import (
    LiteratureReviewSynthesisBuilder,
)

from src.analysis.literature_review_validator import (
    LiteratureReviewGroundingValidator,
)

from src.analysis.comparative_service import (
    ComparativeAnalysisService,
)

from src.analysis.gap_analysis_service import (
    ResearchGapAnalysisService,
)

class LiteratureReviewService:
    """
    Orchestrate evidence-grounded literature-review generation.

    Pipeline:
    1. Run comparative analysis.
    2. Run research-gap analysis.
    3. Normalize validated evidence.
    4. Build structured synthesis findings.
    5. Validate grounding.
    6. Generate deterministic review.
    """

    def __init__(
        self,
        comparative_service: ComparativeAnalysisService | None = None,
        gap_service: ResearchGapAnalysisService | None = None,
        evidence_aggregator: LiteratureReviewEvidenceAggregator | None = None,
        synthesis_builder: LiteratureReviewSynthesisBuilder | None = None,
        grounding_validator: LiteratureReviewGroundingValidator | None = None,
        generator: DeterministicLiteratureReviewGenerator | None = None,
    ) -> None:

        self.comparative_service = (
            comparative_service
            or ComparativeAnalysisService()
        )

        self.gap_service = (
            gap_service
            or ResearchGapAnalysisService()
        )

        self.evidence_aggregator = (
            evidence_aggregator
            or LiteratureReviewEvidenceAggregator()
        )

        self.synthesis_builder = (
            synthesis_builder
            or LiteratureReviewSynthesisBuilder()
        )

        self.grounding_validator = (
            grounding_validator
            or LiteratureReviewGroundingValidator()
        )

        self.generator = (
            generator
            or DeterministicLiteratureReviewGenerator()
        )

    def generate(
        self,
        query: str,
        paper_ids: list[str],
        title: str = "Evidence-Grounded Literature Review",
        evidence_per_paper: int = 8,
    ) -> LiteratureReview:

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

        if len(cleaned_paper_ids) < 2:
            raise ValueError(
                "literature review requires "
                "at least two unique paper_ids"
            )

        if evidence_per_paper <= 0:
            raise ValueError(
                "evidence_per_paper must be positive"
            )

        comparative_analysis = (
            self.comparative_service.analyze(
                query=cleaned_query,
                paper_ids=cleaned_paper_ids,
                evidence_per_paper=(
                    evidence_per_paper
                ),
            )
        )

        gap_analysis = (
            self.gap_service.analyze(
                query=cleaned_query,
                paper_ids=cleaned_paper_ids,
                evidence_per_paper=(
                    evidence_per_paper
                ),
            )
        )

        dimension_evidence = (
            self._collect_dimension_evidence(
                comparative_analysis
            )
        )

        explicit_gap_evidence = (
            self._collect_explicit_gap_evidence(
                gap_analysis
            )
        )

        aggregation = (
            self.evidence_aggregator.aggregate(
                query=cleaned_query,
                paper_ids=cleaned_paper_ids,
                dimension_evidence=(
                    dimension_evidence
                ),
                explicit_gap_evidence=(
                    explicit_gap_evidence
                ),
            )
        )

        synthesis = (
            self.synthesis_builder.build(
                aggregation
            )
        )

        validation = (
            self.grounding_validator.validate(
                aggregation,
                synthesis,
            )
        )

        if not validation.valid:
            issue_summary = "; ".join(
                (
                    f"{issue.code.value}: "
                    f"{issue.message}"
                )
                for issue
                in validation.issues
            )

            raise ValueError(
                "literature review grounding "
                "validation failed: "
                f"{issue_summary}"
            )

        review = (
            self.generator.generate(
                aggregation=aggregation,
                synthesis=synthesis,
                title=title,
            )
        )

        review.validation = (
            validation
        )

        return review

    def _collect_dimension_evidence(
        self,
        comparative_analysis: object,
    ) -> list[object]:

        evidence_items = []
        seen = set()

        profiles = getattr(
            comparative_analysis,
            "profiles",
            [],
        )

        for profile in profiles:

            dimensions = getattr(
                profile,
                "dimensions",
                [],
            )

            for dimension_analysis in dimensions:

                evidence = getattr(
                    dimension_analysis,
                    "evidence",
                    [],
                )

                for item in evidence:

                    evidence_id = getattr(
                        item,
                        "evidence_id",
                        None,
                    )

                    if not evidence_id:
                        continue

                    if evidence_id in seen:
                        continue

                    seen.add(
                        evidence_id
                    )

                    evidence_items.append(
                        item
                    )

        return evidence_items

    def _collect_explicit_gap_evidence(
        self,
        gap_analysis: object,
    ) -> list[object]:

        evidence_items = []
        seen = set()

        paper_signals = getattr(
            gap_analysis,
            "paper_signals",
            [],
        )

        for paper_signal in paper_signals:

            signals = getattr(
                paper_signal,
                "signals",
                [],
            )

            for item in signals:

                evidence_id = getattr(
                    item,
                    "evidence_id",
                    None,
                )

                if not evidence_id:
                    continue

                dedupe_key = (
                    evidence_id,
                    getattr(
                        item,
                        "signal_type",
                        None,
                    ),
                )

                if dedupe_key in seen:
                    continue

                seen.add(
                    dedupe_key
                )

                evidence_items.append(
                    item
                )

        return evidence_items

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