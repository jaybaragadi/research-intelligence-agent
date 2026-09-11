import pytest

from src.analysis.literature_review_generator import (
    DeterministicLiteratureReviewGenerator,
)
from src.analysis.literature_review_models import (
    LiteratureReviewEvidence,
    LiteratureReviewEvidenceAggregation,
    LiteratureReviewEvidenceBundle,
    LiteratureReviewSectionType,
    LiteratureReviewSynthesis,
    LiteratureReviewSynthesisFinding,
)


def make_evidence(
    evidence_id: str,
    paper_id: str,
    citation_text: str | None = None,
) -> LiteratureReviewEvidence:

    return LiteratureReviewEvidence(
        evidence_id=evidence_id,
        paper_id=paper_id,
        page_number=1,
        section="methodology",
        text="Evidence text.",
        citation_text=(citation_text or f"{paper_id}, p. 1"),
    )


def get_section(
    review,
    section_type,
):

    return next(
        section for section in review.sections if section.section_type == section_type
    )


def test_generator_creates_all_taxonomy_sections():

    aggregation = LiteratureReviewEvidenceAggregation(
        query="Review LLM test generation.",
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
        bundles=[],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[],
    )

    review = DeterministicLiteratureReviewGenerator().generate(
        aggregation,
        synthesis,
    )

    section_types = [section.section_type for section in review.sections]

    assert LiteratureReviewSectionType.INTRODUCTION in section_types

    assert LiteratureReviewSectionType.GENERATION_STRATEGIES in section_types

    assert LiteratureReviewSectionType.FUTURE_DIRECTIONS in section_types

    assert LiteratureReviewSectionType.CONCLUSION in section_types


def test_finding_becomes_section_narrative():

    evidence = make_evidence(
        "E1",
        "03_mutap",
    )

    aggregation = LiteratureReviewEvidenceAggregation(
        query="Review feedback.",
        paper_ids=[
            "03_mutap",
        ],
        bundles=[
            LiteratureReviewEvidenceBundle(
                section_type=(LiteratureReviewSectionType.FEEDBACK_AND_ITERATION),
                evidence=[evidence],
            )
        ],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[
            LiteratureReviewSynthesisFinding(
                finding_id="SF1",
                section_type=(LiteratureReviewSectionType.FEEDBACK_AND_ITERATION),
                statement=(
                    "The indexed study incorporates " "feedback into test generation."
                ),
                paper_ids=["03_mutap"],
                evidence_ids=["E1"],
                support_count=1,
                is_cross_paper=False,
            )
        ],
    )

    review = DeterministicLiteratureReviewGenerator().generate(
        aggregation,
        synthesis,
    )

    section = get_section(
        review,
        LiteratureReviewSectionType.FEEDBACK_AND_ITERATION,
    )

    assert "incorporates feedback" in section.narrative

    assert "[E1]" in section.narrative


def test_multiple_evidence_ids_are_rendered():

    aggregation = LiteratureReviewEvidenceAggregation(
        query="Review evaluation.",
        paper_ids=[
            "01_testpilot",
            "05_coverup",
        ],
        bundles=[],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[
            LiteratureReviewSynthesisFinding(
                finding_id="SF1",
                section_type=(LiteratureReviewSectionType.QUALITY_AND_EVALUATION),
                statement=("Multiple indexed studies " "evaluate generated tests."),
                paper_ids=[
                    "01_testpilot",
                    "05_coverup",
                ],
                evidence_ids=[
                    "E1",
                    "E2",
                ],
                support_count=2,
                is_cross_paper=True,
            )
        ],
    )

    review = DeterministicLiteratureReviewGenerator().generate(
        aggregation,
        synthesis,
    )

    section = get_section(
        review,
        LiteratureReviewSectionType.QUALITY_AND_EVALUATION,
    )

    assert "[E1; E2]" in section.narrative


def test_duplicate_marker_ids_are_removed():

    generator = DeterministicLiteratureReviewGenerator()

    marker = generator._evidence_marker(
        [
            "E1",
            "E1",
            "E2",
        ]
    )

    assert marker == "[E1; E2]"


