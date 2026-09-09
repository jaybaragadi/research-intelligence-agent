from collections import defaultdict

from src.analysis.comparison_dimensions import (
    COMPARISON_DIMENSIONS,
)

from src.analysis.comparative_service import (
    ComparativeAnalysisService,
)

from src.analysis.corpus_coverage import (
    CorpusCoverageAnalyzer,
)

from src.analysis.explicit_gap_retriever import (
    ExplicitGapEvidenceRetriever,
)

from src.analysis.gap_candidate_detector import (
    GapCandidateDetector,
)

from src.analysis.gap_models import (
    GapCandidate,
    GapEvidence,
    PaperGapSignals,
    ResearchGapAnalysis,
)

from src.analysis.gap_signal_extractor import (
    ExplicitGapSignalExtractor,
)

from src.analysis.gap_validator import (
    GapValidator,
)


class ResearchGapAnalysisService:
    """
    Coordinate evidence-grounded research-gap
    analysis across the indexed paper corpus.

    The service reuses Phase 9 comparative analysis
    as the source of validated, dimension-classified
    corpus evidence.

    It does not claim universal literature gaps.
    Results describe evidence found in the indexed
    corpus only.
    """

    def __init__(
        self,
        comparative_service: (
            ComparativeAnalysisService
            | None
        ) = None,
        explicit_gap_retriever: (
            ExplicitGapEvidenceRetriever
            | None
        ) = None,
        signal_extractor: (
            ExplicitGapSignalExtractor
            | None
        ) = None,
        coverage_analyzer: (
            CorpusCoverageAnalyzer
            | None
        ) = None,
        candidate_detector: (
            GapCandidateDetector
            | None
        ) = None,
        validator: (
            GapValidator
            | None
        ) = None,
    ):

        self.comparative_service = (
            comparative_service
            or ComparativeAnalysisService()
        )

        self.explicit_gap_retriever = (
            explicit_gap_retriever
            or ExplicitGapEvidenceRetriever()
        )

        self.signal_extractor = (
            signal_extractor
            or ExplicitGapSignalExtractor()
        )

        self.coverage_analyzer = (
            coverage_analyzer
            or CorpusCoverageAnalyzer()
        )

        self.candidate_detector = (
            candidate_detector
            or GapCandidateDetector()
        )

        self.validator = (
            validator
            or GapValidator()
        )

    def analyze(
        self,
        paper_ids: list[str],
        query: str,
        evidence_per_paper: int = 8,
    ) -> ResearchGapAnalysis:
        """
        Run complete corpus-level gap analysis.

        Steps:

        1. validate request;
        2. obtain comparative corpus evidence;
        3. retrieve explicit gap evidence;
        4. deduplicate explicit gap evidence;
        5. extract explicit gap signals;
        6. measure dimension coverage;
        7. create candidate gaps;
        8. validate candidate provenance.
        """

        cleaned_papers = (
            self._clean_paper_ids(
                paper_ids
            )
        )

        cleaned_query = query.strip()

        if not cleaned_query:
            raise ValueError(
                "query cannot be empty"
            )

        if len(cleaned_papers) < 2:
            raise ValueError(
                "gap analysis requires at least "
                "two unique papers"
            )

        if evidence_per_paper <= 0:
            raise ValueError(
                "evidence_per_paper must be positive"
            )

        comparative = (
            self.comparative_service
            .analyze(
                paper_ids=cleaned_papers,
                query=cleaned_query,
                evidence_per_paper=(
                    evidence_per_paper
                ),
            )
        )

        dimension_evidence = [
            evidence
            for profile
            in comparative.profiles
            for dimension
            in profile.dimensions
            for evidence
            in dimension.evidence
        ]

        explicit_evidence = (
            self.explicit_gap_retriever
            .retrieve(
                paper_ids=cleaned_papers,
                evidence_per_query=4,
            )
        )

        explicit_evidence = (
            self._dedupe_explicit_evidence(
                explicit_evidence
            )
        )

        explicit_signals = (
            self.signal_extractor
            .extract_many(
                explicit_evidence
            )
        )

        paper_signals = (
            self._group_paper_signals(
                cleaned_papers,
                explicit_signals,
            )
        )

        dimensions = [
            definition.name
            for definition
            in COMPARISON_DIMENSIONS
        ]

        dimension_coverage = (
            self.coverage_analyzer
            .analyze_for_dimensions(
                evidence=dimension_evidence,
                dimensions=dimensions,
            )
        )

        explicit_candidates = (
            self.candidate_detector
            .build_explicit_candidates(
                explicit_signals
            )
        )

        imbalance_candidates = (
            self.candidate_detector
            .build_imbalance_candidates(
                coverage=dimension_coverage,
                corpus_size=len(
                    cleaned_papers
                ),
            )
        )

        candidates = (
            self._renumber_candidates(
                [
                    *explicit_candidates,
                    *imbalance_candidates,
                ]
            )
        )

        available_evidence_ids = {
            evidence.evidence_id
            for evidence
            in dimension_evidence
        }

        available_evidence_ids.update(
            evidence.evidence_id
            for evidence
            in explicit_evidence
        )

        validation = (
            self.validator.validate(
                candidates=candidates,
                available_evidence_ids=(
                    available_evidence_ids
                ),
            )
        )

        return ResearchGapAnalysis(
            query=cleaned_query,

            corpus_papers=(
                cleaned_papers
            ),

            paper_signals=(
                paper_signals
            ),

            dimension_coverage=(
                dimension_coverage
            ),

            candidates=candidates,

            validation=validation,
        )

    def _dedupe_explicit_evidence(
        self,
        evidence,
    ):
        """
        Deduplicate explicit-gap evidence by
        evidence ID while preserving retrieval
        order.

        The dedicated retriever already performs
        deduplication, but the service also protects
        itself because injected/custom retrievers
        may return duplicate evidence records.
        """

        seen: set[str] = set()

        results = []

        for item in evidence:

            if item.evidence_id in seen:
                continue

            seen.add(
                item.evidence_id
            )

            results.append(
                item
            )

        return results

    def _group_paper_signals(
        self,
        paper_ids: list[str],
        signals: list[GapEvidence],
    ) -> list[PaperGapSignals]:
        """
        Group explicit signals by paper while
        preserving requested corpus order.

        Papers with no explicit signal are retained.
        """

        grouped: dict[
            str,
            list[GapEvidence],
        ] = defaultdict(list)

        for signal in signals:
            grouped[
                signal.paper_id
            ].append(
                signal
            )

        return [
            PaperGapSignals(
                paper_id=paper_id,
                signals=grouped.get(
                    paper_id,
                    [],
                ),
            )
            for paper_id in paper_ids
        ]

    def _renumber_candidates(
        self,
        candidates: list[
            GapCandidate
        ],
    ) -> list[GapCandidate]:
        """
        Give the final combined candidate collection
        unique deterministic IDs.

        Individual detectors may generate IDs in
        separate namespaces. The service owns the
        final output contract.
        """

        for index, candidate in enumerate(
            candidates,
            start=1,
        ):

            candidate.gap_id = (
                f"G{index}"
            )

        return candidates

    def _clean_paper_ids(
        self,
        paper_ids: list[str],
    ) -> list[str]:
        """
        Remove blanks and duplicates while
        preserving requested order.
        """

        seen: set[str] = set()

        results: list[str] = []

        for paper_id in paper_ids:

            cleaned = (
                paper_id.strip()
            )

            if (
                not cleaned
                or cleaned in seen
            ):
                continue

            seen.add(
                cleaned
            )

            results.append(
                cleaned
            )

        return results