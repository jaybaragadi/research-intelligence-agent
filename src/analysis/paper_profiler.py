from collections import defaultdict

from src.analysis.comparison_models import (
    DimensionEvidence,
    PaperAnalysisProfile,
    PaperDimensionAnalysis,
)


class ComparativePaperProfiler:
    """
    Group dimension-classified evidence into
    structured analytical profiles by paper.
    """

    def build_profiles(
        self,
        requested_papers: list[str],
        classified_evidence: list[DimensionEvidence],
    ) -> list[PaperAnalysisProfile]:

        grouped: dict[
            str,
            dict[
                str,
                list[DimensionEvidence],
            ],
        ] = defaultdict(lambda: defaultdict(list))

        for item in classified_evidence:

            grouped[item.paper_id][item.dimension].append(item)

        profiles: list[PaperAnalysisProfile] = []

        for paper_id in requested_papers:

            dimensions: list[PaperDimensionAnalysis] = []

            for dimension_name in sorted(grouped[paper_id].keys()):

                evidence = sorted(
                    grouped[paper_id][dimension_name],
                    key=lambda item: (
                        -item.relevance_score,
                        item.page_number,
                        item.evidence_id,
                    ),
                )

                dimensions.append(
                    PaperDimensionAnalysis(
                        dimension=(dimension_name),
                        evidence=evidence,
                    )
                )

            profiles.append(
                PaperAnalysisProfile(
                    paper_id=paper_id,
                    dimensions=dimensions,
                )
            )

        return profiles
