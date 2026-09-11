from src.analysis.explicit_gap_retriever import (
    EXPLICIT_GAP_QUERIES,
    ExplicitGapEvidenceRetriever,
)
from src.generation.models import (
    EvidencePackage,
    GroundingEvidence,
)
from src.tools.search_papers import (
    PaperSearchResponse,
)


def make_evidence(
    evidence_id: str,
    paper_id: str,
) -> GroundingEvidence:

    return GroundingEvidence(
        evidence_id=evidence_id,
        label="E1",
        paper_id=paper_id,
        page_number=5,
        section="conclusion",
        text=("In future work, we plan " "to investigate this area."),
        citation_text=(f"{paper_id}, p. 5"),
    )


class FakeSearchTool:

    def __init__(self) -> None:

        self.calls = []

    def search(
        self,
        query: str,
        top_k: int | None = None,
        allowed_paper_ids: set[str] | None = None,
        max_per_paper: int | None = None,
    ) -> PaperSearchResponse:

        self.calls.append(
            {
                "query": query,
                "top_k": top_k,
                "allowed_paper_ids": (allowed_paper_ids),
                "max_per_paper": (max_per_paper),
            }
        )

        return PaperSearchResponse(
            query=query,
            result_count=0,
            results=[],
        )


class FakePackageBuilder:

    def __init__(
        self,
        evidence_by_query=None,
    ) -> None:

        self.evidence_by_query = evidence_by_query or {}

    def from_search(
        self,
        response: PaperSearchResponse,
    ) -> EvidencePackage:

        return EvidencePackage(
            query=response.query,
            evidence=list(
                self.evidence_by_query.get(
                    response.query,
                    [],
                )
            ),
        )


def test_empty_paper_list_returns_empty():

    retriever = ExplicitGapEvidenceRetriever(
        search_tool=(FakeSearchTool()),
        package_builder=(FakePackageBuilder()),
    )

    result = retriever.retrieve([])

    assert result == []


def test_rejects_invalid_evidence_count():

    retriever = ExplicitGapEvidenceRetriever(
        search_tool=(FakeSearchTool()),
        package_builder=(FakePackageBuilder()),
    )

    try:

        retriever.retrieve(
            ["paper_a"],
            evidence_per_query=0,
        )

    except ValueError as error:

        assert str(error) == ("evidence_per_query " "must be positive")

    else:

        raise AssertionError("Expected ValueError")


def test_runs_all_gap_queries_per_paper():

    search_tool = FakeSearchTool()

    retriever = ExplicitGapEvidenceRetriever(
        search_tool=search_tool,
        package_builder=(FakePackageBuilder()),
    )

    retriever.retrieve(
        [
            "paper_a",
            "paper_b",
        ],
        evidence_per_query=4,
    )

    assert len(search_tool.calls) == (len(EXPLICIT_GAP_QUERIES) * 2)

    assert search_tool.calls[0]["allowed_paper_ids"] == {"paper_a"}

    assert search_tool.calls[-1]["allowed_paper_ids"] == {"paper_b"}

    assert all(call["top_k"] == 4 for call in search_tool.calls)

    assert all(call["max_per_paper"] == 4 for call in search_tool.calls)


def test_duplicate_evidence_is_removed():

    shared = make_evidence(
        evidence_id="e1",
        paper_id="paper_a",
    )

    evidence_by_query = {
        EXPLICIT_GAP_QUERIES[0]: [shared],
        EXPLICIT_GAP_QUERIES[1]: [shared],
    }

    retriever = ExplicitGapEvidenceRetriever(
        search_tool=(FakeSearchTool()),
        package_builder=(FakePackageBuilder(evidence_by_query)),
    )

    result = retriever.retrieve(["paper_a"])

    assert len(result) == 1

    assert result[0].evidence_id == "e1"


def test_labels_are_rebuilt_deterministically():

    first = make_evidence(
        evidence_id="e1",
        paper_id="paper_a",
    )

    second = make_evidence(
        evidence_id="e2",
        paper_id="paper_a",
    )

    evidence_by_query = {
        EXPLICIT_GAP_QUERIES[0]: [first],
        EXPLICIT_GAP_QUERIES[1]: [second],
    }

    retriever = ExplicitGapEvidenceRetriever(
        search_tool=(FakeSearchTool()),
        package_builder=(FakePackageBuilder(evidence_by_query)),
    )

    result = retriever.retrieve(["paper_a"])

    assert [item.label for item in result] == [
        "E1",
        "E2",
    ]
