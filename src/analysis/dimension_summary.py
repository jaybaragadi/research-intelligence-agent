import re

from src.analysis.comparison_dimensions import (
    COMPARISON_DIMENSIONS,
)
from src.analysis.comparison_models import (
    DimensionEvidence,
)


class DimensionSummarySelector:
    """
    Select the sentence from classified evidence
    that best represents one comparison dimension.

    This remains fully extractive:
    no new factual content is generated.
    """

    def __init__(self) -> None:

        self._dimension_map = {
            dimension.name: dimension for dimension in COMPARISON_DIMENSIONS
        }

    def _normalize(
        self,
        text: str,
    ) -> str:

        text = re.sub(
            r"\s+",
            " ",
            text.strip(),
        )

        # Repair a few common PDF extraction
        # punctuation-spacing problems.
        text = re.sub(
            r"([,;:])(?=[A-Za-z])",
            r"\1 ",
            text,
        )

        text = re.sub(
            r"\.(?=[A-Z])",
            ". ",
            text,
        )

        return text

    def _sentences(
        self,
        text: str,
    ) -> list[str]:

        normalized = self._normalize(text)

        if not normalized:
            return []

        sentences = re.split(
            r"(?<=[.!?])\s+",
            normalized,
        )

        return [sentence.strip() for sentence in sentences if sentence.strip()]

    def _score_sentence(
        self,
        sentence: str,
        dimension: str,
    ) -> float:

        definition = self._dimension_map.get(dimension)

        if definition is None:
            return 0.0

        normalized = sentence.lower()

        score = 0.0

        for keyword in definition.keywords:

            keyword_normalized = keyword.lower()

            if keyword_normalized not in normalized:
                continue

            word_count = len(keyword_normalized.split())

            score += 1.0 if word_count == 1 else 2.0

        return score

    def select(
        self,
        dimension: str,
        evidence: list[DimensionEvidence],
    ) -> tuple[
        str | None,
        list[str],
    ]:
        """
        Return:
            selected sentence,
            supporting evidence IDs.

        Only the evidence source containing the
        chosen sentence is attached to the cell.
        """

        best_sentence: str | None = None
        best_evidence_id: str | None = None
        best_score = 0.0

        for item in evidence:

            for sentence in self._sentences(item.text):

                score = self._score_sentence(
                    sentence=sentence,
                    dimension=dimension,
                )

                if score > best_score:

                    best_score = score

                    best_sentence = sentence

                    best_evidence_id = item.evidence_id

        if best_sentence is None or best_evidence_id is None:

            return None, []

        return (
            best_sentence,
            [best_evidence_id],
        )
