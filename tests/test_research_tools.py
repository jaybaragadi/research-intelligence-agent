from src.tools.research_tools import (
    ResearchTools,
)


class FakeSearchTool:

    def search(
        self,
        query: str,
        top_k: int | None = None,
    ):
        return (
            "search",
            query,
            top_k,
        )


class FakeSummaryTool:

    def summarize(
        self,
        paper_id: str,
    ):
        return (
            "summary",
            paper_id,
        )


class FakeCompareTool:

    def compare(
        self,
        paper_ids: list[str],
        query: str,
        evidence_per_paper: int = 3,
    ):
        return (
            "compare",
            paper_ids,
            query,
            evidence_per_paper,
        )


class FakeEvidenceTool:

    def get(
        self,
        evidence_id: str,
    ):
        return (
            "evidence",
            evidence_id,
        )


class FakeCitationTool:

    def cite(
        self,
        evidence_id: str,
    ):
        return (
            "citation",
            evidence_id,
        )


def build_tools() -> ResearchTools:

    return ResearchTools(
        search_tool=(FakeSearchTool()),
        summarize_tool=(FakeSummaryTool()),
        compare_tool=(FakeCompareTool()),
        evidence_tool=(FakeEvidenceTool()),
        citation_tool=(FakeCitationTool()),
    )


def test_search_routes_to_search_tool():

    tools = build_tools()

    result = tools.search(
        "mutation testing",
        top_k=5,
    )

    assert result == (
        "search",
        "mutation testing",
        5,
    )


def test_summarize_routes_to_summary_tool():

    tools = build_tools()

    result = tools.summarize("03_mutap")

    assert result == (
        "summary",
        "03_mutap",
    )


def test_compare_routes_to_compare_tool():

    tools = build_tools()

    result = tools.compare(
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
        query=("Compare approaches"),
        evidence_per_paper=2,
    )

    assert result == (
        "compare",
        [
            "03_mutap",
            "05_coverup",
        ],
        "Compare approaches",
        2,
    )


def test_evidence_routes_to_evidence_tool():

    tools = build_tools()

    result = tools.evidence("03_mutap_chunk_0001")

    assert result == (
        "evidence",
        "03_mutap_chunk_0001",
    )


def test_citation_routes_to_citation_tool():

    tools = build_tools()

    result = tools.citation("03_mutap_chunk_0001")

    assert result == (
        "citation",
        "03_mutap_chunk_0001",
    )
