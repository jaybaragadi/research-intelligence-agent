import re
from dataclasses import dataclass

from src.config import settings
from src.retrieval.embedding_model import (
    EmbeddingModel,
)
from src.retrieval.faiss_store import (
    FaissStore,
)


LOW_VALUE_SECTIONS = {
    "references",
}


SECTION_BONUSES = {
    "methodology": 0.025,
    "evaluation": 0.020,
    "results": 0.025,
    "discussion": 0.020,
    "limitations": 0.035,
    "threats_to_validity": 0.035,
    "future_work": 0.030,
    "conclusion": 0.010,
    "introduction": 0.005,
    "related_work": -0.005,
}


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "do",
    "does",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "these",
    "to",
    "use",
    "used",
    "using",
    "what",
    "which",
    "with",
}


@dataclass
class RetrievedChunk:
    """
    One retrieved research-evidence chunk
    with provenance and scoring details.

    raw_score:
        Original cosine similarity returned
        by FAISS.

    lexical_score:
        Normalized lexical overlap between
        the query and the chunk.

    score:
        Final hybrid ranking score after
        semantic, lexical, concept, and
        section-aware scoring.
    """

    rank: int

    score: float

    raw_score: float

    lexical_score: float

    chunk_id: str

    paper_id: str

    page_number: int

    section: str | None

    text: str


