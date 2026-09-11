from src.tools.citation_tool import (
    CitationRecord,
    CitationTool,
)
from src.tools.compare_papers import (
    ComparePapersTool,
    PaperComparisonResponse,
)
from src.tools.evidence_tool import (
    EvidenceRecord,
    EvidenceTool,
)
from src.tools.search_papers import (
    PaperSearchResponse,
    SearchPapersTool,
)
from src.tools.summarize_paper import (
    PaperSummary,
    SummarizePaperTool,
)


class ResearchTools:
    """
    Unified application-facing interface for
    the deterministic research tool layer.

    Phase 7 agents should depend on this class
    rather than directly accessing retrieval,
    FAISS, metadata files, or chunk storage.
    """

    def __init__(
        self,
        search_tool: SearchPapersTool | None = None,
        summarize_tool: SummarizePaperTool | None = None,
        compare_tool: ComparePapersTool | None = None,
        evidence_tool: EvidenceTool | None = None,
        citation_tool: CitationTool | None = None,
    ) -> None:

        self.evidence_tool = (
            evidence_tool if evidence_tool is not None else EvidenceTool()
        )

        self.citation_tool = (
            citation_tool
            if citation_tool is not None
            else CitationTool(evidence_tool=(self.evidence_tool))
        )

        self.search_tool = (
            search_tool if search_tool is not None else SearchPapersTool()
        )

        self.summarize_tool = (
            summarize_tool if summarize_tool is not None else SummarizePaperTool()
        )

        self.compare_tool = (
            compare_tool if compare_tool is not None else ComparePapersTool()
        )

    def search(
        self,
        query: str,
        top_k: int | None = None,
    ) -> PaperSearchResponse:
        """
        Search the paper corpus for relevant
        evidence.
        """

        return self.search_tool.search(
            query=query,
            top_k=top_k,
        )

    def summarize(
        self,
        paper_id: str,
    ) -> PaperSummary:
        """
        Return a deterministic structured
        summary for one paper.
        """

        return self.summarize_tool.summarize(paper_id)

    def compare(
        self,
        paper_ids: list[str],
        query: str,
        evidence_per_paper: int = 3,
    ) -> PaperComparisonResponse:
        """
        Compare requested papers using
        paper-scoped retrieved evidence.
        """

        return self.compare_tool.compare(
            paper_ids=paper_ids,
            query=query,
            evidence_per_paper=(evidence_per_paper),
        )

    def evidence(
        self,
        evidence_id: str,
    ) -> EvidenceRecord:
        """
        Resolve and validate one evidence ID.
        """

        return self.evidence_tool.get(evidence_id)

    def citation(
        self,
        evidence_id: str,
    ) -> CitationRecord:
        """
        Produce a citation from validated
        evidence.
        """

        return self.citation_tool.cite(evidence_id)
