import numpy as np

from src.retrieval.cross_encoder_reranker import CrossEncoderReranker
from src.retrieval.retriever import RetrievedChunk


class FakeRetriever:
    def search(
        self,
        query,
        top_k=None,
        max_per_paper=2,
        allowed_paper_ids=None,
    ):
        return [
            RetrievedChunk(
                rank=1,
                score=0.9,
                raw_score=0.9,
                lexical_score=0.5,
                chunk_id="chunk_1",
                paper_id="paper_a",
                page_number=1,
                section="methodology",
                text="Generic software testing approach.",
            ),
            RetrievedChunk(
                rank=2,
                score=0.8,
                raw_score=0.8,
                lexical_score=0.4,
                chunk_id="chunk_2",
                paper_id="paper_b",
                page_number=2,
                section="results",
                text="LLMs generate unit tests using feedback.",
            ),
        ]


class FakeCrossEncoder:
    def predict(self, pairs):
        return np.array(
            [
                0.10,
                0.95,
            ]
        )


def build_reranker():
    reranker = CrossEncoderReranker.__new__(CrossEncoderReranker)

    reranker.base_retriever = FakeRetriever()
    reranker.model = FakeCrossEncoder()
    reranker.candidate_k = 10

    return reranker


def test_cross_encoder_changes_ranking():
    reranker = build_reranker()

    results = reranker.search(
        query="How are LLMs used for test generation?",
        top_k=2,
    )

    assert results[0].paper_id == "paper_b"
    assert results[1].paper_id == "paper_a"


def test_cross_encoder_assigns_new_ranks():
    reranker = build_reranker()

    results = reranker.search(
        query="LLM test generation",
        top_k=2,
    )

    assert results[0].rank == 1
    assert results[1].rank == 2


def test_cross_encoder_respects_top_k():
    reranker = build_reranker()

    results = reranker.search(
        query="LLM test generation",
        top_k=1,
    )

    assert len(results) == 1


def test_cross_encoder_rejects_empty_query():
    reranker = build_reranker()

    try:
        reranker.search(
            query=" ",
        )
    except ValueError as exc:
        assert str(exc) == "Query cannot be empty"
    else:
        raise AssertionError("Expected ValueError")
