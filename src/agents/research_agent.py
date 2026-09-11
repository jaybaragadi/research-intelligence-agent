from typing import Any

from src.agents.intents import (
    ResearchIntent,
)
from src.agents.models import (
    ResearchAgentRequest,
    ResearchAgentResponse,
    RoutedResearchRequest,
    ToolExecutionTrace,
)
from src.agents.router import (
    ResearchIntentRouter,
)
from src.tools.research_tools import (
    ResearchTools,
)


class ResearchAgent:
    """
    Deterministic orchestration layer for the
    Research Intelligence Agent.

    Responsibilities:

    1. receive a research request
    2. route the request
    3. validate routing requirements
    4. select the correct research tool
    5. execute the tool
    6. return structured results
    7. preserve execution trace

    The agent does NOT generate unsupported
    natural-language claims.
    """

    def __init__(
        self,
        router: ResearchIntentRouter | None = None,
        tools: ResearchTools | None = None,
    ) -> None:

        self.router = router if router is not None else ResearchIntentRouter()

        self.tools = tools if tools is not None else ResearchTools()

    def _clarification_response(
        self,
        routed: RoutedResearchRequest,
    ) -> ResearchAgentResponse:
        """
        Return a non-executing response when the
        router determines that required input is
        missing.
        """

        missing = (
            ", ".join(routed.missing_fields)
            if routed.missing_fields
            else "additional information"
        )

        return ResearchAgentResponse(
            query=(routed.original_query),
            intent=(routed.intent),
            status="needs_clarification",
            message=(
                "The request cannot be executed "
                "yet because required information "
                f"is missing: {missing}."
            ),
            paper_ids=(routed.paper_ids),
            evidence_id=(routed.evidence_id),
            needs_clarification=True,
            missing_fields=(routed.missing_fields),
            trace=[],
        )

    def _success_response(
        self,
        routed: RoutedResearchRequest,
        data: Any,
        message: str,
        trace: list[ToolExecutionTrace],
    ) -> ResearchAgentResponse:
        """
        Construct a successful deterministic
        agent response.
        """

        return ResearchAgentResponse(
            query=(routed.original_query),
            intent=(routed.intent),
            status="success",
            message=message,
            data=data,
            paper_ids=(routed.paper_ids),
            evidence_id=(routed.evidence_id),
            trace=trace,
        )

    def _error_response(
        self,
        routed: RoutedResearchRequest,
        error: Exception,
        trace: list[ToolExecutionTrace],
    ) -> ResearchAgentResponse:
        """
        Convert tool execution failures into a
        stable agent response instead of
        crashing the orchestration layer.
        """

        return ResearchAgentResponse(
            query=(routed.original_query),
            intent=(routed.intent),
            status="error",
            message=("Research tool execution failed: " f"{error}"),
            paper_ids=(routed.paper_ids),
            evidence_id=(routed.evidence_id),
            trace=trace,
        )

    def _run_search(
        self,
        routed: RoutedResearchRequest,
        trace: list[ToolExecutionTrace],
    ) -> ResearchAgentResponse:

        step = ToolExecutionTrace(
            step=1,
            tool_name="search",
            status="started",
            inputs={
                "query": (routed.original_query),
            },
        )

        trace.append(step)

        try:

            result = self.tools.search(query=(routed.original_query))

            step.status = "success"

            return self._success_response(
                routed=routed,
                data=result,
                message=("Research search completed."),
                trace=trace,
            )

        except Exception as error:

            step.status = "error"

            step.error = str(error)

            return self._error_response(
                routed=routed,
                error=error,
                trace=trace,
            )

    def _run_summary(
        self,
        routed: RoutedResearchRequest,
        trace: list[ToolExecutionTrace],
    ) -> ResearchAgentResponse:

        summaries: list[Any] = []

        try:

            for index, paper_id in enumerate(
                routed.paper_ids,
                start=1,
            ):

                step = ToolExecutionTrace(
                    step=index,
                    tool_name="summarize",
                    status="started",
                    inputs={"paper_id": paper_id},
                )

                trace.append(step)

                summary = self.tools.summarize(paper_id=paper_id)

                summaries.append(summary)

                step.status = "success"

            data: Any

            if len(summaries) == 1:
                data = summaries[0]

            else:
                data = summaries

            return self._success_response(
                routed=routed,
                data=data,
                message=(
                    "Paper summary completed."
                    if len(summaries) == 1
                    else ("Paper summaries completed.")
                ),
                trace=trace,
            )

        except Exception as error:

            if trace:
                trace[-1].status = "error"
                trace[-1].error = str(error)

            return self._error_response(
                routed=routed,
                error=error,
                trace=trace,
            )

    def _run_compare(
        self,
        routed: RoutedResearchRequest,
        trace: list[ToolExecutionTrace],
    ) -> ResearchAgentResponse:

        step = ToolExecutionTrace(
            step=1,
            tool_name="compare",
            status="started",
            inputs={
                "paper_ids": (routed.paper_ids),
                "query": (routed.original_query),
                "evidence_per_paper": 3,
            },
        )

        trace.append(step)

        try:

            result = self.tools.compare(
                paper_ids=(routed.paper_ids),
                query=(routed.original_query),
                evidence_per_paper=3,
            )

            step.status = "success"

            return self._success_response(
                routed=routed,
                data=result,
                message=("Paper comparison completed."),
                trace=trace,
            )

        except Exception as error:

            step.status = "error"

            step.error = str(error)

            return self._error_response(
                routed=routed,
                error=error,
                trace=trace,
            )

    def _run_evidence(
        self,
        routed: RoutedResearchRequest,
        trace: list[ToolExecutionTrace],
    ) -> ResearchAgentResponse:

        evidence_id = routed.evidence_id

        if evidence_id is None:

            raise ValueError("Evidence intent requires " "an evidence ID.")

        step = ToolExecutionTrace(
            step=1,
            tool_name="evidence",
            status="started",
            inputs={"evidence_id": (evidence_id)},
        )

        trace.append(step)

        try:

            result = self.tools.evidence(evidence_id=(evidence_id))

            step.status = "success"

            return self._success_response(
                routed=routed,
                data=result,
                message=("Evidence validation completed."),
                trace=trace,
            )

        except Exception as error:

            step.status = "error"

            step.error = str(error)

            return self._error_response(
                routed=routed,
                error=error,
                trace=trace,
            )

    def _run_citation(
        self,
        routed: RoutedResearchRequest,
        trace: list[ToolExecutionTrace],
    ) -> ResearchAgentResponse:

        evidence_id = routed.evidence_id

        if evidence_id is None:

            raise ValueError("Citation intent requires " "an evidence ID.")

        step = ToolExecutionTrace(
            step=1,
            tool_name="citation",
            status="started",
            inputs={"evidence_id": (evidence_id)},
        )

        trace.append(step)

        try:

            result = self.tools.citation(evidence_id=(evidence_id))

            step.status = "success"

            return self._success_response(
                routed=routed,
                data=result,
                message=("Citation generation completed."),
                trace=trace,
            )

        except Exception as error:

            step.status = "error"

            step.error = str(error)

            return self._error_response(
                routed=routed,
                error=error,
                trace=trace,
            )

    def run(
        self,
        request: ResearchAgentRequest,
    ) -> ResearchAgentResponse:
        """
        Route and execute one research request.
        """

        routed = self.router.route(request)

        if routed.needs_clarification:

            return self._clarification_response(routed)

        trace: list[ToolExecutionTrace] = []

        if routed.intent == ResearchIntent.SEARCH:

            return self._run_search(
                routed,
                trace,
            )

        if routed.intent == ResearchIntent.SUMMARIZE:

            return self._run_summary(
                routed,
                trace,
            )

        if routed.intent == ResearchIntent.COMPARE:

            return self._run_compare(
                routed,
                trace,
            )

        if routed.intent == ResearchIntent.EVIDENCE:

            return self._run_evidence(
                routed,
                trace,
            )

        if routed.intent == ResearchIntent.CITATION:

            return self._run_citation(
                routed,
                trace,
            )

        return ResearchAgentResponse(
            query=(routed.original_query),
            intent=(routed.intent),
            status="needs_clarification",
            message=("The research intent could not " "be determined."),
            needs_clarification=True,
            missing_fields=["supported_research_intent"],
            trace=[],
        )


def run_research_agent(
    query: str,
) -> ResearchAgentResponse:
    """
    Convenience wrapper for simple callers.
    """

    agent = ResearchAgent()

    request = ResearchAgentRequest(query=query)

    return agent.run(request)
