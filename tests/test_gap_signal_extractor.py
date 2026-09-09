from src.analysis.gap_models import (
    GapSignalType,
)

from src.analysis.gap_signal_extractor import (
    ExplicitGapSignalExtractor,
)

from src.generation.models import (
    GroundingEvidence,
)


def make_evidence(
    text: str,
    section: str | None = "discussion",
    evidence_id: str = "paper_chunk_0001",
):

    return GroundingEvidence(
        evidence_id=evidence_id,

        label="E1",

        paper_id="paper_01",

        page_number=5,

        section=section,

        text=text,

        citation_text="Paper citation",
    )


def signal_types(
    text: str,
    section: str | None = "discussion",
) -> set[GapSignalType]:

    evidence = make_evidence(
        text=text,
        section=section,
    )

    results = (
        ExplicitGapSignalExtractor()
        .extract(
            evidence
        )
    )

    return {
        result.signal_type
        for result in results
    }


def test_extracts_explicit_limitation():

    signals = signal_types(
        (
            "A limitation of our approach "
            "is the restricted evaluation scope."
        )
    )

    assert (
        GapSignalType.LIMITATION
        in signals
    )


def test_extracts_future_work():

    signals = signal_types(
        (
            "In future work, we plan to investigate "
            "additional programming languages."
        ),
        section="conclusion",
    )

    assert (
        GapSignalType.FUTURE_WORK
        in signals
    )


def test_extracts_unresolved_problem():

    signals = signal_types(
        (
            "Generating high-quality tests for "
            "complex branches remains challenging."
        ),
        section="introduction",
    )

    assert (
        GapSignalType.UNRESOLVED_PROBLEM
        in signals
    )


def test_generic_failure_is_not_gap_signal():

    signals = signal_types(
        (
            "The generated test failed "
            "during execution."
        )
    )

    assert signals == set()


def test_generic_limited_word_is_not_gap_signal():

    signals = signal_types(
        (
            "The method achieved limited "
            "branch coverage."
        )
    )

    assert signals == set()


def test_preserves_provenance():

    evidence = make_evidence(
        (
            "Future work will investigate "
            "additional datasets."
        ),
        section="conclusion",
        evidence_id=(
            "08_telpa_chunk_0042"
        ),
    )

    results = (
        ExplicitGapSignalExtractor()
        .extract(
            evidence
        )
    )

    assert len(results) == 1

    result = results[0]

    assert (
        result.evidence_id
        == "08_telpa_chunk_0042"
    )

    assert (
        result.paper_id
        == "paper_01"
    )

    assert (
        result.page_number
        == 5
    )


def test_section_bonus_increases_score():

    extractor = (
        ExplicitGapSignalExtractor()
    )

    text = (
        "Future work will investigate "
        "additional datasets."
    )

    preferred = extractor.extract(
        make_evidence(
            text,
            section="conclusion",
        )
    )

    nonpreferred = extractor.extract(
        make_evidence(
            text,
            section="methodology",
        )
    )

    assert (
        preferred[0].relevance_score
        >
        nonpreferred[0].relevance_score
    )


def test_one_passage_can_produce_multiple_signals():

    signals = signal_types(
        (
            "A limitation of our approach "
            "is its restricted dataset. "
            "In future work, we plan to investigate "
            "larger and more diverse benchmarks."
        )
    )

    assert (
        GapSignalType.LIMITATION
        in signals
    )

    assert (
        GapSignalType.FUTURE_WORK
        in signals
    )


def test_future_work_accepts_planned_research_action():

    evidence = make_evidence(
        text=(
            "In future work, we plan to "
            "investigate additional programming "
            "languages."
        ),
        section="conclusion",
    )

    extractor = (
        ExplicitGapSignalExtractor()
    )

    signals = extractor.extract(
        evidence
    )

    assert any(
        signal.signal_type
        == GapSignalType.FUTURE_WORK
        for signal
        in signals
    )

def test_future_work_accepts_exploration_direction():

    evidence = make_evidence(
        text=(
            "Future work can explore techniques "
            "to improve generated test oracles."
        ),
        section="conclusion",
    )

    extractor = (
        ExplicitGapSignalExtractor()
    )

    signals = extractor.extract(
        evidence
    )

    assert any(
        signal.signal_type
        == GapSignalType.FUTURE_WORK
        for signal
        in signals
    )

def test_future_work_accepts_remaining_research_action():

    evidence = make_evidence(
        text=(
            "Finding ways to extend the dataset "
            "and tested LLMs remains part of "
            "our future work."
        ),
        section="conclusion",
    )

    extractor = (
        ExplicitGapSignalExtractor()
    )

    signals = extractor.extract(
        evidence
    )

    assert any(
        signal.signal_type
        == GapSignalType.FUTURE_WORK
        for signal
        in signals
    )

def test_future_work_rejects_document_navigation():

    evidence = make_evidence(
        text=(
            "Finally, we conclude the paper in "
            "Section 8, highlighting some avenues "
            "for future works."
        ),
        section="introduction",
    )

    extractor = (
        ExplicitGapSignalExtractor()
    )

    signals = extractor.extract(
        evidence
    )

    assert not any(
        signal.signal_type
        == GapSignalType.FUTURE_WORK
        for signal
        in signals
    )

def test_future_work_rejects_future_research_enablement():

    evidence = make_evidence(
        text=(
            "We released our implementation "
            "and experimental data to facilitate "
            "replication, future research, and "
            "practical use."
        ),
        section="evaluation",
    )

    extractor = (
        ExplicitGapSignalExtractor()
    )

    signals = extractor.extract(
        evidence
    )

    assert not any(
        signal.signal_type
        == GapSignalType.FUTURE_WORK
        for signal
        in signals
    )

def test_same_evidence_can_produce_limitation_and_future_work():

    evidence = make_evidence(
        text=(
            "A limitation of our approach is "
            "the restricted dataset. Finding "
            "ways to extend the dataset remains "
            "part of our future work."
        ),
        section="conclusion",
    )

    extractor = (
        ExplicitGapSignalExtractor()
    )

    signals = extractor.extract(
        evidence
    )

    signal_types = {
        signal.signal_type
        for signal
        in signals
    }

    assert (
        GapSignalType.LIMITATION
        in signal_types
    )

    assert (
        GapSignalType.FUTURE_WORK
        in signal_types
    )