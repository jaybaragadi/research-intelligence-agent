from src.analysis.comparison_findings import (
    ComparisonFindingBuilder,
)
from src.analysis.comparison_matrix import (
    ComparisonMatrixBuilder,
)
from src.analysis.comparison_models import (
    ComparativeAnalysis,
)
from src.analysis.evidence_classifier import (
    EvidenceDimensionClassifier,
)
from src.analysis.paper_profiler import (
    ComparativePaperProfiler,
)
from src.generation.evidence_package import (
    EvidencePackageBuilder,
)
from src.generation.query_focus import (
    build_comparison_focus_query,
)
from src.tools.compare_papers import (
    ComparePapersTool,
)


class ComparativeAnalysisService:
    """
    High-level deterministic comparative
    research-analysis service.
    """

    def __init__(
        self,
        compare_tool: ComparePapersTool | None = None,
        package_builder: EvidencePackageBuilder | None = None,
        classifier: EvidenceDimensionClassifier | None = None,
        profiler: ComparativePaperProfiler | None = None,
        matrix_builder: ComparisonMatrixBuilder | None = None,
        finding_builder: ComparisonFindingBuilder | None = None,
    ) -> None:

        self.compare_tool = (
            compare_tool if compare_tool is not None else ComparePapersTool()
        )

        self.package_builder = (
            package_builder if package_builder is not None else EvidencePackageBuilder()
        )

        self.classifier = (
            classifier if classifier is not None else EvidenceDimensionClassifier()
        )

        self.profiler = profiler if profiler is not None else ComparativePaperProfiler()

        self.matrix_builder = (
            matrix_builder if matrix_builder is not None else ComparisonMatrixBuilder()
        )

        self.finding_builder = (
            finding_builder
            if finding_builder is not None
            else ComparisonFindingBuilder()
        )

    def analyze(
        self,
        paper_ids: list[str],
        query: str,
        evidence_per_paper: int = 6,
    ) -> ComparativeAnalysis:

        cleaned_papers = list(
            dict.fromkeys(
                paper_id.strip() for paper_id in paper_ids if paper_id.strip()
            )
        )

        if len(cleaned_papers) < 2:

            raise ValueError("At least two unique paper IDs " "are required")

        if not query.strip():

            raise ValueError("Query cannot be empty")

        retrieval_query = build_comparison_focus_query(
            query=query,
            paper_ids=cleaned_papers,
        )

        comparison = self.compare_tool.compare(
            paper_ids=(cleaned_papers),
            query=(retrieval_query),
            evidence_per_paper=(evidence_per_paper),
        )

        package = self.package_builder.from_comparison(comparison)

        package.query = query

        classified = self.classifier.classify_many(package.evidence)

        profiles = self.profiler.build_profiles(
            requested_papers=(cleaned_papers),
            classified_evidence=(classified),
        )

        matrix = self.matrix_builder.build(
            requested_papers=(cleaned_papers),
            profiles=(profiles),
        )

        findings = self.finding_builder.build(matrix)

        return ComparativeAnalysis(
            query=query,
            requested_papers=(cleaned_papers),
            profiles=profiles,
            matrix=matrix,
            findings=findings,
        )
