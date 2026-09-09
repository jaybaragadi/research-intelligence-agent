from src.generation.grounding_validator import (
    GroundingValidator,
)

from src.generation.models import (
    EvidencePackage,
    GeneratedClaim,
    GeneratedDraft,
    GroundingEvidence,
)


def make_package():

    return EvidencePackage(
        query="question",

        evidence=[
            GroundingEvidence(
                evidence_id=(
                    "paper_a_chunk_0001"
                ),

                label="E1",

                paper_id="paper_a",

                page_number=3,

                section="methodology",

                text="Evidence",

                citation_text="Citation",
            )
        ],
    )


def test_valid_claim_passes():

    draft = GeneratedDraft(
        query="question",

        answer_text="Supported answer",

        claims=[
            GeneratedClaim(
                claim_id="C1",

                text="Supported claim",

                evidence_ids=[
                    "paper_a_chunk_0001"
                ],
            )
        ],
    )

    result = (
        GroundingValidator()
        .validate(
            draft,
            make_package(),
        )
    )

    assert result.is_valid

    assert (
        result.validated_claim_count
        == 1
    )


def test_claim_without_evidence_fails():

    draft = GeneratedDraft(
        query="question",

        answer_text="answer",

        claims=[
            GeneratedClaim(
                claim_id="C1",

                text="Unsupported claim",

                evidence_ids=[],
            )
        ],
    )

    result = (
        GroundingValidator()
        .validate(
            draft,
            make_package(),
        )
    )

    assert not result.is_valid

    assert (
        result.issues[0].issue_type
        == "missing_evidence"
    )


def test_unknown_evidence_fails():

    draft = GeneratedDraft(
        query="question",

        answer_text="answer",

        claims=[
            GeneratedClaim(
                claim_id="C1",

                text="Claim",

                evidence_ids=[
                    "fake_chunk_9999"
                ],
            )
        ],
    )

    result = (
        GroundingValidator()
        .validate(
            draft,
            make_package(),
        )
    )

    assert not result.is_valid

    assert (
        result.issues[0].issue_type
        == "unknown_evidence"
    )


def test_duplicate_claim_id_fails():

    draft = GeneratedDraft(
        query="question",

        answer_text="answer",

        claims=[
            GeneratedClaim(
                claim_id="C1",

                text="Claim one",

                evidence_ids=[
                    "paper_a_chunk_0001"
                ],
            ),

            GeneratedClaim(
                claim_id="C1",

                text="Claim two",

                evidence_ids=[
                    "paper_a_chunk_0001"
                ],
            ),
        ],
    )

    result = (
        GroundingValidator()
        .validate(
            draft,
            make_package(),
        )
    )

    assert not result.is_valid

    assert any(
        issue.issue_type
        == "duplicate_claim_id"

        for issue
        in result.issues
    )