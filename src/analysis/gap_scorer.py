from src.analysis.gap_models import (
    GapConfidence,
    GapEvidence,
    GapSignalType,
)


class GapConfidenceScorer:
    """
    Deterministically assign confidence to
    research-gap candidates.

    Confidence reflects support inside the
    indexed corpus only.

    It must not be interpreted as confidence
    that a gap exists across all published
    scientific literature.
    """

    def score_explicit(
        self,
        signal_type: GapSignalType,
        evidence: list[GapEvidence],
    ) -> GapConfidence:
        """
        Score an explicit candidate.

        Explicit limitation and future-work
        statements receive stronger confidence
        when supported by strong phrase matches.

        Unresolved-problem statements are treated
        more conservatively.
        """

        if not evidence:
            return GapConfidence.LOW

        strongest_score = max(item.relevance_score for item in evidence)

        evidence_count = len({item.evidence_id for item in evidence})

        if signal_type in {
            GapSignalType.LIMITATION,
            GapSignalType.FUTURE_WORK,
        }:

            if strongest_score >= 2.0 and evidence_count >= 1:
                return GapConfidence.HIGH

        if signal_type == GapSignalType.UNRESOLVED_PROBLEM:

            if strongest_score >= 2.0 and evidence_count >= 2:
                return GapConfidence.HIGH

        if strongest_score >= 1.5:
            return GapConfidence.MEDIUM

        return GapConfidence.LOW

    def score_imbalance(
        self,
        high_paper_count: int,
        low_paper_count: int,
        corpus_size: int,
    ) -> GapConfidence:
        """
        Score a corpus-imbalance candidate.

        Confidence depends on the observed
        difference in paper coverage.

        Both dimensions must have non-zero
        representation before this scorer is
        meaningful.
        """

        if corpus_size <= 0:
            raise ValueError("corpus_size must be positive")

        if high_paper_count < 0:
            raise ValueError("high_paper_count cannot be negative")

        if low_paper_count < 0:
            raise ValueError("low_paper_count cannot be negative")

        if high_paper_count > corpus_size or low_paper_count > corpus_size:
            raise ValueError("paper counts cannot exceed corpus_size")

        if high_paper_count == 0 or low_paper_count == 0:
            return GapConfidence.LOW

        high_ratio = high_paper_count / corpus_size

        low_ratio = low_paper_count / corpus_size

        difference = high_ratio - low_ratio

        if difference >= 0.6:
            return GapConfidence.HIGH

        if difference >= 0.35:
            return GapConfidence.MEDIUM

        return GapConfidence.LOW
