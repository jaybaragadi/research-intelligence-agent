import re

from src.analysis.comparison_dimensions import (
    COMPARISON_DIMENSIONS,
    ComparisonDimension,
)
from src.analysis.comparison_models import (
    DimensionEvidence,
)
from src.generation.models import (
    GroundingEvidence,
)

SECTION_BONUSES = {
    "evaluation_method": {
        "evaluation",
        "experimental_setup",
        "experiments",
        "results",
    },
    "limitations": {
        "limitations",
        "threats",
        "threats_to_validity",
        "discussion",
    },
    "generation_strategy": {
        "methodology",
        "method",
        "approach",
    },
    "feedback_signal": {
        "methodology",
        "method",
        "approach",
    },
    "iteration_strategy": {
        "methodology",
        "method",
        "approach",
    },
}


class EvidenceDimensionClassifier:
    """
    Deterministically classify validated evidence
    passages into analytical comparison dimensions.

    Classification is based on:

    1. Dimension-specific keyword signals.
    2. Section-aware relevance bonuses.
    3. Dimension-specific semantic gates where
       broad keyword matching would otherwise create
       misleading classifications.

    A single evidence passage may support more than
    one analytical dimension.
    """

    def _normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalize whitespace and casing for
        deterministic matching.
        """

        return re.sub(
            r"\s+",
            " ",
            text.lower().strip(),
        )

    def _keyword_score(
        self,
        text: str,
        dimension: ComparisonDimension,
    ) -> float:
        """
        Score a passage according to the number
        of dimension-specific keyword matches.

        Multi-word phrases receive slightly more
        weight than individual words because they
        generally carry stronger analytical meaning.
        """

        normalized = self._normalize(text)

        score = 0.0

        for keyword in dimension.keywords:

            normalized_keyword = keyword.lower()

            if normalized_keyword not in normalized:
                continue

            word_count = len(normalized_keyword.split())

            score += 1.0 if word_count == 1 else 1.5

        return score

    def _section_bonus(
        self,
        section: str | None,
        dimension: str,
    ) -> float:
        """
        Give a small preference to evidence found
        in sections that are naturally associated
        with a comparison dimension.

        This is only a ranking bonus.

        Evidence from other sections remains valid
        and may still be classified.
        """

        if not section:
            return 0.0

        normalized = section.lower().strip().replace(" ", "_")

        preferred_sections = SECTION_BONUSES.get(
            dimension,
            set(),
        )

        if normalized in preferred_sections:
            return 0.75

        return 0.0

    def _passes_dimension_gate(
        self,
        text: str,
        dimension: str,
    ) -> bool:
        """
        Apply stricter rules to dimensions where
        broad lexical matching could create a
        misleading analytical conclusion.

        Currently limitations requires language
        indicating a limitation of the paper,
        approach, method, study, system, or framework.

        For example:

            "limitations of test cases"

        should not automatically be interpreted as:

            "limitations of MuTAP"
        """

        normalized = self._normalize(text)

        if dimension != "limitations":
            return True

        limitation_patterns = (
            (
                r"\blimitation of (?:our|the) "
                r"(?:approach|method|study|system|framework)\b"
            ),
            (
                r"\blimitations of (?:our|the) "
                r"(?:approach|method|study|system|framework)\b"
            ),
            (
                r"\bour (?:approach|method|study|system|framework) "
                r"(?:is|has|cannot|does not)\b"
            ),
            r"\bthreat to validity\b",
            r"\bthreats to validity\b",
            (
                r"\bdrawback of (?:our|the) "
                r"(?:approach|method|study|system|framework)\b"
            ),
            (
                r"\bdrawbacks of (?:our|the) "
                r"(?:approach|method|study|system|framework)\b"
            ),
            r"\bfuture work\b",
        )

        return any(
            re.search(
                pattern,
                normalized,
            )
            for pattern in limitation_patterns
        )

    def classify(
        self,
        evidence: GroundingEvidence,
        minimum_score: float = 1.0,
    ) -> list[DimensionEvidence]:
        """
        Classify one validated evidence passage.

        A passage may support multiple dimensions.

        Only classifications satisfying both the
        relevance score and any dimension-specific
        gate are returned.
        """

        if minimum_score <= 0:
            raise ValueError("minimum_score must be positive")

        results: list[DimensionEvidence] = []

        for dimension in COMPARISON_DIMENSIONS:

            score = self._keyword_score(
                text=evidence.text,
                dimension=dimension,
            )

            score += self._section_bonus(
                section=evidence.section,
                dimension=dimension.name,
            )

            if score < minimum_score:
                continue

            if not self._passes_dimension_gate(
                text=evidence.text,
                dimension=dimension.name,
            ):
                continue

            results.append(
                DimensionEvidence(
                    evidence_id=(evidence.evidence_id),
                    paper_id=(evidence.paper_id),
                    dimension=(dimension.name),
                    page_number=(evidence.page_number),
                    section=(evidence.section),
                    text=(evidence.text),
                    citation_text=(evidence.citation_text),
                    relevance_score=(score),
                )
            )

        return results

    def classify_many(
        self,
        evidence_items: list[GroundingEvidence],
    ) -> list[DimensionEvidence]:
        """
        Classify multiple validated evidence
        passages while preserving all supported
        paper/dimension relationships.
        """

        classified: list[DimensionEvidence] = []

        for evidence in evidence_items:

            classified.extend(self.classify(evidence))

        return classified
