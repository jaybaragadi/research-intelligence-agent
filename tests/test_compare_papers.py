import pytest

from src.retrieval.retriever import (
    RetrievedChunk,
)
from src.tools.compare_papers import (
    ComparePapersTool,
)


class FakeComparisonRetriever:
    """
    Deterministic fake retriever used for
    comparison-tool unit tests.

    It supports the same optional paper scope
    as SemanticRetriever.
    """

    def search(
        self,
        query: str,
        top_k: int | None = None,
        candidate_multiplier: int = 6,
        max_per_paper: int = 2,
        allowed_paper_ids: set[str] | None = None,
    ) -> list[RetrievedChunk]:

        results = [
            RetrievedChunk(
                rank=1,
                score=0.90,
                raw_score=0.80,
                lexical_score=0.75,
                chunk_id=("paper_a_chunk_1"),
                paper_id=("paper_a"),
                page_number=3,
                section=("methodology"),
                text=("Paper A uses mutation " "testing to improve tests."),
            ),
            RetrievedChunk(
                rank=2,
                score=0.85,
                raw_score=0.78,
                lexical_score=0.70,
                chunk_id=("paper_b_chunk_1"),
                paper_id=("paper_b"),
                page_number=4,
                section=("methodology"),
                text=("Paper B uses coverage " "feedback to improve tests."),
            ),
            RetrievedChunk(
                rank=3,
                score=0.80,
                raw_score=0.72,
                lexical_score=0.65,
                chunk_id=("paper_c_chunk_1"),
                paper_id=("paper_c"),
                page_number=5,
                section=("results"),
                text=("Paper C contains unrelated " "evidence."),
            ),
        ]

        if allowed_paper_ids is not None:
            results = [
                result for result in results if result.paper_id in allowed_paper_ids
            ]

        if top_k is not None:
            results = results[:top_k]

        return results


def test_compare_groups_requested_papers():

    tool = ComparePapersTool(retriever=(FakeComparisonRetriever()))

    response = tool.compare(
        paper_ids=[
            "paper_a",
            "paper_b",
        ],
        query=("How do the approaches " "improve generated tests?"),
    )

    assert response.requested_papers == [
        "paper_a",
        "paper_b",
    ]

    assert response.matched_papers == [
        "paper_a",
        "paper_b",
    ]

    assert response.missing_papers == []


def test_compare_filters_unrequested_papers():

    tool = ComparePapersTool(retriever=(FakeComparisonRetriever()))

    response = tool.compare(
        paper_ids=[
            "paper_a",
            "paper_b",
        ],
        query=("Compare approaches"),
    )

    returned_ids = [entry.paper_id for entry in response.comparisons]

    assert "paper_c" not in returned_ids


def test_compare_preserves_provenance():

    tool = ComparePapersTool(retriever=(FakeComparisonRetriever()))

    response = tool.compare(
        paper_ids=[
            "paper_a",
            "paper_b",
        ],
        query=("Compare approaches"),
    )

    evidence = response.comparisons[0].evidence[0]

    assert evidence.page_number == 3

    assert evidence.section == "methodology"

    assert evidence.chunk_id == "paper_a_chunk_1"


def test_compare_marks_missing_evidence():

    tool = ComparePapersTool(retriever=(FakeComparisonRetriever()))

    response = tool.compare(
        paper_ids=[
            "paper_a",
            "paper_missing",
        ],
        query=("Compare approaches"),
    )

    assert response.matched_papers == ["paper_a"]

    assert response.missing_papers == ["paper_missing"]


def test_compare_requires_two_papers():

    tool = ComparePapersTool(retriever=(FakeComparisonRetriever()))

    with pytest.raises(
        ValueError,
        match=("At least two paper IDs " "are required"),
    ):

        tool.compare(
            paper_ids=["paper_a"],
            query=("Compare approaches"),
        )


def test_compare_requires_unique_papers():

    tool = ComparePapersTool(retriever=(FakeComparisonRetriever()))

    with pytest.raises(
        ValueError,
        match=("At least two unique paper IDs " "are required"),
    ):

        tool.compare(
            paper_ids=[
                "paper_a",
                "paper_a",
            ],
            query=("Compare approaches"),
        )


def test_compare_rejects_empty_query():

    tool = ComparePapersTool(retriever=(FakeComparisonRetriever()))

    with pytest.raises(
        ValueError,
        match=("Query cannot be empty"),
    ):

        tool.compare(
            paper_ids=[
                "paper_a",
                "paper_b",
            ],
            query="   ",
        )


def test_compare_scopes_retrieval_per_paper():

    calls: list[set[str] | None] = []

    class TrackingRetriever:
        """
        Tracks which paper scope was supplied
        to each retrieval call.
        """

        def search(
            self,
            query: str,
            top_k: int | None = None,
            candidate_multiplier: int = 6,
            max_per_paper: int = 2,
            allowed_paper_ids: set[str] | None = None,
        ) -> list[RetrievedChunk]:

            calls.append(allowed_paper_ids)

            paper_id = next(iter(allowed_paper_ids or {"unknown"}))

            return [
                RetrievedChunk(
                    rank=1,
                    score=0.80,
                    raw_score=0.70,
                    lexical_score=0.60,
                    chunk_id=(f"{paper_id}_chunk"),
                    paper_id=(paper_id),
                    page_number=1,
                    section=("methodology"),
                    text=("Relevant evidence."),
                )
            ]

    tool = ComparePapersTool(retriever=(TrackingRetriever()))

    response = tool.compare(
        paper_ids=[
            "paper_a",
            "paper_b",
        ],
        query=("Compare feedback"),
    )

    assert calls == [
        {"paper_a"},
        {"paper_b"},
    ]

    assert response.missing_papers == []
