import pytest

from src.generation.deterministic_generator import (
    DeterministicGroundedGenerator,
)
from src.generation.models import (
    EvidencePackage,
    GroundingEvidence,
)


def make_evidence(
    evidence_id: str,
    label: str,
    text: str,
):

    return GroundingEvidence(
        evidence_id=evidence_id,
        label=label,
        paper_id="paper_a",
        page_number=3,
        section="methodology",
        text=text,
        citation_text="Citation",
    )


def test_generator_creates_grounded_claim():

    package = EvidencePackage(
        query="How is feedback used?",
        evidence=[
            make_evidence(
                "paper_a_chunk_0001",
                "E1",
                ("Feedback improves the " "generated test. More text."),
            )
        ],
    )

    draft = DeterministicGroundedGenerator().generate(package)

    assert len(draft.claims) == 1

    assert draft.claims[0].evidence_ids == ["paper_a_chunk_0001"]

    assert "[E1]" in draft.answer_text


def test_generator_limits_claim_count():

    package = EvidencePackage(
        query="evidence sentence",
        evidence=[
            make_evidence(
                f"paper_a_chunk_{index:04d}",
                f"E{index}",
                f"Evidence sentence {index}.",
            )
            for index in range(
                1,
                6,
            )
        ],
    )

    draft = DeterministicGroundedGenerator(max_claims=2).generate(package)

    assert len(draft.claims) == 2


def test_generator_handles_no_evidence():

    draft = DeterministicGroundedGenerator().generate(
        EvidencePackage(
            query="question",
            evidence=[],
        )
    )

    assert draft.claims == []

    assert "No validated evidence" in draft.answer_text


def test_generator_rejects_empty_query():

    with pytest.raises(ValueError):

        (
            DeterministicGroundedGenerator().generate(
                EvidencePackage(
                    query="   ",
                    evidence=[],
                )
            )
        )


def test_generator_selects_query_relevant_sentence():

    package = EvidencePackage(
        query=("How is iterative feedback used?"),
        evidence=[
            make_evidence(
                "paper_a_chunk_0001",
                "E1",
                (
                    "The framework was evaluated "
                    "on Python programs. "
                    "Iterative feedback is used "
                    "to improve generated tests."
                ),
            )
        ],
    )

    draft = DeterministicGroundedGenerator().generate(package)

    assert draft.claims[0].text == (
        "Iterative feedback is used " "to improve generated tests."
    )


def test_generator_ignores_zero_overlap_evidence():

    package = EvidencePackage(
        query=("How is iterative feedback used?"),
        evidence=[
            make_evidence(
                "paper_a_chunk_0001",
                "E1",
                ("The experiment uses " "Python version 3.10."),
            )
        ],
    )

    draft = DeterministicGroundedGenerator().generate(package)

    assert draft.claims == []


def test_generator_rejects_generic_domain_language():

    package = EvidencePackage(
        query=("How do LLM-based testing " "approaches use iterative feedback?"),
        evidence=[
            make_evidence(
                "paper_a_chunk_0001",
                "E1",
                (
                    "LLM-based test generation "
                    "was evaluated using several "
                    "software benchmarks."
                ),
            ),
            make_evidence(
                "paper_a_chunk_0002",
                "E2",
                (
                    "Compilation feedback is "
                    "used to refine invalid "
                    "generated tests."
                ),
            ),
        ],
    )

    draft = DeterministicGroundedGenerator().generate(package)

    assert len(draft.claims) == 1

    assert draft.claims[0].evidence_ids == ["paper_a_chunk_0002"]


def test_generator_ignores_front_matter_contaminated_sentence():

    package = EvidencePackage(
        query=(
            "How are Large Language Models being used "
            "to improve automated software test generation?"
        ),
        evidence=[
            make_evidence(
                "paper_a_chunk_0001",
                "E1",
                (
                    "An Empirical Evaluation of Using Large Language Models "
                    "for Automated Unit Test Generation Max Author, Jane Author "
                    "Abstract—Unit tests play a key role in ensuring the "
                    "correctness of software."
                ),
            ),
            make_evidence(
                "paper_a_chunk_0002",
                "E2",
                (
                    "Large language models are used with iterative feedback "
                    "to improve generated tests and correct invalid outputs."
                ),
            ),
        ],
    )

    draft = DeterministicGroundedGenerator().generate(package)

    assert len(draft.claims) == 1
    assert draft.claims[0].evidence_ids == ["paper_a_chunk_0002"]
    assert "Abstract" not in draft.claims[0].text
