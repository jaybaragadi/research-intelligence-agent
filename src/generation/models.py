from dataclasses import (
    dataclass,
    field,
)


@dataclass
class GroundingEvidence:
    """
    One validated evidence passage available
    to the answer generator.

    The evidence has already passed through
    EvidenceTool and CitationTool.
    """

    evidence_id: str

    label: str

    paper_id: str

    page_number: int

    section: str | None

    text: str

    citation_text: str


@dataclass
class EvidencePackage:
    """
    Complete evidence context supplied to an
    answer generator.

    The generator must not use evidence outside
    this package.
    """

    query: str

    evidence: list[GroundingEvidence] = field(default_factory=list)


@dataclass
class GeneratedClaim:
    """
    One answer claim and the exact evidence
    identifiers supporting it.
    """

    claim_id: str

    text: str

    evidence_ids: list[str] = field(default_factory=list)


@dataclass
class GeneratedDraft:
    """
    Candidate answer produced by a generator
    before grounding validation.
    """

    query: str

    answer_text: str

    claims: list[GeneratedClaim] = field(default_factory=list)


@dataclass
class GroundingIssue:
    """
    One grounding validation failure.
    """

    issue_type: str

    message: str

    claim_id: str | None = None

    evidence_id: str | None = None


@dataclass
class GroundingValidationResult:
    """
    Result of validating a candidate draft
    against its evidence package.
    """

    is_valid: bool

    validated_claim_count: int

    issue_count: int

    issues: list[GroundingIssue] = field(default_factory=list)


@dataclass
class GroundedAnswer:
    """
    Final Phase 8 response.

    This object is returned only after the
    candidate draft has been checked against
    the validated evidence package.
    """

    query: str

    answer_text: str

    claims: list[GeneratedClaim]

    evidence: list[GroundingEvidence]

    validation: GroundingValidationResult