def test_introduction_reports_indexed_paper_count():

    aggregation = LiteratureReviewEvidenceAggregation(
        query="Review research.",
        paper_ids=[
            "01_testpilot",
            "03_mutap",
            "05_coverup",
        ],
        bundles=[],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[],
    )

    review = DeterministicLiteratureReviewGenerator().generate(
        aggregation,
        synthesis,
    )

    introduction = get_section(
        review,
        LiteratureReviewSectionType.INTRODUCTION,
    )

    assert "3 papers" in introduction.narrative

    assert "indexed corpus" in introduction.narrative


def test_single_paper_uses_singular_wording():

    aggregation = LiteratureReviewEvidenceAggregation(
        query="Review research.",
        paper_ids=[
            "03_mutap",
        ],
        bundles=[],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[],
    )

    review = DeterministicLiteratureReviewGenerator().generate(
        aggregation,
        synthesis,
    )

    introduction = get_section(
        review,
        LiteratureReviewSectionType.INTRODUCTION,
    )

    assert "1 paper " in introduction.narrative


def test_empty_future_work_section_does_not_claim_no_research_exists():

    aggregation = LiteratureReviewEvidenceAggregation(
        query="Review future work.",
        paper_ids=[
            "03_mutap",
        ],
        bundles=[],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[],
    )

    review = DeterministicLiteratureReviewGenerator().generate(
        aggregation,
        synthesis,
    )

    section = get_section(
        review,
        LiteratureReviewSectionType.FUTURE_DIRECTIONS,
    )

    text = section.narrative.lower()

    assert "no qualifying" in text

    assert "current evidence aggregation" in text

    assert "no researchers" not in text


def test_citations_are_deduplicated_across_sections():

    shared = make_evidence(
        "E1",
        "03_mutap",
        citation_text=("MuTAP (2023), p. 5"),
    )

    aggregation = LiteratureReviewEvidenceAggregation(
        query="Review research.",
        paper_ids=[
            "03_mutap",
        ],
        bundles=[
            LiteratureReviewEvidenceBundle(
                section_type=(LiteratureReviewSectionType.RESEARCH_LANDSCAPE),
                evidence=[shared],
            ),
            LiteratureReviewEvidenceBundle(
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                evidence=[shared],
            ),
        ],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[],
    )

    review = DeterministicLiteratureReviewGenerator().generate(
        aggregation,
        synthesis,
    )

    assert review.citations == ["MuTAP (2023), p. 5"]


def test_generator_preserves_evidence_in_section():

    evidence = make_evidence(
        "E1",
        "05_coverup",
    )

    aggregation = LiteratureReviewEvidenceAggregation(
        query="Review strategies.",
        paper_ids=[
            "05_coverup",
        ],
        bundles=[
            LiteratureReviewEvidenceBundle(
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                evidence=[evidence],
            )
        ],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[],
    )

    review = DeterministicLiteratureReviewGenerator().generate(
        aggregation,
        synthesis,
    )

    section = get_section(
        review,
        LiteratureReviewSectionType.GENERATION_STRATEGIES,
    )

    assert section.evidence[0].evidence_id == "E1"


def test_mismatched_queries_are_rejected():

    aggregation = LiteratureReviewEvidenceAggregation(
        query="Query A",
        paper_ids=["03_mutap"],
        bundles=[],
    )

    synthesis = LiteratureReviewSynthesis(
        query="Query B",
        paper_ids=["03_mutap"],
        findings=[],
    )

    with pytest.raises(
        ValueError,
        match="same query",
    ):
        (
            DeterministicLiteratureReviewGenerator().generate(
                aggregation,
                synthesis,
            )
        )


def test_mismatched_paper_ids_are_rejected():

    aggregation = LiteratureReviewEvidenceAggregation(
        query="Review research.",
        paper_ids=["03_mutap"],
        bundles=[],
    )

    synthesis = LiteratureReviewSynthesis(
        query="Review research.",
        paper_ids=["05_coverup"],
        findings=[],
    )

    with pytest.raises(
        ValueError,
        match="same paper_ids",
    ):
        (
            DeterministicLiteratureReviewGenerator().generate(
                aggregation,
                synthesis,
            )
        )


def test_blank_title_uses_default():

    aggregation = LiteratureReviewEvidenceAggregation(
        query="Review research.",
        paper_ids=["03_mutap"],
        bundles=[],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[],
    )

    review = DeterministicLiteratureReviewGenerator().generate(
        aggregation,
        synthesis,
        title="   ",
    )

    assert review.title == "Evidence-Grounded Literature Review"
