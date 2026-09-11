from dataclasses import (
    dataclass,
    field,
)
from enum import Enum


class GapType(str, Enum):
    """
    High-level type of research-gap result.

    EXPLICIT:
        A paper directly reports a limitation,
        unresolved issue, or future-work need.

    CORPUS_IMBALANCE:
        The indexed corpus contains substantially
        more evidence for one research area than
        another related area.

    INSUFFICIENT_EVIDENCE:
        The corpus does not contain enough
        validated evidence to safely claim a gap.
    """

    EXPLICIT = "explicit"

    CORPUS_IMBALANCE = "corpus_imbalance"

    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class GapSignalType(str, Enum):
    """
    Type of evidence signal that contributes
    to gap analysis.
    """

    LIMITATION = "limitation"

    FUTURE_WORK = "future_work"

    UNRESOLVED_PROBLEM = "unresolved_problem"

    UNDEREXPLORED_AREA = "underexplored_area"

    COVERAGE_IMBALANCE = "coverage_imbalance"


class GapConfidence(str, Enum):
    """
    Confidence assigned to a candidate gap.

    Confidence describes support inside the
    indexed corpus.

    It does NOT claim that the gap exists across
    all published scientific literature.
    """

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"


@dataclass
class GapEvidence:
    """
    One validated evidence passage supporting
    a research-gap signal or candidate.

    Provenance is kept explicit so every gap
    can be traced back to the source paper.
    """

    evidence_id: str

    paper_id: str

    page_number: int

    section: str | None

    signal_type: GapSignalType

    text: str

    citation_text: str

    relevance_score: float = 0.0


@dataclass
class PaperGapSignals:
    """
    Gap-related evidence collected for one paper.
    """

    paper_id: str

    signals: list[GapEvidence] = field(default_factory=list)


@dataclass
class DimensionCoverage:
    """
    Corpus-level coverage statistics for one
    analytical research dimension.

    This represents evidence presence in the
    indexed corpus, not scientific importance.
    """

    dimension: str

    paper_count: int

    evidence_count: int

    paper_ids: list[str] = field(default_factory=list)

    evidence_ids: list[str] = field(default_factory=list)


@dataclass
class GapCandidate:
    """
    One candidate research gap.

    A candidate is not automatically considered
    a validated research gap.
    """

    gap_id: str

    gap_type: GapType

    title: str

    description: str

    confidence: GapConfidence

    paper_ids: list[str] = field(default_factory=list)

    evidence_ids: list[str] = field(default_factory=list)

    dimensions: list[str] = field(default_factory=list)

    reason: str = ""


@dataclass
class GapValidationIssue:
    """
    Problem discovered while validating a
    candidate research gap.
    """

    issue_type: str

    message: str

    gap_id: str | None = None

    evidence_id: str | None = None


@dataclass
class GapValidationResult:
    """
    Validation result for one or more candidate
    research gaps.
    """

    is_valid: bool

    validated_gap_count: int

    issue_count: int

    issues: list[GapValidationIssue] = field(default_factory=list)


@dataclass
class ResearchGapAnalysis:
    """
    Complete Phase 10 gap-analysis response.
    """

    query: str

    corpus_papers: list[str]

    paper_signals: list[PaperGapSignals]

    dimension_coverage: list[DimensionCoverage]

    candidates: list[GapCandidate]

    validation: GapValidationResult | None = None
