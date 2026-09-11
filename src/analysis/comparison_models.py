from dataclasses import (
    dataclass,
    field,
)


@dataclass
class DimensionEvidence:
    """
    One evidence passage assigned to one
    analytical comparison dimension.
    """

    evidence_id: str

    paper_id: str

    dimension: str

    page_number: int

    section: str | None

    text: str

    citation_text: str

    relevance_score: float = 0.0


@dataclass
class PaperDimensionAnalysis:
    """
    Evidence associated with one analytical
    dimension for one paper.
    """

    dimension: str

    evidence: list[DimensionEvidence] = field(default_factory=list)


@dataclass
class PaperAnalysisProfile:
    """
    Structured comparative profile of one
    research paper.
    """

    paper_id: str

    dimensions: list[PaperDimensionAnalysis] = field(default_factory=list)


@dataclass
class ComparisonCell:
    """
    One paper/dimension cell in the final
    comparison matrix.

    Phase 9 remains extractive and evidence
    grounded.
    """

    paper_id: str

    dimension: str

    summary: str | None

    evidence_ids: list[str] = field(default_factory=list)


@dataclass
class ComparisonRow:
    """
    One analytical dimension across all
    requested papers.
    """

    dimension: str

    cells: list[ComparisonCell] = field(default_factory=list)


@dataclass
class ComparativeFinding:
    """
    One deterministic cross-paper observation.

    It is created only from populated comparison
    cells and preserves supporting evidence IDs.
    """

    finding_id: str

    finding_type: str

    text: str

    paper_ids: list[str]

    evidence_ids: list[str] = field(default_factory=list)


@dataclass
class ComparativeAnalysis:
    """
    Complete Phase 9 comparative-analysis result.
    """

    query: str

    requested_papers: list[str]

    profiles: list[PaperAnalysisProfile]

    matrix: list[ComparisonRow]

    findings: list[ComparativeFinding]
