from dataclasses import dataclass, field

import pytest

from src.analysis.literature_review_models import (
    LiteratureReviewSectionType,
    LiteratureReviewValidationIssue,
    LiteratureReviewValidationIssueCode,
    LiteratureReviewValidationResult,
)

from src.analysis.literature_review_service import (
    LiteratureReviewService,
)


@dataclass
class FakeDimensionEvidence:
    evidence_id: str
    paper_id: str
    page_number: int
    section: str | None
    text: str
    citation_text: str
    dimension: str


@dataclass
class FakeDimensionAnalysis:
    evidence: list[
        FakeDimensionEvidence
    ] = field(
        default_factory=list
    )


@dataclass
class FakeProfile:
    dimensions: list[
        FakeDimensionAnalysis
    ] = field(
        default_factory=list
    )


@dataclass
class FakeComparativeAnalysis:
    profiles: list[
        FakeProfile
    ] = field(
        default_factory=list
    )


@dataclass
class FakeGapEvidence:
    evidence_id: str
    paper_id: str
    page_number: int
    section: str | None
    text: str
    citation_text: str
    signal_type: str


@dataclass
class FakePaperGapSignals:
    signals: list[
        FakeGapEvidence
    ] = field(
        default_factory=list
    )


@dataclass
class FakeGapAnalysis:
    paper_signals: list[
        FakePaperGapSignals
    ] = field(
        default_factory=list
    )


class FakeComparativeService:

    def __init__(
        self,
        result,
    ):
        self.result = result
        self.calls = []

    def analyze(
        self,
        query,
        paper_ids,
        evidence_per_paper,
    ):
        self.calls.append(
            (
                query,
                paper_ids,
                evidence_per_paper,
            )
        )

        return self.result


class FakeGapService:

    def __init__(
        self,
        result,
    ):
        self.result = result
        self.calls = []

    def analyze(
        self,
        query,
        paper_ids,
        evidence_per_paper,
    ):
        self.calls.append(
            (
                query,
                paper_ids,
                evidence_per_paper,
            )
        )

        return self.result


class AlwaysInvalidValidator:

    def validate(
        self,
        aggregation,
        synthesis,
    ):
        return (
            LiteratureReviewValidationResult(
                valid=False,
                issues=[
                    LiteratureReviewValidationIssue(
                        code=(
                            LiteratureReviewValidationIssueCode
                            .UNKNOWN_EVIDENCE_ID
                        ),
                        message=(
                            "Synthetic validation failure."
                        ),
                    )
                ],
            )
        )


def build_services():

    comparative_result = (
        FakeComparativeAnalysis(
            profiles=[
                FakeProfile(
                    dimensions=[
                        FakeDimensionAnalysis(
                            evidence=[
                                FakeDimensionEvidence(
                                    evidence_id="E1",
                                    paper_id="03_mutap",
                                    page_number=5,
                                    section="methodology",
                                    text=(
                                        "Mutation feedback "
                                        "guides test generation."
                                    ),
                                    citation_text=(
                                        "MuTAP (2023), p. 5"
                                    ),
                                    dimension=(
                                        "generation_strategy"
                                    ),
                                ),
                                FakeDimensionEvidence(
                                    evidence_id="E2",
                                    paper_id="05_coverup",
                                    page_number=4,
                                    section="methodology",
                                    text=(
                                        "Coverage feedback "
                                        "guides test generation."
                                    ),
                                    citation_text=(
                                        "CoverUp (2024), p. 4"
                                    ),
                                    dimension=(
                                        "generation_strategy"
                                    ),
                                ),
                            ]
                        )
                    ]
                )
            ]
        )
    )

    gap_result = (
        FakeGapAnalysis(
            paper_signals=[
                FakePaperGapSignals(
                    signals=[
                        FakeGapEvidence(
                            evidence_id="E3",
                            paper_id="03_mutap",
                            page_number=13,
                            section="conclusion",
                            text=(
                                "Future work may investigate "
                                "additional settings."
                            ),
                            citation_text=(
                                "MuTAP (2023), p. 13"
                            ),
                            signal_type="future_work",
                        )
                    ]
                )
            ]
        )
    )

    return (
        FakeComparativeService(
            comparative_result
        ),
        FakeGapService(
            gap_result
        ),
    )


def test_service_generates_valid_review():

    comparative_service, gap_service = (
        build_services()
    )

    service = LiteratureReviewService(
        comparative_service=(
            comparative_service
        ),
        gap_service=gap_service,
    )

    review = service.generate(
        query="Review LLM-based test generation.",
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
        evidence_per_paper=6,
    )

    assert (
        review.validation
        is not None
    )

    assert (
        review.validation.valid
        is True
    )

    assert review.paper_ids == [
        "03_mutap",
        "05_coverup",
    ]


