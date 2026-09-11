from collections import defaultdict

from src.analysis.gap_models import (
    DimensionCoverage,
    GapCandidate,
    GapEvidence,
    GapSignalType,
    GapType,
)
from src.analysis.gap_scorer import (
    GapConfidenceScorer,
)


class GapCandidateDetector:
    """
    Build conservative research-gap candidates from
    validated explicit gap signals and corpus coverage.

    This detector does not claim universal literature gaps.

    It creates candidate observations only from the
    indexed corpus.
    """

    def __init__(
        self,
        scorer: GapConfidenceScorer | None = None,
    ):

        self.scorer = scorer or GapConfidenceScorer()

    def build_explicit_candidates(
        self,
        signals: list[GapEvidence],
    ) -> list[GapCandidate]:
        """
        Convert explicit gap-related evidence into
        candidate research gaps.

        Evidence is grouped by:

            paper_id
            signal_type

        Multiple evidence passages supporting the same
        signal type in one paper become one candidate.
        """

        grouped: dict[
            tuple[str, GapSignalType],
            list[GapEvidence],
        ] = defaultdict(list)

        for signal in signals:
            grouped[
                (
                    signal.paper_id,
                    signal.signal_type,
                )
            ].append(signal)

        candidates: list[GapCandidate] = []

        counter = 1

        for (
            paper_id,
            signal_type,
        ) in sorted(
            grouped,
            key=lambda item: (
                item[0],
                item[1].value,
            ),
        ):

            evidence = grouped[
                (
                    paper_id,
                    signal_type,
                )
            ]

            evidence_ids = self._unique_preserving_order(
                item.evidence_id for item in evidence
            )

            title = self._explicit_title(signal_type)

            description = self._explicit_description(
                paper_id=paper_id,
                signal_type=signal_type,
            )

            confidence = self.scorer.score_explicit(
                signal_type=signal_type,
                evidence=evidence,
            )

            candidates.append(
                GapCandidate(
                    gap_id=f"G{counter}",
                    gap_type=(GapType.EXPLICIT),
                    title=title,
                    description=description,
                    confidence=confidence,
                    paper_ids=[paper_id],
                    evidence_ids=(evidence_ids),
                    dimensions=[],
                    reason=(
                        "The indexed paper contains "
                        f"explicit {signal_type.value} "
                        "language supported by validated "
                        "evidence."
                    ),
                )
            )

            counter += 1

        return candidates

    def build_imbalance_candidates(
        self,
        coverage: list[DimensionCoverage],
        corpus_size: int,
        minimum_high_coverage_ratio: float = 0.5,
        maximum_low_coverage_ratio: float = 0.25,
    ) -> list[GapCandidate]:
        """
        Build conservative corpus-imbalance candidates.

        A candidate is created only when:

        1. corpus_size is large enough to compare;
        2. one dimension has meaningful representation;
        3. another dimension has low but non-zero coverage;
        4. the difference is substantial.

        Zero evidence is intentionally excluded because
        zero retrieved evidence is not proof of a gap.
        """

        if corpus_size < 2:
            return []

        if not (0 < minimum_high_coverage_ratio <= 1):
            raise ValueError("minimum_high_coverage_ratio " "must be between 0 and 1")

        if not (0 <= maximum_low_coverage_ratio < 1):
            raise ValueError("maximum_low_coverage_ratio " "must be between 0 and 1")

        if maximum_low_coverage_ratio >= minimum_high_coverage_ratio:
            raise ValueError(
                "maximum_low_coverage_ratio "
                "must be lower than "
                "minimum_high_coverage_ratio"
            )

        represented = [item for item in coverage if item.paper_count > 0]

        if len(represented) < 2:
            return []

        candidates: list[GapCandidate] = []

        counter = 1

        for low in represented:

            low_ratio = low.paper_count / corpus_size

            if low_ratio > maximum_low_coverage_ratio:
                continue

            stronger = [
                item
                for item in represented
                if (
                    item.dimension != low.dimension
                    and (item.paper_count / corpus_size) >= minimum_high_coverage_ratio
                )
            ]

            if not stronger:
                continue

            strongest = max(
                stronger,
                key=lambda item: (
                    item.paper_count,
                    item.evidence_count,
                    item.dimension,
                ),
            )

            high_ratio = strongest.paper_count / corpus_size

            if high_ratio <= low_ratio:
                continue

            evidence_ids = self._unique_preserving_order(
                [
                    *strongest.evidence_ids,
                    *low.evidence_ids,
                ]
            )

            paper_ids = self._unique_preserving_order(
                [
                    *strongest.paper_ids,
                    *low.paper_ids,
                ]
            )

            candidates.append(
                GapCandidate(
                    gap_id=(f"CI{counter}"),
                    gap_type=(GapType.CORPUS_IMBALANCE),
                    title=("Uneven corpus coverage: " f"{low.dimension}"),
                    description=(
                        f"The indexed corpus contains "
                        f"substantially less evidence for "
                        f"'{low.dimension}' than for "
                        f"'{strongest.dimension}'."
                    ),
                    confidence=(
                        self.scorer.score_imbalance(
                            high_paper_count=(strongest.paper_count),
                            low_paper_count=(low.paper_count),
                            corpus_size=corpus_size,
                        )
                    ),
                    paper_ids=paper_ids,
                    evidence_ids=(evidence_ids),
                    dimensions=[
                        strongest.dimension,
                        low.dimension,
                    ],
                    reason=(
                        f"{strongest.paper_count} of "
                        f"{corpus_size} papers contain "
                        f"evidence for "
                        f"'{strongest.dimension}', while "
                        f"{low.paper_count} of "
                        f"{corpus_size} contain evidence "
                        f"for '{low.dimension}'. This is "
                        "a corpus-level imbalance, not "
                        "proof of an external literature "
                        "gap."
                    ),
                )
            )

            counter += 1

        return candidates

    def _explicit_title(
        self,
        signal_type: GapSignalType,
    ) -> str:
        """
        Produce a neutral candidate title.
        """

        labels = {
            GapSignalType.LIMITATION: ("Explicit reported limitation"),
            GapSignalType.FUTURE_WORK: ("Explicit future-work direction"),
            GapSignalType.UNRESOLVED_PROBLEM: ("Explicit unresolved problem"),
            GapSignalType.UNDEREXPLORED_AREA: ("Explicit underexplored area"),
            GapSignalType.COVERAGE_IMBALANCE: ("Corpus coverage imbalance"),
        }

        return labels[signal_type]

    def _explicit_description(
        self,
        paper_id: str,
        signal_type: GapSignalType,
    ) -> str:
        """
        Produce a conservative explicit-candidate
        description.
        """

        return (
            f"Paper '{paper_id}' contains validated "
            f"evidence classified as "
            f"'{signal_type.value}'."
        )

    def _unique_preserving_order(
        self,
        values,
    ) -> list[str]:
        """
        Deduplicate while preserving first-seen order.
        """

        seen: set[str] = set()

        results: list[str] = []

        for value in values:

            if value in seen:
                continue

            seen.add(value)

            results.append(value)

        return results
