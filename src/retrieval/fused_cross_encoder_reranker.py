from sentence_transformers import CrossEncoder

from src.retrieval.cross_encoder_reranker import (
    DEFAULT_CROSS_ENCODER_MODEL,
)
from src.retrieval.retriever import (
    RetrievedChunk,
    SemanticRetriever,
)


class FusedCrossEncoderReranker:
    """
    Experimental reranker that combines the existing
    hybrid retrieval score with a cross-encoder score.

    The baseline SemanticRetriever remains unchanged.

    Workflow:
        query
          -> SemanticRetriever
          -> candidate chunks
          -> CrossEncoder(query, chunk)
          -> normalize both score sets
          -> 50/50 score fusion
          -> paper diversity
          -> final ranking

    This is intentionally a separate experimental path
    so that the frozen baseline and pure cross-encoder
    experiment remain reproducible.
    """

    def __init__(
        self,
        base_retriever: SemanticRetriever | None = None,
        model_name: str = DEFAULT_CROSS_ENCODER_MODEL,
        candidate_k: int = 30,
        cross_encoder_weight: float = 0.5,
    ) -> None:
        if candidate_k <= 0:
            raise ValueError("candidate_k must be positive")

        if not 0.0 <= cross_encoder_weight <= 1.0:
            raise ValueError("cross_encoder_weight must be between 0 and 1")

        self.base_retriever = (
            base_retriever if base_retriever is not None else SemanticRetriever()
        )

        self.model = CrossEncoder(model_name)

        self.candidate_k = candidate_k
        self.cross_encoder_weight = cross_encoder_weight

    def _normalize(
        self,
        values: list[float],
    ) -> list[float]:
        """
        Min-max normalize one query's candidate scores.

        This is necessary because the existing hybrid score
        and cross-encoder score are on different numeric scales.
        """

        if not values:
            return []

        minimum = min(values)
        maximum = max(values)

        if maximum == minimum:
            return [1.0 for _ in values]

        return [(value - minimum) / (maximum - minimum) for value in values]

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

        cross_encoder_scores = [float(score) for score in self.model.predict(pairs)]

        baseline_scores = [float(candidate.score) for candidate in candidates]

        normalized_baseline = self._normalize(baseline_scores)

        normalized_cross_encoder = self._normalize(cross_encoder_scores)

        baseline_weight = 1.0 - self.cross_encoder_weight

        fused_candidates: list[tuple[RetrievedChunk, float]] = []

        for (
            candidate,
            baseline_score,
            cross_encoder_score,
        ) in zip(
            candidates,
            normalized_baseline,
            normalized_cross_encoder,
        ):
            fused_score = (
                baseline_weight * baseline_score
                + self.cross_encoder_weight * cross_encoder_score
            )

            fused_candidates.append(
                (
                    candidate,
                    fused_score,
                )
            )

        fused_candidates.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        selected: list[RetrievedChunk] = []

        paper_counts: dict[str, int] = {}

        for candidate, fused_score in fused_candidates:
            current_count = paper_counts.get(
                candidate.paper_id,
                0,
            )

            if current_count >= max_per_paper:
                continue

            selected.append(
                RetrievedChunk(
                    rank=len(selected) + 1,
                    score=float(fused_score),
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
