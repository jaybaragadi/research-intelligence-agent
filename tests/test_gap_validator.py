from src.analysis.gap_models import (
    GapCandidate,
    GapConfidence,
    GapType,
)
from src.analysis.gap_validator import (
    GapValidator,
)


def make_candidate(
    gap_id: str = "G1",
    gap_type: GapType = GapType.EXPLICIT,
    paper_ids: list[str] | None = None,
    evidence_ids: list[str] | None = None,
    dimensions: list[str] | None = None,
) -> GapCandidate:

    return GapCandidate(
        gap_id=gap_id,
        gap_type=gap_type,
        title="Candidate gap",
        description=("Evidence-grounded candidate."),
        confidence=(GapConfidence.MEDIUM),
        paper_ids=(paper_ids if paper_ids is not None else ["paper_a"]),
        evidence_ids=(evidence_ids if evidence_ids is not None else ["e1"]),
        dimensions=(dimensions if dimensions is not None else []),
        reason=("Supported by indexed corpus evidence."),
    )


def test_valid_explicit_candidate_passes():

    result = GapValidator().validate(
        candidates=[make_candidate()],
        available_evidence_ids={"e1"},
    )

    assert result.is_valid is True

    assert result.validated_gap_count == 1

    assert result.issue_count == 0


def test_unknown_evidence_is_rejected():

    result = GapValidator().validate(
        candidates=[make_candidate(evidence_ids=["missing"])],
        available_evidence_ids={"e1"},
    )

    assert result.is_valid is False

    assert any(issue.issue_type == "unknown_evidence_id" for issue in result.issues)


def test_explicit_candidate_requires_evidence():

    result = GapValidator().validate(
        candidates=[make_candidate(evidence_ids=[])],
        available_evidence_ids=set(),
    )

    assert result.is_valid is False

    assert any(
        issue.issue_type == "explicit_gap_without_evidence" for issue in result.issues
    )


def test_explicit_candidate_requires_paper():

    result = GapValidator().validate(
        candidates=[make_candidate(paper_ids=[])],
        available_evidence_ids={"e1"},
    )

    assert result.is_valid is False

    assert any(
        issue.issue_type == "explicit_gap_without_paper" for issue in result.issues
    )


def test_duplicate_gap_ids_are_rejected():

    result = GapValidator().validate(
        candidates=[
            make_candidate(
                gap_id="G1",
                evidence_ids=["e1"],
            ),
            make_candidate(
                gap_id="G1",
                evidence_ids=["e2"],
            ),
        ],
        available_evidence_ids={
            "e1",
            "e2",
        },
    )

    assert result.is_valid is False

    assert any(issue.issue_type == "duplicate_gap_id" for issue in result.issues)


def test_duplicate_evidence_ids_are_rejected():

    result = GapValidator().validate(
        candidates=[
            make_candidate(
                evidence_ids=[
                    "e1",
                    "e1",
                ]
            )
        ],
        available_evidence_ids={"e1"},
    )

    assert result.is_valid is False

    assert any(issue.issue_type == "duplicate_evidence_id" for issue in result.issues)


def test_valid_imbalance_candidate_passes():

    candidate = make_candidate(
        gap_id="CI1",
        gap_type=(GapType.CORPUS_IMBALANCE),
        paper_ids=[
            "paper_a",
            "paper_b",
        ],
        evidence_ids=[
            "e1",
            "e2",
        ],
        dimensions=[
            "quality_objective",
            "limitations",
        ],
    )

    result = GapValidator().validate(
        candidates=[candidate],
        available_evidence_ids={
            "e1",
            "e2",
        },
    )

    assert result.is_valid is True

    assert result.validated_gap_count == 1


def test_imbalance_requires_two_dimensions():

    candidate = make_candidate(
        gap_id="CI1",
        gap_type=(GapType.CORPUS_IMBALANCE),
        dimensions=["limitations"],
    )

    result = GapValidator().validate(
        candidates=[candidate],
        available_evidence_ids={"e1"},
    )

    assert result.is_valid is False

    assert any(
        issue.issue_type == "imbalance_requires_two_dimensions"
        for issue in result.issues
    )


def test_insufficient_evidence_cannot_claim_support():

    candidate = make_candidate(
        gap_id="IE1",
        gap_type=(GapType.INSUFFICIENT_EVIDENCE),
        evidence_ids=["e1"],
    )

    result = GapValidator().validate(
        candidates=[candidate],
        available_evidence_ids={"e1"},
    )

    assert result.is_valid is False

    assert any(
        issue.issue_type == "insufficient_evidence_has_support"
        for issue in result.issues
    )


def test_empty_candidate_list_is_valid():

    result = GapValidator().validate(
        candidates=[],
        available_evidence_ids=set(),
    )

    assert result.is_valid is True

    assert result.validated_gap_count == 0

    assert result.issue_count == 0
