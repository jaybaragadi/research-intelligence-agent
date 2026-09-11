from src.analysis.comparison_models import (
    ComparativeAnalysis,
    DimensionEvidence,
    PaperAnalysisProfile,
    PaperDimensionAnalysis,
)
from src.analysis.gap_analysis_service import (
    ResearchGapAnalysisService,
)
from src.analysis.gap_models import (
    GapType,
)
from src.generation.models import (
    GroundingEvidence,
)


def make_dimension_evidence(
    evidence_id: str,
    paper_id: str,
    dimension: str,
    text: str,
) -> DimensionEvidence:

    return DimensionEvidence(
        evidence_id=evidence_id,
        paper_id=paper_id,
        dimension=dimension,
        page_number=2,
        section="discussion",
        text=text,
        citation_text="Citation",
        relevance_score=2.0,
    )


def make_grounding_evidence(
    evidence_id: str,
    paper_id: str,
    text: str,
) -> GroundingEvidence:

    return GroundingEvidence(
        evidence_id=evidence_id,
        label="E1",
        paper_id=paper_id,
        page_number=2,
        section="discussion",
        text=text,
        citation_text="Citation",
    )


class FakeComparativeService:

    def __init__(
        self,
        evidence: list[DimensionEvidence],
    ):

        self.evidence = evidence

    def analyze(
        self,
        paper_ids: list[str],
        query: str,
        evidence_per_paper: int = 8,
    ) -> ComparativeAnalysis:

        profiles = []

        for paper_id in paper_ids:

            paper_evidence = [
                item for item in self.evidence if item.paper_id == paper_id
            ]

            dimensions = {}

            for item in paper_evidence:

                dimensions.setdefault(
                    item.dimension,
                    [],
                ).append(item)

            profiles.append(
                PaperAnalysisProfile(
                    paper_id=paper_id,
                    dimensions=[
                        PaperDimensionAnalysis(
                            dimension=dimension,
                            evidence=items,
                        )
                        for (dimension, items) in dimensions.items()
                    ],
                )
            )

        return ComparativeAnalysis(
            query=query,
            requested_papers=paper_ids,
            profiles=profiles,
            matrix=[],
            findings=[],
        )


class FakeExplicitGapRetriever:

    def __init__(
        self,
        evidence: list[GroundingEvidence] | None = None,
    ) -> None:

        self.evidence = evidence or []

        self.calls = []

    def retrieve(
        self,
        paper_ids: list[str],
        evidence_per_query: int = 4,
    ) -> list[GroundingEvidence]:

        self.calls.append(
            {
                "paper_ids": (paper_ids),
                "evidence_per_query": (evidence_per_query),
            }
        )

        return list(self.evidence)


def test_service_requires_two_unique_papers():

    service = ResearchGapAnalysisService(
        comparative_service=(FakeComparativeService([])),
        explicit_gap_retriever=(FakeExplicitGapRetriever()),
    )

    try:

        service.analyze(
            paper_ids=[
                "paper_a",
                "paper_a",
            ],
            query="Find gaps",
        )

        assert False

    except ValueError as exc:

        assert "two unique papers" in str(exc)


def test_service_extracts_explicit_gap_signal():

    evidence = [
        make_dimension_evidence(
            evidence_id="comparison_e1",
            paper_id="paper_a",
            dimension="limitations",
            text=("The evaluation measures " "branch coverage."),
        )
    ]

    explicit_evidence = [
        make_grounding_evidence(
            evidence_id="e1",
            paper_id="paper_a",
            text=(
                "A limitation of our approach " "is the restricted evaluation scope."
            ),
        )
    ]

    service = ResearchGapAnalysisService(
        comparative_service=(FakeComparativeService(evidence)),
        explicit_gap_retriever=(FakeExplicitGapRetriever(explicit_evidence)),
    )

    result = service.analyze(
        paper_ids=[
            "paper_a",
            "paper_b",
        ],
        query="Find research gaps",
    )

    assert len(result.candidates) == 1

    assert result.candidates[0].gap_type == GapType.EXPLICIT

    assert result.candidates[0].evidence_ids == ["e1"]

    assert result.validation is not None

    assert result.validation.is_valid is True


def test_service_preserves_papers_without_signals():

    evidence = [
        make_dimension_evidence(
            evidence_id="comparison_e1",
            paper_id="paper_a",
            dimension="limitations",
            text=("The evaluation measures " "branch coverage."),
        )
    ]

    explicit_evidence = [
        make_grounding_evidence(
            evidence_id="e1",
            paper_id="paper_a",
            text=(
                "A limitation of our approach " "is the restricted evaluation scope."
            ),
        )
    ]

    service = ResearchGapAnalysisService(
        comparative_service=(FakeComparativeService(evidence)),
        explicit_gap_retriever=(FakeExplicitGapRetriever(explicit_evidence)),
    )

    result = service.analyze(
        paper_ids=[
            "paper_a",
            "paper_b",
        ],
        query="Find research gaps",
    )

    assert [item.paper_id for item in result.paper_signals] == [
        "paper_a",
        "paper_b",
    ]

    paper_b = result.paper_signals[1]

    assert paper_b.signals == []


