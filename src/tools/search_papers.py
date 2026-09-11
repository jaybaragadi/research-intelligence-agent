from dataclasses import dataclass

from src.retrieval.retriever import (
    RetrievedChunk,
    SemanticRetriever,
)


@dataclass
class PaperSearchResult:
    """
    Structured research evidence returned by
    the paper-search tool.
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
class PaperSearchResponse:
    """
    Full structured response for one research
    evidence search.
    """

    query: str
    result_count: int
    results: list[PaperSearchResult]


class SearchPapersTool:
    """
    Deterministic research search tool.

    This tool wraps the semantic retriever and
    converts retrieval output into a stable
    application-level schema.

    Future agents should depend on this tool
    instead of directly calling FAISS.
    """

    def __init__(
        self,
        retriever: SemanticRetriever | None = None,
    ) -> None:

        self.retriever = retriever if retriever is not None else SemanticRetriever()

    def search(
        self,
        query: str,
        top_k: int | None = None,
        allowed_paper_ids: set[str] | None = None,
        max_per_paper: int | None = None,
    ) -> PaperSearchResponse:
        """
        Search the research-paper corpus.

        Parameters
        ----------
        query:
            Natural-language research question.

        top_k:
            Maximum number of evidence chunks
            to return.

        allowed_paper_ids:
            Optional paper scope.

            When supplied, only chunks belonging
            to these papers are eligible.

        max_per_paper:
            Optional maximum number of returned
            chunks from one paper.

            This is useful for paper-scoped
            evidence acquisition where more than
            the retriever's default diversity
            limit may be required.

        Returns
        -------
        PaperSearchResponse
            Structured evidence with provenance.
        """

        if not query.strip():

            raise ValueError("Query cannot be empty")

        search_kwargs = {
            "query": query,
            "top_k": top_k,
        }

        if allowed_paper_ids is not None:

            search_kwargs["allowed_paper_ids"] = allowed_paper_ids

        if max_per_paper is not None:

            search_kwargs["max_per_paper"] = max_per_paper

        retrieved = self.retriever.search(**search_kwargs)

        results = [self._convert_result(result) for result in retrieved]

        return PaperSearchResponse(
            query=query,
            result_count=len(results),
            results=results,
        )

    def _convert_result(
        self,
        result: RetrievedChunk,
    ) -> PaperSearchResult:
        """
        Convert an internal retriever result
        into the stable tool-output schema.
        """

        return PaperSearchResult(
            rank=result.rank,
            paper_id=result.paper_id,
            page_number=result.page_number,
            section=result.section,
            score=result.score,
            raw_score=result.raw_score,
            lexical_score=(result.lexical_score),
            chunk_id=result.chunk_id,
            text=result.text,
        )


def search_papers(
    query: str,
    top_k: int | None = None,
) -> PaperSearchResponse:
    """
    Convenience function for applications
    that do not need to manage a tool instance.
    """

    tool = SearchPapersTool()

    return tool.search(
        query=query,
        top_k=top_k,
    )
