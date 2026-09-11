from enum import Enum


class ResearchIntent(
    str,
    Enum,
):
    """
    Supported deterministic research-agent
    intents.

    Phase 7 routing selects one of these
    intents before any research tool is
    executed.
    """

    SEARCH = "search"

    SUMMARIZE = "summarize"

    COMPARE = "compare"

    EVIDENCE = "evidence"

    CITATION = "citation"

    UNKNOWN = "unknown"
