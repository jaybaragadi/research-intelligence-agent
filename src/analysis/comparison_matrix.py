from src.analysis.comparison_dimensions import (
    COMPARISON_DIMENSIONS,
)

from src.analysis.comparison_models import (
    ComparisonCell,
    ComparisonRow,
    PaperAnalysisProfile,
)

from src.analysis.dimension_summary import (
    DimensionSummarySelector,
)


class ComparisonMatrixBuilder:
    """
    Convert per-paper analytical profiles into
    a dimension-by-paper matrix.
    """

    def __init__(
        self,
        max_evidence_per_cell: int = 2,
        summary_selector: (
            DimensionSummarySelector
            | None
        ) = None,
    ) -> None:

        if (
            max_evidence_per_cell
            <= 0
        ):

            raise ValueError(
                "max_evidence_per_cell "
                "must be positive"
            )

        self.max_evidence_per_cell = (
            max_evidence_per_cell
        )

        self.summary_selector = (
            summary_selector
            if summary_selector is not None
            else DimensionSummarySelector()
        )

    def build(
        self,
        requested_papers: list[str],
        profiles: list[
            PaperAnalysisProfile
        ],
    ) -> list[ComparisonRow]:

        profile_map = {
            profile.paper_id: profile
            for profile in profiles
        }

        rows: list[
            ComparisonRow
        ] = []

        for definition in (
            COMPARISON_DIMENSIONS
        ):

            cells: list[
                ComparisonCell
            ] = []

            for paper_id in (
                requested_papers
            ):

                profile = (
                    profile_map.get(
                        paper_id
                    )
                )

                evidence = []

                if profile is not None:

                    dimension = next(
                        (
                            item
                            for item
                            in profile.dimensions
                            if (
                                item.dimension
                                == definition.name
                            )
                        ),
                        None,
                    )

                    if dimension is not None:

                        evidence = (
                            dimension.evidence[
                                :self.max_evidence_per_cell
                            ]
                        )

                summary, evidence_ids = (
                    self.summary_selector.select(
                        dimension=(
                            definition.name
                        ),

                        evidence=evidence,
                    )
                )

                cells.append(
                    ComparisonCell(
                        paper_id=paper_id,

                        dimension=(
                            definition.name
                        ),

                        summary=summary,

                        evidence_ids=(
                            evidence_ids
                        ),
                    )
                )

            rows.append(
                ComparisonRow(
                    dimension=(
                        definition.name
                    ),

                    cells=cells,
                )
            )

        return rows