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
                chunk_id=(
                    "paper_a_chunk_0001"
                ),
                paper_id="paper_a",
                page_number=5,
                section="methodology",
                text=(
                    "Mutation testing is used "
                    "to assess test quality."
                ),
            )
        ]


def test_search_returns_structured_response():

    tool = SearchPapersTool(
        retriever=FakeRetriever()
    )

    response = tool.search(
        "Which approaches use mutation testing?"
    )

    assert (
        response.query
        == "Which approaches use mutation testing?"
    )

    assert response.result_count == 1

    assert (
        response.results[0].paper_id
        == "paper_a"
    )

    assert (
        response.results[0].page_number
        == 5
    )

    assert (
        response.results[0].section
        == "methodology"
    )


def test_search_preserves_scores():

    tool = SearchPapersTool(
        retriever=FakeRetriever()
    )

    response = tool.search(
        "mutation testing"
    )

    result = response.results[0]

    assert result.score == 0.82

    assert result.raw_score == 0.74

    assert (
        result.lexical_score
        == 0.80
    )


def test_search_rejects_empty_query():

    tool = SearchPapersTool(
        retriever=FakeRetriever()
    )

    try:

        tool.search(
            "   "
        )

    except ValueError as error:

        assert (
            str(error)
            == "Query cannot be empty"
        )

    else:

        raise AssertionError(
            "Expected ValueError"
        )