class SemanticRetriever:
    """
    Hybrid research-evidence retriever.

    Retrieval pipeline:

        user question
             ↓
        query embedding
             ↓
        FAISS candidate retrieval
             ↓
        low-value content filtering
             ↓
        lexical normalization
             ↓
        lexical overlap scoring
             ↓
        concept-alignment bonus
             ↓
        section-aware scoring
             ↓
        paper diversity
             ↓
        final top-k evidence
    """

    def __init__(
        self,
    ) -> None:

        self.embedding_model = (
            EmbeddingModel(
                settings.embedding_model
            )
        )

        self.store = (
            FaissStore(
                settings.vector_store_dir
            )
        )


    def _normalize_token(
        self,
        token: str,
    ) -> str:
        """
        Apply lightweight lexical normalization.

        This helps align common morphological
        variants without requiring a full NLP
        dependency.

        Examples:

            tests       -> test
            generated   -> generate
            generating  -> generate
            improves    -> improve
            limitations -> limitation
        """

        irregular_forms = {
            "generated": "generate",
            "generating": "generate",
            "generation": "generate",

            "improved": "improve",
            "improves": "improve",
            "improving": "improve",

            "limitations": "limitation",

            "approaches": "approach",

            "methods": "method",

            "techniques": "technique",

            "strategies": "strategy",

            "tests": "test",

            "papers": "paper",

            "results": "result",

            "benchmarks": "benchmark",

            "metrics": "metric",

            "challenges": "challenge",

            "weaknesses": "weakness",

            "risks": "risk",
        }

        if token in irregular_forms:

            return irregular_forms[
                token
            ]

        if (
            token.endswith("ies")
            and len(token) > 4
        ):

            return (
                token[:-3]
                + "y"
            )

        if (
            token.endswith("s")
            and not token.endswith("ss")
            and len(token) > 4
        ):

            return token[:-1]

        return token


    def _tokenize(
        self,
        text: str,
    ) -> set[str]:
        """
        Convert text into normalized lexical
        concepts.

        Stopwords and very short tokens are removed.
        """

        raw_tokens = re.findall(
            r"[a-z0-9]+",
            text.lower(),
        )

        tokens: set[str] = set()

        for token in raw_tokens:

            if (
                len(token) <= 2
                or token in STOPWORDS
            ):
                continue

            normalized = (
                self._normalize_token(
                    token
                )
            )

            if (
                len(normalized) > 2
                and normalized
                not in STOPWORDS
            ):

                tokens.add(
                    normalized
                )

        return tokens


    def _lexical_score(
        self,
        query: str,
        text: str,
    ) -> float:
        """
        Measure normalized lexical overlap
        between the query and the chunk.

        Returns a value between:

            0.0 and 1.0
        """

        query_terms = (
            self._tokenize(
                query
            )
        )

        if not query_terms:

            return 0.0

        text_terms = (
            self._tokenize(
                text
            )
        )

        overlap = (
            query_terms
            & text_terms
        )

        return (
            len(overlap)
            / len(query_terms)
        )


    def _concept_alignment_bonus(
        self,
        query: str,
        text: str,
    ) -> float:
        """
        Reward chunks containing several
        meaningful query concepts.

        This helps distinguish direct evidence
        from passages that merely contain one
        semantically related term.

        Example:

            Query:
                iterative feedback improve
                generated tests

            Strong passage:
                iterative feedback improves
                generated tests

            Weak passage:
                feedback-directed testing
        """

        query_terms = (
            self._tokenize(
                query
            )
        )

        text_terms = (
            self._tokenize(
                text
            )
        )

        if not query_terms:

            return 0.0

        matched_terms = (
            query_terms
            & text_terms
        )

        matched_count = len(
            matched_terms
        )

        if matched_count >= 5:

            return 0.040

        if matched_count >= 4:

            return 0.025

        if matched_count >= 3:

            return 0.010

        return 0.0


    def _looks_like_reference_text(
        self,
        text: str,
    ) -> bool:
        """
        Detect bibliography-heavy chunks.

        This protects retrieval quality when
        section metadata is imperfect and a
        references chunk is accidentally labeled
        as another section.
        """

        normalized = (
            text.lower()
        )

        reference_markers = (
            "doi.org/",
            "arxiv:",
            "arxiv.org",
            "proc. acm",
            "ieee computer society",
            "conference on software",
            "transactions on software",
            "et al.",
        )

        marker_count = sum(
            1
            for marker
            in reference_markers
            if marker in normalized
        )

        citation_patterns = len(
            re.findall(
                r"\[\d+\]",
                text,
            )
        )

        year_patterns = len(
            re.findall(
                r"\b(?:19|20)\d{2}\b",
                text,
            )
        )

        if marker_count >= 3:

            return True

        if (
            citation_patterns >= 6
            and year_patterns >= 4
        ):

            return True

        return False


    def _section_bonus(
        self,
        section: str | None,
    ) -> float:
        """
        Apply a small general research-section
        bonus.

        The bonus is deliberately small because
        section metadata is not always perfect.
        """

        if section is None:

            return 0.0

        return (
            SECTION_BONUSES.get(
                section,
                0.0,
            )
        )


    def _query_section_bonus(
        self,
        query: str,
        section: str | None,
    ) -> float:
        """
        Apply small query-intent-aware section
        bonuses.

        Example:

            limitation questions

        should prefer:

            limitations
            threats_to_validity
            future_work
        """

        if section is None:

            return 0.0

        normalized_query = (
            query.lower()
        )

        bonus = 0.0

        limitation_terms = (
            "limitation",
            "limitations",
            "weakness",
            "weaknesses",
            "challenge",
            "challenges",
            "threat",
            "threats",
            "future work",
            "drawback",
            "drawbacks",
            "risk",
            "risks",
        )

        methodology_terms = (
            "approach",
            "approaches",
            "method",
            "methods",
            "methodology",
            "technique",
            "techniques",
            "strategy",
            "strategies",
        )

        result_terms = (
            "result",
            "results",
            "performance",
            "coverage",
            "improvement",
            "improvements",
            "improve",
            "improves",
            "improved",
            "outperform",
            "outperforms",
            "effective",
            "effectiveness",
        )

        evaluation_terms = (
            "evaluate",
            "evaluation",
            "evaluated",
            "benchmark",
            "benchmarks",
            "metric",
            "metrics",
            "compare",
            "comparison",
        )

        if any(
            term in normalized_query
            for term in limitation_terms
        ):

            if section in {
                "limitations",
                "threats_to_validity",
                "future_work",
            }:

                bonus += 0.050

            elif section in {
                "discussion",
                "conclusion",
            }:

                bonus += 0.020

        if any(
            term in normalized_query
            for term in methodology_terms
        ):

            if (
                section
                == "methodology"
            ):

                bonus += 0.030

        if any(
            term in normalized_query
            for term in result_terms
        ):

            if section in {
                "results",
                "evaluation",
            }:

                bonus += 0.025

        if any(
            term in normalized_query
            for term in evaluation_terms
        ):

            if section in {
                "evaluation",
                "experimental_setup",
                "results",
            }:

                bonus += 0.020

        return bonus


    def _hybrid_score(
        self,
        query: str,
        text: str,
        raw_score: float,
        section: str | None,
    ) -> tuple[
        float,
        float,
    ]:
        """
        Combine semantic similarity,
        lexical relevance, concept alignment,
        and section-aware scoring.

        Current weighting:

            85% semantic similarity
            15% lexical overlap

        Small bonuses are added afterward.
        """

        lexical_score = (
            self._lexical_score(
                query,
                text,
            )
        )

        semantic_component = (
            raw_score
            * 0.85
        )

        lexical_component = (
            lexical_score
            * 0.15
        )

        concept_bonus = (
            self._concept_alignment_bonus(
                query,
                text,
            )
        )

        section_bonus = (
            self._section_bonus(
                section
            )
        )

        query_section_bonus = (
            self._query_section_bonus(
                query,
                section,
            )
        )

        final_score = (
            semantic_component
            + lexical_component
            + concept_bonus
            + section_bonus
            + query_section_bonus
        )

        return (
            final_score,
            lexical_score,
        )


    def search(
        self,
        query: str,
        top_k: int | None = None,
        candidate_multiplier: int = 6,
        max_per_paper: int = 2,
    ) -> list[RetrievedChunk]:
        """
        Search the research corpus and return
        high-quality evidence.

        Example:

            top_k = 5
            candidate_multiplier = 6

        FAISS first retrieves up to 30 candidate
        chunks.

        Those candidates are then:

            filtered
            normalized
            lexically scored
            concept scored
            section scored
            diversified

        before returning the final top-k results.
        """

        if not query.strip():

            raise ValueError(
                "Query cannot be empty"
            )

        if top_k is None:

            top_k = (
                settings.top_k
            )

        if top_k <= 0:

            raise ValueError(
                "top_k must be positive"
            )

        if candidate_multiplier <= 0:

            raise ValueError(
                "candidate_multiplier "
                "must be positive"
            )

        if max_per_paper <= 0:

            raise ValueError(
                "max_per_paper "
                "must be positive"
            )

        chunks = (
            self.store.load_chunks()
        )

        if not chunks:

            return []

        query_embedding = (
            self.embedding_model.encode_query(
                query
            )
        )

        candidate_k = min(
            len(chunks),
            max(
                top_k,
                top_k
                * candidate_multiplier,
            ),
        )

        scores, indexes = (
            self.store.search(
                query_embedding,
                candidate_k,
            )
        )

        candidates: list[
            RetrievedChunk
        ] = []

        for score, index in zip(
            scores[0],
            indexes[0],
        ):

            if index < 0:

                continue

            chunk = chunks[
                int(index)
            ]

            if (
                chunk.section
                in LOW_VALUE_SECTIONS
            ):

                continue

            if (
                self._looks_like_reference_text(
                    chunk.text
                )
            ):

                continue

            raw_score = float(
                score
            )

            (
                hybrid_score,
                lexical_score,
            ) = (
                self._hybrid_score(
                    query=query,
                    text=chunk.text,
                    raw_score=raw_score,
                    section=chunk.section,
                )
            )

            candidates.append(
                RetrievedChunk(
                    rank=0,

                    score=(
                        hybrid_score
                    ),

                    raw_score=(
                        raw_score
                    ),

                    lexical_score=(
                        lexical_score
                    ),

                    chunk_id=(
                        chunk.chunk_id
                    ),

                    paper_id=(
                        chunk.paper_id
                    ),

                    page_number=(
                        chunk.page_number
                    ),

                    section=(
                        chunk.section
                    ),

                    text=(
                        chunk.text
                    ),
                )
            )

        candidates.sort(
            key=lambda result: (
                result.score
            ),
            reverse=True,
        )

        selected: list[
            RetrievedChunk
        ] = []

        paper_counts: dict[
            str,
            int,
        ] = {}

        for candidate in candidates:

            current_count = (
                paper_counts.get(
                    candidate.paper_id,
                    0,
                )
            )

            if (
                current_count
                >= max_per_paper
            ):

                continue

            candidate.rank = (
                len(selected)
                + 1
            )

            selected.append(
                candidate
            )

            paper_counts[
                candidate.paper_id
            ] = (
                current_count
                + 1
            )

            if (
                len(selected)
                >= top_k
            ):

                break

        return selected