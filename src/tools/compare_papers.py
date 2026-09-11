from dataclasses import (
    dataclass,
    field,
)

from src.retrieval.retriever import (
    SemanticRetriever,
)


@dataclass
class ComparisonEvidence:
    """
    One evidence passage associated with
    one paper in a comparison.

    Every passage preserves enough provenance
    for later citation and evidence validation.
    """

    rank: int

    paper_id: str

    page_number: int

    section: str | None

    score: float

    raw_score: float

    lexical_score: float

    chunk_id: str

    text: str


@dataclass
class PaperComparisonEntry:
    """
    Evidence collected for one requested
    research paper.
    """

    paper_id: str

    evidence: list[ComparisonEvidence] = field(default_factory=list)


@dataclass
class PaperComparisonResponse:
    """
    Deterministic comparison result.

    Phase 6 does not generate prose conclusions.

    Instead, it returns evidence for each
    requested paper under the same comparison
    question.
    """

    query: str

    requested_papers: list[str]

    matched_papers: list[str]

    missing_papers: list[str]

    comparisons: list[PaperComparisonEntry]


class ComparePapersTool:
    """
    Compare two or more research papers using
    paper-scoped evidence retrieval.

    Each requested paper is searched
    independently.

    This prevents one paper with globally
    stronger semantic similarity from crowding
    another requested paper out of the
    comparison.
    """

    def __init__(
        self,
        retriever: SemanticRetriever | None = None,
    ) -> None:

        self.retriever = retriever if retriever is not None else SemanticRetriever()

    def compare(
        self,
        paper_ids: list[str],
        query: str,
        evidence_per_paper: int = 3,
    ) -> PaperComparisonResponse:
        """
        Compare requested papers around one
        shared research question.

        Parameters
        ----------
        paper_ids:
            Paper identifiers to compare.

        query:
            Shared comparison question.

        evidence_per_paper:
            Maximum number of evidence chunks
            returned for each paper.

        Returns
        -------
        PaperComparisonResponse
            Evidence grouped independently by
            requested paper.
        """

        cleaned_papers = [
            paper_id.strip() for paper_id in paper_ids if paper_id.strip()
        ]

        if len(cleaned_papers) < 2:
            raise ValueError("At least two paper IDs are required")

        if not query.strip():
            raise ValueError("Query cannot be empty")

        if evidence_per_paper <= 0:
            raise ValueError("evidence_per_paper must be positive")

        # Preserve caller order while removing
        # duplicate paper identifiers.
        requested_papers = list(dict.fromkeys(cleaned_papers))

        if len(requested_papers) < 2:
            raise ValueError("At least two unique paper IDs are required")

        evidence_by_paper: dict[
            str,
            list[ComparisonEvidence],
        ] = {paper_id: [] for paper_id in requested_papers}

        # Important Phase 6.3 correction:
        #
        # Retrieve separately for every requested
        # paper instead of doing one global search
        # and filtering afterward.
        for paper_id in requested_papers:

            retrieved = self.retriever.search(
                query=query,
                top_k=(evidence_per_paper),
                candidate_multiplier=6,
                max_per_paper=(evidence_per_paper),
                allowed_paper_ids={paper_id},
            )

            for result in retrieved:

                evidence_by_paper[paper_id].append(
                    ComparisonEvidence(
                        rank=(result.rank),
                        paper_id=(result.paper_id),
                        page_number=(result.page_number),
                        section=(result.section),
                        score=(result.score),
                        raw_score=(result.raw_score),
                        lexical_score=(result.lexical_score),
                        chunk_id=(result.chunk_id),
                        text=(result.text),
                    )
                )

        matched_papers = [
            paper_id for paper_id in requested_papers if evidence_by_paper[paper_id]
        ]

        missing_papers = [
            paper_id for paper_id in requested_papers if not evidence_by_paper[paper_id]
        ]

        comparisons = [
            PaperComparisonEntry(
                paper_id=paper_id,
                evidence=(evidence_by_paper[paper_id]),
            )
            for paper_id in requested_papers
        ]

        return PaperComparisonResponse(
            query=query,
            requested_papers=(requested_papers),
            matched_papers=(matched_papers),
            missing_papers=(missing_papers),
            comparisons=(comparisons),
        )


def compare_papers(
    paper_ids: list[str],
    query: str,
    evidence_per_paper: int = 3,
) -> PaperComparisonResponse:
    """
    Convenience wrapper for callers that do
    not need to manage a ComparePapersTool
    instance directly.
    """

    tool = ComparePapersTool()

    return tool.compare(
        paper_ids=paper_ids,
        query=query,
        evidence_per_paper=(evidence_per_paper),
    )
