from src.analysis.comparison_models import (
    DimensionEvidence,
)
from src.analysis.dimension_summary import (
    DimensionSummarySelector,
)


def make_evidence(
    text: str,
    evidence_id: str = "e1",
):

    return DimensionEvidence(
        evidence_id=evidence_id,
        paper_id="03_mutap",
        dimension="feedback_signal",
        page_number=1,
        section="methodology",
        text=text,
        citation_text="Citation",
        relevance_score=3.0,
    )


def test_selects_dimension_specific_sentence():

    evidence = [
        make_evidence(
            (
                "The approach was evaluated "
                "on multiple benchmarks. "
                "Surviving mutants are used "
                "as feedback to improve tests."
            )
        )
    ]

    summary, ids = DimensionSummarySelector().select(
        dimension="feedback_signal",
        evidence=evidence,
    )

    assert summary == ("Surviving mutants are used " "as feedback to improve tests.")

    assert ids == ["e1"]


def test_returns_exact_source_id():

    evidence = [
        make_evidence(
            ("Coverage feedback guides " "subsequent test generation."),
            evidence_id="coverup_1",
        )
    ]

    _, ids = DimensionSummarySelector().select(
        dimension="feedback_signal",
        evidence=evidence,
    )

    assert ids == ["coverup_1"]


def test_returns_none_when_no_dimension_match():

    evidence = [make_evidence("The paper was published in 2025.")]

    summary, ids = DimensionSummarySelector().select(
        dimension="feedback_signal",
        evidence=evidence,
    )

    assert summary is None
    assert ids == []
