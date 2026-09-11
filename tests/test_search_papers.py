from src.retrieval.retriever import (
    RetrievedChunk,
)
from src.tools.search_papers import (
    SearchPapersTool,
)


class FakeRetriever:
    """
    Small deterministic retriever used for
    tool-level unit tests.
    """

    def search(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[RetrievedChunk]:

        return [
            RetrievedChunk(
                rank=1,
                score=0.82,
                raw_score=0.74,
                lexical_score=0.80,
                chunk_id=("paper_a_chunk_0001"),
                paper_id="paper_a",
                page_number=5,
                section="methodology",
                text=("Mutation testing is used " "to assess test quality."),
            )
        ]


def test_search_returns_structured_response():

    tool = SearchPapersTool(retriever=FakeRetriever())

    response = tool.search("Which approaches use mutation testing?")

    assert response.query == "Which approaches use mutation testing?"

    assert response.result_count == 1

    assert response.results[0].paper_id == "paper_a"

    assert response.results[0].page_number == 5

    assert response.results[0].section == "methodology"


def test_search_preserves_scores():

    tool = SearchPapersTool(retriever=FakeRetriever())

    response = tool.search("mutation testing")

    result = response.results[0]

    assert result.score == 0.82

    assert result.raw_score == 0.74

    assert result.lexical_score == 0.80


def test_search_rejects_empty_query():

    tool = SearchPapersTool(retriever=FakeRetriever())

    try:

        tool.search("   ")

    except ValueError as error:

        assert str(error) == "Query cannot be empty"

    else:

        raise AssertionError("Expected ValueError")


class ScopedFakeRetriever:
    """
    Verify that tool-level paper scoping is
    forwarded to the semantic retriever.
    """

    def __init__(self) -> None:
        self.allowed_paper_ids = None
        self.max_per_paper = None

    def search(
        self,
        query: str,
        top_k: int | None = None,
        allowed_paper_ids: set[str] | None = None,
        max_per_paper: int = 2,
    ) -> list[RetrievedChunk]:

        self.allowed_paper_ids = allowed_paper_ids

        self.max_per_paper = max_per_paper

        return []


def test_search_forwards_paper_scope():

    retriever = ScopedFakeRetriever()

    tool = SearchPapersTool(retriever=retriever)

    response = tool.search(
        query="future work",
        top_k=4,
        allowed_paper_ids={"paper_a"},
        max_per_paper=4,
    )

    assert response.result_count == 0

    assert retriever.allowed_paper_ids == {"paper_a"}

    assert retriever.max_per_paper == 4
