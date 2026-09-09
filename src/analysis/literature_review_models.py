from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class LiteratureReviewSectionType(str, Enum):
    INTRODUCTION = "introduction"

    RESEARCH_LANDSCAPE = "research_landscape"

    GENERATION_STRATEGIES = "generation_strategies"

    FEEDBACK_AND_ITERATION = "feedback_and_iteration"

    QUALITY_AND_EVALUATION = "quality_and_evaluation"

    LIMITATIONS_AND_GAPS = "limitations_and_gaps"

    FUTURE_DIRECTIONS = "future_directions"

    CONCLUSION = "conclusion"


@dataclass(frozen=True)
class LiteratureReviewEvidence:
    evidence_id: str
    paper_id: str
    page_number: int
    section: str | None
    text: str
    citation_text: str


@dataclass
class LiteratureReviewFinding:
    finding_id: str

    section_type: LiteratureReviewSectionType

    statement: str

    paper_ids: list[str] = field(
        default_factory=list
    )

    evidence_ids: list[str] = field(
        default_factory=list
    )


@dataclass
class LiteratureReviewSynthesisFinding:
    finding_id: str

    section_type: LiteratureReviewSectionType

    statement: str

    paper_ids: list[str] = field(
        default_factory=list
    )

    evidence_ids: list[str] = field(
        default_factory=list
    )

    support_count: int = 0

    is_cross_paper: bool = False


@dataclass
class LiteratureReviewSynthesis:
    query: str

    paper_ids: list[str]

    findings: list[
        LiteratureReviewSynthesisFinding
    ] = field(
        default_factory=list
    )


@dataclass
class LiteratureReviewSection:
    section_type: LiteratureReviewSectionType

    title: str

    objective: str

    findings: list[LiteratureReviewFinding] = field(
        default_factory=list
    )

    evidence: list[LiteratureReviewEvidence] = field(
        default_factory=list
    )

    narrative: str = ""


@dataclass
class LiteratureReviewEvidenceBundle:
    section_type: LiteratureReviewSectionType

    evidence: list[LiteratureReviewEvidence] = field(
        default_factory=list
    )


@dataclass
class LiteratureReviewEvidenceAggregation:
    query: str

    paper_ids: list[str]

    bundles: list[
        LiteratureReviewEvidenceBundle
    ] = field(
        default_factory=list
    )


@dataclass
class LiteratureReviewPlan:
    query: str

    paper_ids: list[str]

    sections: list[LiteratureReviewSection] = field(
        default_factory=list
    )


class LiteratureReviewValidationIssueCode(str, Enum):
    DUPLICATE_FINDING_ID = (
        "duplicate_finding_id"
    )

    UNKNOWN_EVIDENCE_ID = (
        "unknown_evidence_id"
    )

    EVIDENCE_OUTSIDE_CORPUS = (
        "evidence_outside_corpus"
    )

    PAPER_SUPPORT_MISMATCH = (
        "paper_support_mismatch"
    )

    SUPPORT_COUNT_MISMATCH = (
        "support_count_mismatch"
    )

    CROSS_PAPER_SUPPORT_TOO_LOW = (
        "cross_paper_support_too_low"
    )

    SINGLE_PAPER_FLAG_MISMATCH = (
        "single_paper_flag_mismatch"
    )

    EMPTY_FINDING_STATEMENT = (
        "empty_finding_statement"
    )

    FINDING_WITHOUT_EVIDENCE = (
        "finding_without_evidence"
    )


@dataclass
class LiteratureReviewValidationIssue:
    code: LiteratureReviewValidationIssueCode

    message: str

    section_type: (
        LiteratureReviewSectionType
        | None
    ) = None

    finding_id: str | None = None


@dataclass
class LiteratureReviewValidationResult:
    valid: bool

    issues: list[
        LiteratureReviewValidationIssue
    ] = field(
        default_factory=list
    )


@dataclass
class LiteratureReview:
    query: str

    paper_ids: list[str]

    title: str

    sections: list[LiteratureReviewSection]

    citations: list[str] = field(
        default_factory=list
    )

    validation: (
        LiteratureReviewValidationResult
        | None
    ) = None

    corpus_scope_note: str = (
        "This review summarizes evidence from the "
        "indexed corpus only. It does not represent "
        "an exhaustive review of all published "
        "literature."
    )