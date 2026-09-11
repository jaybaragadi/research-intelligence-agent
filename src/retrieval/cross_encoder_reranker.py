from sentence_transformers import CrossEncoder

from src.retrieval.retriever import RetrievedChunk, SemanticRetriever

DEFAULT_CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class CrossEncoderReranker:
    """
    Optional second-stage reranker.

    The existing SemanticRetriever remains the baseline.

    Workflow:
        query
          -> SemanticRetriever
          -> candidate chunks
          -> CrossEncoder(query, chunk)
          -> reranked results
    """

    def __init__(
        self,
        base_retriever: SemanticRetriever | None = None,
        model_name: str = DEFAULT_CROSS_ENCODER_MODEL,
        candidate_k: int = 30,
    ) -> None:
        if candidate_k <= 0:
            raise ValueError("candidate_k must be positive")

        self.base_retriever = (
            base_retriever if base_retriever is not None else SemanticRetriever()
        )

        self.model = CrossEncoder(model_name)

        self.candidate_k = candidate_k

    def search(
        self,
        query: str,
        top_k: int | None = None,
        allowed_paper_ids: set[str] | None = None,
        max_per_paper: int = 2,
    ) -> list[RetrievedChunk]:
        if not query.strip():
            raise ValueError("Query cannot be empty")

        if top_k is None:
            top_k = 5

        if top_k <= 0:
            raise ValueError("top_k must be positive")

        if max_per_paper <= 0:
            raise ValueError("max_per_paper must be positive")

        candidate_limit = max(
            self.candidate_k,
            top_k,
        )

        candidates = self.base_retriever.search(
            query=query,
            top_k=candidate_limit,
            max_per_paper=candidate_limit,
            allowed_paper_ids=allowed_paper_ids,
        )

        if not candidates:
            return []

        pairs = [
            (
                query,
                candidate.text,
            )
            for candidate in candidates
        ]

        rerank_scores = self.model.predict(pairs)

        ranked_candidates = sorted(
            zip(
                candidates,
                rerank_scores,
            ),
            key=lambda item: float(item[1]),
            reverse=True,
        )

        selected: list[RetrievedChunk] = []
        paper_counts: dict[str, int] = {}

        for candidate, rerank_score in ranked_candidates:
            current_count = paper_counts.get(
                candidate.paper_id,
                0,
            )

            if current_count >= max_per_paper:
                continue

            selected.append(
                RetrievedChunk(
                    rank=len(selected) + 1,
                    score=float(rerank_score),
                    raw_score=candidate.raw_score,
                    lexical_score=candidate.lexical_score,
                    chunk_id=candidate.chunk_id,
                    paper_id=candidate.paper_id,
                    page_number=candidate.page_number,
                    section=candidate.section,
                    text=candidate.text,
                )
            )

            paper_counts[candidate.paper_id] = current_count + 1

            if len(selected) >= top_k:
                break

        return selected