def test_service_preserves_zero_dimension_coverage():

    service = ResearchGapAnalysisService(
        comparative_service=(FakeComparativeService([])),
        explicit_gap_retriever=(FakeExplicitGapRetriever()),
    )

    result = service.analyze(
        paper_ids=[
            "paper_a",
            "paper_b",
        ],
        query="Find research gaps",
    )

    lookup = {item.dimension: item for item in result.dimension_coverage}

    assert "limitations" in lookup

    assert lookup["limitations"].paper_count == 0


def test_duplicate_explicit_evidence_is_not_duplicate_signal():

    shared_text = (
        "In future work, we plan to investigate " "additional programming languages."
    )

    explicit_evidence = [
        make_grounding_evidence(
            evidence_id="e1",
            paper_id="paper_a",
            text=shared_text,
        ),
        make_grounding_evidence(
            evidence_id="e1",
            paper_id="paper_a",
            text=shared_text,
        ),
    ]

    service = ResearchGapAnalysisService(
        comparative_service=(FakeComparativeService([])),
        explicit_gap_retriever=(FakeExplicitGapRetriever(explicit_evidence)),
    )

    result = service.analyze(
        paper_ids=[
            "paper_a",
            "paper_b",
        ],
        query="Find research gaps",
    )

    signals = result.paper_signals[0].signals

    assert len(signals) == 1

    assert signals[0].evidence_id == "e1"


def test_service_can_create_corpus_imbalance():

    evidence = []

    for index in range(
        1,
        9,
    ):

        evidence.append(
            make_dimension_evidence(
                evidence_id=(f"q{index}"),
                paper_id=(f"p{index}"),
                dimension=("quality_objective"),
                text=("The evaluation measures " "branch coverage."),
            )
        )

    for index in range(
        1,
        3,
    ):

        evidence.append(
            make_dimension_evidence(
                evidence_id=(f"l{index}"),
                paper_id=(f"p{index}"),
                dimension="limitations",
                text=("The discussion describes " "study constraints."),
            )
        )

    papers = [
        f"p{index}"
        for index in range(
            1,
            11,
        )
    ]

    service = ResearchGapAnalysisService(
        comparative_service=(FakeComparativeService(evidence)),
        explicit_gap_retriever=(FakeExplicitGapRetriever()),
    )

    result = service.analyze(
        paper_ids=papers,
        query="Find research gaps",
    )

    imbalance = [
        candidate
        for candidate in result.candidates
        if (candidate.gap_type == GapType.CORPUS_IMBALANCE)
    ]

    assert len(imbalance) >= 1

    assert result.validation is not None

    assert result.validation.is_valid is True


def test_service_uses_dedicated_explicit_gap_evidence():

    comparative_evidence = [
        make_dimension_evidence(
            evidence_id="comparison_e1",
            paper_id="paper_a",
            dimension="limitations",
            text=("The evaluation measures " "branch coverage."),
        )
    ]

    explicit_evidence = [
        make_grounding_evidence(
            evidence_id="gap_e1",
            paper_id="paper_a",
            text=(
                "In future work, we plan "
                "to investigate additional "
                "programming languages."
            ),
        )
    ]

    service = ResearchGapAnalysisService(
        comparative_service=(FakeComparativeService(comparative_evidence)),
        explicit_gap_retriever=(FakeExplicitGapRetriever(explicit_evidence)),
    )

    result = service.analyze(
        paper_ids=[
            "paper_a",
            "paper_b",
        ],
        query="Find research gaps",
    )

    explicit = [
        candidate
        for candidate in result.candidates
        if (candidate.gap_type == GapType.EXPLICIT)
    ]

    assert len(explicit) == 1

    assert explicit[0].evidence_ids == ["gap_e1"]


def test_validator_accepts_dedicated_gap_evidence():

    explicit_evidence = [
        make_grounding_evidence(
            evidence_id="gap_e1",
            paper_id="paper_a",
            text=("A limitation of our approach " "is the restricted dataset."),
        )
    ]

    service = ResearchGapAnalysisService(
        comparative_service=(FakeComparativeService([])),
        explicit_gap_retriever=(FakeExplicitGapRetriever(explicit_evidence)),
    )

    result = service.analyze(
        paper_ids=[
            "paper_a",
            "paper_b",
        ],
        query="Find research gaps",
    )

    assert result.validation is not None

    assert result.validation.is_valid is True

    assert result.validation.issue_count == 0
