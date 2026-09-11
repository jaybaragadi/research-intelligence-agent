from src.analysis.evidence_classifier import EvidenceDimensionClassifier
from src.generation.models import GroundingEvidence


def make_evidence(
    text: str,
    section: str | None = "methodology",
):
    return GroundingEvidence(
        evidence_id="05_coverup_chunk_0001",
        label="E1",
        paper_id="05_coverup",
        page_number=2,
        section=section,
        text=text,
        citation_text="Citation",
    )


def get_dimensions(
    text: str,
    section: str | None = "methodology",
) -> set[str]:
    evidence = make_evidence(
        text=text,
        section=section,
    )

    results = EvidenceDimensionClassifier().classify(evidence)

    return {result.dimension for result in results}


def test_classifies_feedback_evidence():
    dimensions = get_dimensions(
        (
            "Coverage feedback is added to "
            "the prompt before generating "
            "another test."
        )
    )

    assert "feedback_signal" in dimensions


def test_evidence_can_match_multiple_dimensions():
    dimensions = get_dimensions(
        (
            "The system iteratively uses "
            "coverage feedback to improve "
            "generated tests."
        )
    )

    assert "feedback_signal" in dimensions
    assert "iteration_strategy" in dimensions
    assert "quality_objective" in dimensions


def test_irrelevant_evidence_returns_no_dimensions():
    dimensions = get_dimensions(
        "The paper was published in 2025.",
        section=None,
    )

    assert dimensions == set()


def test_relevance_score_is_preserved():
    evidence = make_evidence(
        "Mutation testing uses surviving mutants as feedback."
    )

    results = EvidenceDimensionClassifier().classify(evidence)

    feedback = next(
        result
        for result in results
        if result.dimension == "feedback_signal"
    )

    assert feedback.relevance_score > 0


def test_failure_alone_is_not_limitation():
    dimensions = get_dimensions(
        "The generated test failed during execution."
    )

    assert "limitations" not in dimensions


def test_limitation_language_is_classified():
    dimensions = get_dimensions(
        (
            "A limitation of the approach "
            "is its dependence on execution feedback."
        )
    )

    assert "limitations" in dimensions


def test_coverage_alone_is_not_feedback_signal_via_dimensions():
    dimensions = get_dimensions(
        "Code coverage is weakly correlated with bug detection.",
        section=None,
    )

    assert "feedback_signal" not in dimensions


def test_surviving_mutants_are_feedback_signal_via_dimensions():
    dimensions = get_dimensions(
        (
            "The method augments prompts with "
            "surviving mutants to expose "
            "weaknesses in generated tests."
        )
    )

    assert "feedback_signal" in dimensions


def test_improvement_alone_is_not_iteration_via_dimensions():
    dimensions = get_dimensions(
        "The proposed approach improves the effectiveness of generated tests."
    )

    assert "iteration_strategy" not in dimensions


def test_test_case_limitation_is_not_method_limitation_via_dimensions():
    dimensions = get_dimensions(
        (
            "Surviving mutants highlight the "
            "limitations of test cases in detecting bugs."
        )
    )

    assert "limitations" not in dimensions


def test_coverage_alone_is_not_feedback_signal_with_evidence_object():
    evidence = make_evidence(
        "Code coverage is weakly correlated with bug detection."
    )

    results = EvidenceDimensionClassifier().classify(evidence)

    dimensions = {result.dimension for result in results}

    assert "feedback_signal" not in dimensions


def test_surviving_mutants_are_feedback_signal_with_evidence_object():
    evidence = make_evidence(
        (
            "The method augments prompts with "
            "surviving mutants to expose weaknesses "
            "in generated tests."
        )
    )

    results = EvidenceDimensionClassifier().classify(evidence)

    dimensions = {result.dimension for result in results}

    assert "feedback_signal" in dimensions


def test_improvement_alone_is_not_iteration_with_evidence_object():
    evidence = make_evidence(
        "The proposed approach improves the effectiveness of generated tests."
    )

    results = EvidenceDimensionClassifier().classify(evidence)

    dimensions = {result.dimension for result in results}

    assert "iteration_strategy" not in dimensions


def test_test_case_limitation_is_not_method_limitation_with_evidence_object():
    evidence = make_evidence(
        (
            "Surviving mutants highlight the "
            "limitations of test cases in detecting bugs."
        )
    )

    results = EvidenceDimensionClassifier().classify(evidence)

    dimensions = {result.dimension for result in results}

    assert "limitations" not in dimensions