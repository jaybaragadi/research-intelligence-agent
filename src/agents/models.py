from dataclasses import (
    dataclass,
    field,
)
from typing import Any

from src.agents.intents import (
    ResearchIntent,
)


@dataclass
class ResearchAgentRequest:
    """
    Raw request received by the research agent.
    """

    query: str

    paper_ids: list[str] = field(default_factory=list)

    evidence_id: str | None = None


@dataclass
class RoutedResearchRequest:
    """
    Structured routing decision.

    No research tool has been executed yet.
    """

    original_query: str

    intent: ResearchIntent

    paper_ids: list[str] = field(default_factory=list)

    evidence_id: str | None = None

    confidence: float = 0.0

    reason: str = ""

    needs_clarification: bool = False

    missing_fields: list[str] = field(default_factory=list)


@dataclass
class ToolExecutionTrace:
    """
    One deterministic tool invocation made
    by the research agent.

    This gives us observability without
    exposing internal implementation details
    from the tool itself.
    """

    step: int

    tool_name: str

    status: str

    inputs: dict[str, Any] = field(default_factory=dict)

    error: str | None = None


@dataclass
class ResearchAgentResponse:
    """
    Structured result returned by the
    deterministic research-agent layer.

    `data` contains the native structured
    result produced by the selected research
    tool.

    Natural-language LLM synthesis will be
    added above this contract later.
    """

    query: str

    intent: ResearchIntent

    status: str

    message: str

    data: Any = None

    paper_ids: list[str] = field(default_factory=list)

    evidence_id: str | None = None

    needs_clarification: bool = False

    missing_fields: list[str] = field(default_factory=list)

    trace: list[ToolExecutionTrace] = field(default_factory=list)
