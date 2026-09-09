from collections import defaultdict

from src.analysis.comparison_models import (
    DimensionEvidence,
)

from src.analysis.gap_models import (
    DimensionCoverage,
)


class CorpusCoverageAnalyzer:
    """
    Analyze how validated comparative evidence
    is distributed across the indexed research corpus.

    This class measures evidence coverage only.

    It does NOT interpret low coverage as a research gap.
    """

    def analyze(
        self,
        evidence: list[DimensionEvidence],
    ) -> list[DimensionCoverage]:
        """
        Build corpus-level coverage statistics
        for every represented analytical dimension.

        Results are deterministic and sorted
        alphabetically by dimension.
        """

        grouped: dict[
            str,
            list[DimensionEvidence],
        ] = defaultdict(list)

        for item in evidence:
            grouped[item.dimension].append(
                item
            )

        results: list[
            DimensionCoverage
        ] = []

        for dimension in sorted(
            grouped
        ):

            items = grouped[
                dimension
            ]

            paper_ids = (
                self._unique_preserving_order(
                    item.paper_id
                    for item in items
                )
            )

            evidence_ids = (
                self._unique_preserving_order(
                    item.evidence_id
                    for item in items
                )
            )

            results.append(
                DimensionCoverage(
                    dimension=dimension,

                    paper_count=len(
                        paper_ids
                    ),

                    evidence_count=len(
                        evidence_ids
                    ),

                    paper_ids=paper_ids,

                    evidence_ids=(
                        evidence_ids
                    ),
                )
            )

        return results

    def analyze_for_dimensions(
        self,
        evidence: list[DimensionEvidence],
        dimensions: list[str],
    ) -> list[DimensionCoverage]:
        """
        Build coverage for a requested dimension set.

        Missing dimensions are represented explicitly
        with zero evidence rather than silently omitted.

        This distinction becomes important later when
        candidate-gap logic evaluates corpus coverage.
        """

        cleaned_dimensions = (
            self._unique_preserving_order(
                dimension.strip()
                for dimension
                in dimensions
                if dimension.strip()
            )
        )

        grouped: dict[
            str,
            list[DimensionEvidence],
        ] = defaultdict(list)

        requested = set(
            cleaned_dimensions
        )

        for item in evidence:

            if (
                item.dimension
                not in requested
            ):
                continue

            grouped[
                item.dimension
            ].append(
                item
            )

        results: list[
            DimensionCoverage
        ] = []

        for dimension in (
            cleaned_dimensions
        ):

            items = grouped.get(
                dimension,
                [],
            )

            paper_ids = (
                self._unique_preserving_order(
                    item.paper_id
                    for item in items
                )
            )

            evidence_ids = (
                self._unique_preserving_order(
                    item.evidence_id
                    for item in items
                )
            )

            results.append(
                DimensionCoverage(
                    dimension=dimension,

                    paper_count=len(
                        paper_ids
                    ),

                    evidence_count=len(
                        evidence_ids
                    ),

                    paper_ids=paper_ids,

                    evidence_ids=(
                        evidence_ids
                    ),
                )
            )

        return results

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

            seen.add(
                value
            )

            results.append(
                value
            )

        return results