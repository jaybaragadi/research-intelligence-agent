import re

from src.analysis.gap_models import (
    GapEvidence,
    GapSignalType,
)
from src.analysis.gap_taxonomy import (
    GAP_SIGNAL_DEFINITIONS,
)
from src.generation.models import (
    GroundingEvidence,
)


class ExplicitGapSignalExtractor:
    """
    Extract explicit research-gap signals from
    validated evidence passages.

    This extractor is deliberately conservative.

    It only creates GapEvidence when one of the
    configured strong taxonomy phrases is present.

    It does not infer a research gap merely because
    evidence is absent or because a passage contains
    generic words such as:

        limited
        challenge
        failure
        coverage
    """

    def _normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalize whitespace and case for
        deterministic phrase matching.
        """

        return re.sub(
            r"\s+",
            " ",
            text.lower().strip(),
        )

    def _normalize_section(
        self,
        section: str | None,
    ) -> str | None:
        """
        Normalize section labels so they can be
        compared with taxonomy preferred sections.
        """

        if not section:
            return None

        return section.lower().strip().replace(" ", "_")

    def _phrase_score(
        self,
        text: str,
        phrases: tuple[str, ...],
    ) -> float:
        """
        Score explicit phrase matches.

        Longer multi-word phrases receive more
        weight because they are less ambiguous.
        """

        normalized = self._normalize(text)

        score = 0.0

        for phrase in phrases:

            normalized_phrase = phrase.lower()

            if normalized_phrase not in normalized:
                continue

            word_count = len(normalized_phrase.split())

            if word_count >= 4:
                score += 2.0

            elif word_count >= 2:
                score += 1.5

            else:
                score += 1.0

        return score

    def _section_bonus(
        self,
        section: str | None,
        preferred_sections: tuple[str, ...],
    ) -> float:
        """
        Add a small ranking bonus for evidence found
        in sections naturally associated with explicit
        gap statements.

        This does not create a signal by itself.
        """

        normalized_section = self._normalize_section(section)

        if normalized_section is None or normalized_section not in preferred_sections:
            return 0.0

        return 0.5

    def _has_future_work_action(
        self,
        text: str,
    ) -> bool:
        """
        Determine whether future-work language
        expresses an actual research action or
        direction.

        Merely mentioning "future work" or
        "future research" is not sufficient.

        Examples that should qualify:

        - we plan to investigate ...
        - future work can explore ...
        - further research is needed ...
        - remains part of our future work
        - another area of future work is ...

        Examples that should not qualify:

        - Section 8 discusses future work.
        - data was released to facilitate
          future research.
        """

        normalized = self._normalize(text)

        action_patterns = (
            "we plan to",
            "we intend to",
            "we aim to",
            "we will investigate",
            "we will explore",
            "future work can",
            "future work could",
            "future work should",
            "future work will",
            "future work is to",
            "future research can",
            "future research could",
            "future research should",
            "future research is needed",
            "further research is needed",
            "future direction is",
            "future directions include",
            "another area of future work is",
            "an area of future work is",
            "promising direction for future work",
            "promising direction for future research",
            "remains part of our future work",
            "remain part of our future work",
            "we see it as our future work",
            "we consider this future work",
        )

        return any(pattern in normalized for pattern in action_patterns)

    def extract(
        self,
        evidence: GroundingEvidence,
        minimum_score: float = 1.5,
    ) -> list[GapEvidence]:
        """
        Extract all explicit gap signals supported
        by one validated evidence passage.

        One passage may support multiple signal types.

        Example:

            "A limitation of our approach is X.
             Future work will investigate Y."

        may produce:

            LIMITATION
            FUTURE_WORK
        """

        if minimum_score <= 0:
            raise ValueError("minimum_score must be positive")

        results: list[GapEvidence] = []

        for definition in GAP_SIGNAL_DEFINITIONS:

            phrase_score = self._phrase_score(
                text=evidence.text,
                phrases=(definition.phrases),
            )

            if phrase_score < minimum_score:
                continue

            if (
                definition.signal_type == GapSignalType.FUTURE_WORK
                and not self._has_future_work_action(evidence.text)
            ):
                continue

            score = phrase_score

            score += self._section_bonus(
                section=evidence.section,
                preferred_sections=(definition.preferred_sections),
            )

            results.append(
                GapEvidence(
                    evidence_id=(evidence.evidence_id),
                    paper_id=(evidence.paper_id),
                    page_number=(evidence.page_number),
                    section=(evidence.section),
                    signal_type=(definition.signal_type),
                    text=(evidence.text),
                    citation_text=(evidence.citation_text),
                    relevance_score=(score),
                )
            )

        return results

    def extract_many(
        self,
        evidence_items: list[GroundingEvidence],
    ) -> list[GapEvidence]:
        """
        Extract explicit gap signals from multiple
        validated evidence passages.
        """

        results: list[GapEvidence] = []

        for evidence in evidence_items:

            results.extend(self.extract(evidence))

        return results
