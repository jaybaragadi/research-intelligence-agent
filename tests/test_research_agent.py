from src.agents.intents import (
    ResearchIntent,
)
from src.agents.models import (
    ResearchAgentRequest,
)
from src.agents.research_agent import (
    ResearchAgent,
)
from src.agents.router import (
    ResearchIntentRouter,
)


class FakeResearchTools:

    def __init__(
        self,
    ):
        self.calls = []

    def search(
        self,
        query: str,
        top_k=None,
    ):
        self.calls.append(
            (
                "search",
                query,
            )
        )

        return {
            "type": "search",
            "query": query,
        }

    def summarize(
        self,
        paper_id: str,
    ):
        self.calls.append(
            (
                "summarize",
                paper_id,
            )
        )

        return {
            "type": "summary",
            "paper_id": paper_id,
        }

    def compare(
        self,
        paper_ids: list[str],
        query: str,
        evidence_per_paper: int = 3,
    ):
        self.calls.append(
            (
                "compare",
                paper_ids,
                query,
                evidence_per_paper,
            )
        )

        return {
            "type": "comparison",
            "paper_ids": paper_ids,
        }

    def evidence(
        self,
        evidence_id: str,
    ):
        self.calls.append(
            (
                "evidence",
                evidence_id,
            )
        )

        return {
            "type": "evidence",
            "evidence_id": evidence_id,
        }

    def citation(
        self,
        evidence_id: str,
    ):
        self.calls.append(
            (
                "citation",
                evidence_id,
            )
        )

        return {
            "type": "citation",
            "evidence_id": evidence_id,
        }


def build_agent():

    tools = FakeResearchTools()

    agent = ResearchAgent(
        router=ResearchIntentRouter(),
        tools=tools,
    )

    return (
        agent,
        tools,
    )


def test_agent_executes_search():

    agent, tools = build_agent()

    response = agent.run(
        ResearchAgentRequest(
            query=("How does mutation testing " "improve test generation?")
        )
    )

    assert response.status == "success"

    assert response.intent == ResearchIntent.SEARCH

    assert tools.calls[0][0] == "search"


def test_agent_executes_summary():

    agent, tools = build_agent()

    response = agent.run(ResearchAgentRequest(query=("Summarize TELPA")))

    assert response.status == "success"

    assert response.intent == ResearchIntent.SUMMARIZE

    assert tools.calls == [
        (
            "summarize",
            "08_telpa",
        )
    ]


def test_agent_can_summarize_multiple_papers():

    agent, tools = build_agent()

    response = agent.run(ResearchAgentRequest(query=("Summarize TELPA " "and CoverUp")))

    assert response.status == "success"

    assert len(response.data) == 2

    assert tools.calls == [
        (
            "summarize",
            "08_telpa",
        ),
        (
            "summarize",
            "05_coverup",
        ),
    ]


def test_agent_executes_compare():

    agent, tools = build_agent()

    response = agent.run(ResearchAgentRequest(query=("Compare MuTAP " "and CoverUp")))

    assert response.status == "success"

    assert response.intent == ResearchIntent.COMPARE

    assert tools.calls[0][0] == "compare"

    assert tools.calls[0][1] == [
        "03_mutap",
        "05_coverup",
    ]


def test_agent_executes_evidence():

    agent, tools = build_agent()

    response = agent.run(
        ResearchAgentRequest(query=("Show evidence " "08_telpa_chunk_0040"))
    )

    assert response.status == "success"

    assert response.intent == ResearchIntent.EVIDENCE

    assert tools.calls == [
        (
            "evidence",
            "08_telpa_chunk_0040",
        )
    ]


def test_agent_executes_citation():

    agent, tools = build_agent()

    response = agent.run(ResearchAgentRequest(query=("Cite " "05_coverup_chunk_0017")))

    assert response.status == "success"

    assert response.intent == ResearchIntent.CITATION

    assert tools.calls == [
        (
            "citation",
            "05_coverup_chunk_0017",
        )
    ]


def test_agent_does_not_execute_when_clarification_needed():

    agent, tools = build_agent()

    response = agent.run(ResearchAgentRequest(query=("Compare TELPA")))

    assert response.status == "needs_clarification"

    assert response.needs_clarification

    assert tools.calls == []


def test_agent_trace_records_success():

    agent, _ = build_agent()

    response = agent.run(ResearchAgentRequest(query=("Summarize TELPA")))

    assert len(response.trace) == 1

    assert response.trace[0].tool_name == "summarize"

    assert response.trace[0].status == "success"


def test_agent_trace_records_multiple_steps():

    agent, _ = build_agent()

    response = agent.run(ResearchAgentRequest(query=("Summarize TELPA " "and CoverUp")))

    assert len(response.trace) == 2

    assert [trace.step for trace in response.trace] == [
        1,
        2,
    ]


class FailingResearchTools(FakeResearchTools):

    def search(
        self,
        query: str,
        top_k=None,
    ):
        raise RuntimeError("Simulated search failure")


def test_agent_returns_structured_error():

    tools = FailingResearchTools()

    agent = ResearchAgent(
        router=ResearchIntentRouter(),
        tools=tools,
    )

    response = agent.run(
        ResearchAgentRequest(query=("How does mutation " "testing work?"))
    )

    assert response.status == "error"

    assert response.trace[0].status == "error"

    assert "Simulated search failure" in response.message


def test_empty_query_does_not_execute_tool():

    agent, tools = build_agent()

    response = agent.run(ResearchAgentRequest(query="   "))

    assert response.status == "needs_clarification"

    assert tools.calls == []
