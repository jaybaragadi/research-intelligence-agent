import math
import re
from collections import Counter

from src.generation.models import (
    EvidencePackage,
    GeneratedClaim,
    GeneratedDraft,
)

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "approach",
    "approaches",
    "based",
    "be",
    "by",
    "do",
    "does",
    "for",
    "from",
    "generation",
    "generated",
    "how",
    "in",
    "is",
    "it",
    "llm",
    "llms",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "these",
    "this",
    "test",
    "testing",
    "tests",
    "to",
    "use",
    "used",
    "using",
    "what",
    "which",
    "with",
}


class DeterministicGroundedGenerator:
    """
    Evidence-grounded deterministic generator.

    Instead of taking the first sentence from
    each evidence chunk, it selects the sentence
    most relevant to the user's query.

    No new factual content is created.
    """

    def __init__(
        self,
        max_claims: int = 5,
        min_relevance_score: float = 1.0,
    ) -> None:

        if max_claims <= 0:

            raise ValueError("max_claims must be positive")

        if min_relevance_score <= 0:

            raise ValueError("min_relevance_score must be positive")

        self.max_claims = max_claims

        self.min_relevance_score = min_relevance_score

    def _normalize(
        self,
        text: str,
    ) -> str:

        text = re.sub(
            r"\s+",
            " ",
            text.strip(),
        )

        # Improve obvious PDF punctuation
        # spacing without modifying the stored
        # source evidence.
        text = re.sub(
            r"([,;:])(?=[A-Za-z])",
            r"\1 ",
            text,
        )

        return text

    def _tokens(
        self,
        text: str,
    ) -> list[str]:

        tokens = re.findall(
            r"[a-z0-9]+",
            text.lower(),
        )

        return [
            token for token in tokens if (len(token) > 1 and token not in STOP_WORDS)
        ]

    def _sentences(
        self,
        text: str,
    ) -> list[str]:

        cleaned = self._normalize(text)

        if not cleaned:
            return []

        sentences = re.split(
            r"(?<=[.!?])\s+",
            cleaned,
        )

        return [sentence.strip() for sentence in sentences if sentence.strip()]

    def _query_weights(
        self,
        package: EvidencePackage,
    ) -> dict[str, float]:
        """
        Assign higher weight to query terms that
        are less common across the retrieved
        evidence.

        For example, in a question about
        'iterative feedback', generic terms such
        as 'LLM' are likely common, while
        'iterative' and 'feedback' are more
        discriminating.
        """

        query_terms = list(dict.fromkeys(self._tokens(package.query)))

        if not query_terms:
            return {}

        documents = [set(self._tokens(evidence.text)) for evidence in package.evidence]

        document_count = max(
            len(documents),
            1,
        )

        frequencies = Counter()

        for document in documents:

            for term in query_terms:

                if term in document:

                    frequencies[term] += 1

        weights: dict[
            str,
            float,
        ] = {}

        for term in query_terms:

            document_frequency = frequencies[term]

            weights[term] = (
                math.log((document_count + 1) / (document_frequency + 1)) + 1.0
            )

        return weights

    def _focus_terms(
        self,
        package: EvidencePackage,
    ) -> set[str]:
        """
        Identify the strongest query concepts.

        Generic corpus vocabulary is already
        removed by _tokens(), leaving terms that
        are more useful for deciding whether a
        sentence directly addresses the question.
        """

        return set(self._tokens(package.query))

    def _best_sentence(
        self,
        text: str,
        query_weights: dict[
            str,
            float,
        ],
    ) -> tuple[str, float]:

        sentences = self._sentences(text)

        if not sentences:
            return "", 0.0

        best_sentence = ""
        best_score = 0.0

        for sentence in sentences:

            if self._is_front_matter_contaminated(sentence):
                continue

            sentence_tokens = set(self._tokens(sentence))

            score = sum(
                weight
                for term, weight in query_weights.items()
                if term in sentence_tokens
            )

            if score > best_score:

                best_sentence = sentence

                best_score = score

        return (
            best_sentence,
            best_score,
        )

    def generate(
        self,
        package: EvidencePackage,
    ) -> GeneratedDraft:

        if not package.query.strip():

            raise ValueError("Evidence package query " "cannot be empty")

        if not package.evidence:

            return GeneratedDraft(
                query=package.query,
                answer_text=(
                    "No validated evidence was " "available for this question."
                ),
                claims=[],
            )

        query_weights = self._query_weights(package)

        focus_terms = self._focus_terms(package)

        candidates: list[
            tuple[
                float,
                object,
                str,
            ]
        ] = []

        for evidence in package.evidence:

            sentence, score = self._best_sentence(
                text=evidence.text,
                query_weights=(query_weights),
            )

            sentence_tokens = set(self._tokens(sentence))

            has_focus_overlap = bool(sentence_tokens & focus_terms)

            if sentence and score >= self.min_relevance_score and has_focus_overlap:

                candidates.append(
                    (
                        score,
                        evidence,
                        sentence,
                    )
                )

        # Most question-relevant evidence first.
        candidates.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        candidates = candidates[: self.max_claims]

        claims: list[GeneratedClaim] = []

        rendered: list[str] = []

        for (
            _,
            evidence,
            sentence,
        ) in candidates:

            claim_id = f"C{len(claims) + 1}"

            claims.append(
                GeneratedClaim(
                    claim_id=claim_id,
                    text=sentence,
                    evidence_ids=[evidence.evidence_id],
                )
            )

            rendered.append(f"{sentence} " f"[{evidence.label}]")

        if not claims:

            return GeneratedDraft(
                query=package.query,
                answer_text=(
                    "Validated evidence was "
                    "retrieved, but no passage "
                    "was sufficiently relevant "
                    "to produce a grounded "
                    "deterministic claim."
                ),
                claims=[],
            )

        return GeneratedDraft(
            query=package.query,
            answer_text=" ".join(rendered),
            claims=claims,
        )

    def _is_front_matter_contaminated(
        self,
        sentence: str,
    ) -> bool:
        """
        Detect sentences contaminated by PDF title/author
        front matter before an abstract marker.

        These are extraction artifacts rather than clean
        research claims and should not be synthesized as
        grounded answer statements.
        """

        normalized = self._normalize(sentence)

        abstract_match = re.search(
            r"\babstract\b\s*[—–:-]",
            normalized,
            flags=re.IGNORECASE,
        )

        if not abstract_match:
            return False

        prefix = normalized[: abstract_match.start()].strip()

        return len(prefix.split()) >= 4
