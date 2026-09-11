import numpy as np

from src.retrieval.fused_cross_encoder_reranker import (
    FusedCrossEncoderReranker,
)
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
                score=0.90,
                raw_score=0.90,
                lexical_score=0.50,
                chunk_id="chunk_1",
                paper_id="paper_a",
                page_number=1,
                section="methodology",
                text="Baseline strongly prefers this chunk.",
            ),
            RetrievedChunk(
                rank=2,
                score=0.60,
                raw_score=0.60,
                lexical_score=0.30,
                chunk_id="chunk_2",
                paper_id="paper_b",
                page_number=2,
                section="results",
                text="Cross encoder strongly prefers this chunk.",
            ),
        ]


class FakeCrossEncoder:
    def predict(self, pairs):
        return np.array(
            [
                0.20,
                0.95,
            ]
        )


def build_reranker(
    cross_encoder_weight=0.5,
):
    reranker = FusedCrossEncoderReranker.__new__(FusedCrossEncoderReranker)

    reranker.base_retriever = FakeRetriever()
    reranker.model = FakeCrossEncoder()
    reranker.candidate_k = 10
    reranker.cross_encoder_weight = cross_encoder_weight

    return reranker


def test_normalize_values():
    reranker = build_reranker()

    normalized = reranker._normalize(
        [
            1.0,
            2.0,
            3.0,
        ]
    )

    assert normalized == [
        0.0,
        0.5,
        1.0,
    ]


def test_normalize_equal_values():
    reranker = build_reranker()

    normalized = reranker._normalize(
        [
            2.0,
            2.0,
        ]
    )

    assert normalized == [
        1.0,
        1.0,
    ]


def test_baseline_only_preserves_baseline_ranking():
    reranker = build_reranker(cross_encoder_weight=0.0)

    results = reranker.search(
        query="test generation",
        top_k=2,
    )

    assert results[0].paper_id == "paper_a"


def test_cross_encoder_only_uses_cross_encoder_ranking():
    reranker = build_reranker(cross_encoder_weight=1.0)

    results = reranker.search(
        query="test generation",
        top_k=2,
    )

    assert results[0].paper_id == "paper_b"


def test_fused_search_respects_top_k():
    reranker = build_reranker()

    results = reranker.search(
        query="test generation",
        top_k=1,
    )

    assert len(results) == 1


def test_fused_search_rejects_empty_query():
    reranker = build_reranker()

    try:
        reranker.search(
            query=" ",
        )
    except ValueError as exc:
        assert str(exc) == "Query cannot be empty"
    else:
        raise AssertionError("Expected ValueError")
