from dataclasses import dataclass

from src.analysis.literature_review_evidence import (
    LiteratureReviewEvidenceAggregator,
)
from src.analysis.literature_review_models import (
    LiteratureReviewSectionType,
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
class FakeGapEvidence:
    evidence_id: str
    paper_id: str
    page_number: int
    section: str | None
    text: str
    citation_text: str
    signal_type: str


def get_bundle(
    aggregation,
    section_type,
):

    return next(
        bundle for bundle in aggregation.bundles if bundle.section_type == section_type
    )


def test_generation_strategy_maps_to_two_review_sections():

    evidence = FakeDimensionEvidence(
        evidence_id="E1",
        paper_id="03_mutap",
        page_number=5,
        section="methodology",
        text=("Mutation feedback is used " "to improve generated tests."),
        citation_text=("MuTAP (2023), p. 5"),
        dimension="generation_strategy",
    )

    aggregation = LiteratureReviewEvidenceAggregator().aggregate(
        query=("Review LLM test generation."),
        paper_ids=[
            "03_mutap",
        ],
        dimension_evidence=[evidence],
        explicit_gap_evidence=[],
    )

    section_types = {bundle.section_type for bundle in aggregation.bundles}

    assert LiteratureReviewSectionType.RESEARCH_LANDSCAPE in section_types

    assert LiteratureReviewSectionType.GENERATION_STRATEGIES in section_types


def test_feedback_and_iteration_share_review_section():

    evidence_items = [
        FakeDimensionEvidence(
            evidence_id="E1",
            paper_id="05_coverup",
            page_number=4,
            section="methodology",
            text="Coverage feedback is used.",
            citation_text="CoverUp (2025), p. 4",
            dimension="feedback_signal",
        ),
        FakeDimensionEvidence(
            evidence_id="E2",
            paper_id="05_coverup",
            page_number=4,
            section="methodology",
            text="The system iterates on failed tests.",
            citation_text="CoverUp (2025), p. 4",
            dimension="iteration_strategy",
        ),
    ]

    aggregation = LiteratureReviewEvidenceAggregator().aggregate(
        query="Review iterative test generation.",
        paper_ids=[
            "05_coverup",
        ],
        dimension_evidence=evidence_items,
        explicit_gap_evidence=[],
    )

    bundle = get_bundle(
        aggregation,
        LiteratureReviewSectionType.FEEDBACK_AND_ITERATION,
    )

    assert len(bundle.evidence) == 2


def test_limitation_gap_evidence_maps_to_limitations_section():

    evidence = FakeGapEvidence(
        evidence_id="E10",
        paper_id="04_symprompt",
        page_number=16,
        section="threats_to_validity",
        text=("The evaluation is limited " "to specific languages and models."),
        citation_text=("SymPrompt (2024), p. 16"),
        signal_type="limitation",
    )

    aggregation = LiteratureReviewEvidenceAggregator().aggregate(
        query="Review limitations.",
        paper_ids=[
            "04_symprompt",
        ],
        dimension_evidence=[],
        explicit_gap_evidence=[evidence],
    )

    bundle = get_bundle(
        aggregation,
        LiteratureReviewSectionType.LIMITATIONS_AND_GAPS,
    )

    assert bundle.evidence[0].evidence_id == "E10"


def test_future_work_maps_to_future_directions():

    evidence = FakeGapEvidence(
        evidence_id="E20",
        paper_id="09_hits",
        page_number=10,
        section="conclusion",
        text=("Extending the dataset remains " "part of future work."),
        citation_text=("HITS (2024), p. 10"),
        signal_type="future_work",
    )

    aggregation = LiteratureReviewEvidenceAggregator().aggregate(
        query="Review future work.",
        paper_ids=[
            "09_hits",
        ],
        dimension_evidence=[],
        explicit_gap_evidence=[evidence],
    )

    bundle = get_bundle(
        aggregation,
        LiteratureReviewSectionType.FUTURE_DIRECTIONS,
    )

    assert bundle.evidence[0].paper_id == "09_hits"


def test_unresolved_problem_maps_to_two_sections():

    evidence = FakeGapEvidence(
        evidence_id="E30",
        paper_id="10_coding_before_testing",
        page_number=8,
        section="results",
        text=("Oracle correctness remains " "an unresolved concern."),
        citation_text=("Coding Before Testing (2026), p. 8"),
        signal_type="unresolved_problem",
    )

    aggregation = LiteratureReviewEvidenceAggregator().aggregate(
        query="Review unresolved problems.",
        paper_ids=[
            "10_coding_before_testing",
        ],
        dimension_evidence=[],
        explicit_gap_evidence=[evidence],
    )

    section_types = {bundle.section_type for bundle in aggregation.bundles}

    assert LiteratureReviewSectionType.LIMITATIONS_AND_GAPS in section_types

    assert LiteratureReviewSectionType.FUTURE_DIRECTIONS in section_types


def test_duplicate_evidence_is_removed_within_section():

    evidence = FakeDimensionEvidence(
        evidence_id="E1",
        paper_id="03_mutap",
        page_number=5,
        section="methodology",
        text="Mutation feedback is used.",
        citation_text="MuTAP (2023), p. 5",
        dimension="generation_strategy",
    )

    aggregation = LiteratureReviewEvidenceAggregator().aggregate(
        query="Review test generation.",
        paper_ids=[
            "03_mutap",
        ],
        dimension_evidence=[
            evidence,
            evidence,
        ],
        explicit_gap_evidence=[],
    )

    bundle = get_bundle(
        aggregation,
        LiteratureReviewSectionType.GENERATION_STRATEGIES,
    )

    assert len(bundle.evidence) == 1


def test_same_evidence_can_exist_in_different_sections():

    evidence = FakeDimensionEvidence(
        evidence_id="E1",
        paper_id="03_mutap",
        page_number=5,
        section="methodology",
        text="Mutation feedback is used.",
        citation_text="MuTAP (2023), p. 5",
        dimension="generation_strategy",
    )

    aggregation = LiteratureReviewEvidenceAggregator().aggregate(
        query="Review test generation.",
        paper_ids=[
            "03_mutap",
        ],
        dimension_evidence=[evidence],
        explicit_gap_evidence=[],
    )

    landscape = get_bundle(
        aggregation,
        LiteratureReviewSectionType.RESEARCH_LANDSCAPE,
    )

    strategies = get_bundle(
        aggregation,
        LiteratureReviewSectionType.GENERATION_STRATEGIES,
    )

    assert landscape.evidence[0].evidence_id == "E1"

    assert strategies.evidence[0].evidence_id == "E1"


def test_evidence_from_unrequested_paper_is_excluded():

    evidence = FakeDimensionEvidence(
        evidence_id="E1",
        paper_id="05_coverup",
        page_number=4,
        section="methodology",
        text="Coverage feedback is used.",
        citation_text="CoverUp (2025), p. 4",
        dimension="feedback_signal",
    )

    aggregation = LiteratureReviewEvidenceAggregator().aggregate(
        query="Review MuTAP.",
        paper_ids=[
            "03_mutap",
        ],
        dimension_evidence=[evidence],
        explicit_gap_evidence=[],
    )

    assert aggregation.bundles == []


def test_paper_order_is_preserved_and_duplicates_removed():

    aggregation = LiteratureReviewEvidenceAggregator().aggregate(
        query="Review papers.",
        paper_ids=[
            "03_mutap",
            "05_coverup",
            "03_mutap",
        ],
        dimension_evidence=[],
        explicit_gap_evidence=[],
    )

    assert aggregation.paper_ids == [
        "03_mutap",
        "05_coverup",
    ]


def test_empty_query_is_rejected():

    aggregator = LiteratureReviewEvidenceAggregator()

    try:
        aggregator.aggregate(
            query="   ",
            paper_ids=[
                "03_mutap",
            ],
            dimension_evidence=[],
            explicit_gap_evidence=[],
        )

        assert False

    except ValueError as exc:

        assert "query" in str(exc)
