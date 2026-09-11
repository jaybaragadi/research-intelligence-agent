from src.agents.intents import (
    ResearchIntent,
)
from src.agents.models import (
    ResearchAgentRequest,
)
from src.agents.router import (
    ResearchIntentRouter,
)


def build_router():
    return ResearchIntentRouter()


def test_routes_general_question_to_search():

    router = build_router()

    routed = router.route(
        ResearchAgentRequest(
            query=("How does mutation testing " "improve generated tests?")
        )
    )

    assert routed.intent == ResearchIntent.SEARCH

    assert not (routed.needs_clarification)


def test_routes_summary_by_alias():

    router = build_router()

    routed = router.route(ResearchAgentRequest(query=("Summarize TELPA")))

    assert routed.intent == ResearchIntent.SUMMARIZE

    assert routed.paper_ids == ["08_telpa"]

    assert not (routed.needs_clarification)


def test_routes_compare_by_aliases():

    router = build_router()

    routed = router.route(ResearchAgentRequest(query=("Compare MuTAP and CoverUp")))

    assert routed.intent == ResearchIntent.COMPARE

    assert routed.paper_ids == [
        "03_mutap",
        "05_coverup",
    ]

    assert not (routed.needs_clarification)


def test_compare_requires_two_papers():

    router = build_router()

    routed = router.route(ResearchAgentRequest(query=("Compare TELPA")))

    assert routed.intent == ResearchIntent.COMPARE

    assert routed.needs_clarification

    assert "at_least_two_paper_ids" in routed.missing_fields


def test_summary_requires_paper():

    router = build_router()

    routed = router.route(ResearchAgentRequest(query=("Summarize this paper")))

    assert routed.intent == ResearchIntent.SUMMARIZE

    assert routed.needs_clarification

    assert "paper_id" in routed.missing_fields


def test_routes_evidence_request():

    router = build_router()

    routed = router.route(
        ResearchAgentRequest(query=("Show evidence " "08_telpa_chunk_0040"))
    )

    assert routed.intent == ResearchIntent.EVIDENCE

    assert routed.evidence_id == "08_telpa_chunk_0040"


def test_routes_citation_request():

    router = build_router()

    routed = router.route(ResearchAgentRequest(query=("Cite " "05_coverup_chunk_0017")))

    assert routed.intent == ResearchIntent.CITATION

    assert routed.evidence_id == "05_coverup_chunk_0017"


def test_extracts_explicit_paper_ids():

    router = build_router()

    routed = router.route(
        ResearchAgentRequest(query=("Compare 03_mutap " "and 08_telpa"))
    )

    assert routed.paper_ids == [
        "03_mutap",
        "08_telpa",
    ]


def test_duplicate_papers_are_removed():

    router = build_router()

    routed = router.route(
        ResearchAgentRequest(query=("Compare TELPA with " "08_telpa and CoverUp"))
    )

    assert routed.paper_ids == [
        "08_telpa",
        "05_coverup",
    ]


def test_empty_query_requires_clarification():

    router = build_router()

    routed = router.route(ResearchAgentRequest(query="   "))

    assert routed.intent == ResearchIntent.UNKNOWN

    assert routed.needs_clarification

    assert "query" in routed.missing_fields