def test_service_creates_generation_section():

    comparative_service, gap_service = (
        build_services()
    )

    review = LiteratureReviewService(
        comparative_service=(
            comparative_service
        ),
        gap_service=gap_service,
    ).generate(
        query="Review generation strategies.",
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    section = next(
        item
        for item
        in review.sections
        if item.section_type
        == LiteratureReviewSectionType
        .GENERATION_STRATEGIES
    )

    assert section.findings

    assert (
        section.findings[0]
        .paper_ids
        == [
            "03_mutap",
            "05_coverup",
        ]
    )


def test_service_creates_future_direction_section():

    comparative_service, gap_service = (
        build_services()
    )

    review = LiteratureReviewService(
        comparative_service=(
            comparative_service
        ),
        gap_service=gap_service,
    ).generate(
        query="Review future directions.",
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    section = next(
        item
        for item
        in review.sections
        if item.section_type
        == LiteratureReviewSectionType
        .FUTURE_DIRECTIONS
    )

    assert section.findings

    assert (
        "future"
        in section.narrative.lower()
    )


def test_service_passes_query_and_papers_to_dependencies():

    comparative_service, gap_service = (
        build_services()
    )

    service = LiteratureReviewService(
        comparative_service=(
            comparative_service
        ),
        gap_service=gap_service,
    )

    service.generate(
        query="  Review testing research.  ",
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
        evidence_per_paper=7,
    )

    assert (
        comparative_service.calls[0]
        == (
            "Review testing research.",
            [
                "03_mutap",
                "05_coverup",
            ],
            7,
        )
    )

    assert (
        gap_service.calls[0]
        == (
            "Review testing research.",
            [
                "03_mutap",
                "05_coverup",
            ],
            7,
        )
    )


def test_duplicate_paper_ids_are_removed():

    comparative_service, gap_service = (
        build_services()
    )

    service = LiteratureReviewService(
        comparative_service=(
            comparative_service
        ),
        gap_service=gap_service,
    )

    review = service.generate(
        query="Review research.",
        paper_ids=[
            "03_mutap",
            "05_coverup",
            "03_mutap",
        ],
    )

    assert review.paper_ids == [
        "03_mutap",
        "05_coverup",
    ]


def test_empty_query_is_rejected():

    comparative_service, gap_service = (
        build_services()
    )

    service = LiteratureReviewService(
        comparative_service=(
            comparative_service
        ),
        gap_service=gap_service,
    )

    with pytest.raises(
        ValueError,
        match="query",
    ):
        service.generate(
            query="   ",
            paper_ids=[
                "03_mutap",
                "05_coverup",
            ],
        )


def test_less_than_two_unique_papers_is_rejected():

    comparative_service, gap_service = (
        build_services()
    )

    service = LiteratureReviewService(
        comparative_service=(
            comparative_service
        ),
        gap_service=gap_service,
    )

    with pytest.raises(
        ValueError,
        match="at least two",
    ):
        service.generate(
            query="Review research.",
            paper_ids=[
                "03_mutap",
                "03_mutap",
            ],
        )


def test_invalid_evidence_per_paper_is_rejected():

    comparative_service, gap_service = (
        build_services()
    )

    service = LiteratureReviewService(
        comparative_service=(
            comparative_service
        ),
        gap_service=gap_service,
    )

    with pytest.raises(
        ValueError,
        match="evidence_per_paper",
    ):
        service.generate(
            query="Review research.",
            paper_ids=[
                "03_mutap",
                "05_coverup",
            ],
            evidence_per_paper=0,
        )


def test_generation_stops_when_grounding_fails():

    comparative_service, gap_service = (
        build_services()
    )

    service = LiteratureReviewService(
        comparative_service=(
            comparative_service
        ),
        gap_service=gap_service,
        grounding_validator=(
            AlwaysInvalidValidator()
        ),
    )

    with pytest.raises(
        ValueError,
        match="grounding validation failed",
    ):
        service.generate(
            query="Review research.",
            paper_ids=[
                "03_mutap",
                "05_coverup",
            ],
        )


def test_custom_title_is_preserved():

    comparative_service, gap_service = (
        build_services()
    )

    service = LiteratureReviewService(
        comparative_service=(
            comparative_service
        ),
        gap_service=gap_service,
    )

    review = service.generate(
        query="Review research.",
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
        title=(
            "LLMs for Automated Software Testing"
        ),
    )

    assert (
        review.title
        == "LLMs for Automated Software Testing"
    )