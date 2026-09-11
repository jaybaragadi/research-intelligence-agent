import argparse

from src.agents.models import (
    ResearchAgentRequest,
)
from src.agents.router import (
    ResearchIntentRouter,
)


def main() -> None:

    parser = argparse.ArgumentParser(
        description=("Inspect research-agent " "intent routing")
    )

    parser.add_argument(
        "query",
        type=str,
        help=("Natural-language research " "request"),
    )

    args = parser.parse_args()

    router = ResearchIntentRouter()

    routed = router.route(ResearchAgentRequest(query=args.query))

    print()
    print("=" * 70)
    print("RESEARCH INTENT ROUTER")
    print("=" * 70)

    print(f"Query              : " f"{routed.original_query}")

    print(f"Intent             : " f"{routed.intent.value}")

    print(f"Confidence         : " f"{routed.confidence:.2f}")

    print(
        "Paper IDs          : "
        + (", ".join(routed.paper_ids) if routed.paper_ids else "None")
    )

    print(f"Evidence ID        : " f"{routed.evidence_id or 'None'}")

    print(f"Needs clarification: " f"{routed.needs_clarification}")

    print(
        "Missing fields     : "
        + (", ".join(routed.missing_fields) if routed.missing_fields else "None")
    )

    print(f"Reason             : " f"{routed.reason}")

    print("=" * 70)


if __name__ == "__main__":
    main()
