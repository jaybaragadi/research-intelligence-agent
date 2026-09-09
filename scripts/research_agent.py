import argparse
from dataclasses import (
    asdict,
    is_dataclass,
)
from pprint import pprint
from typing import Any

from src.agents.models import (
    ResearchAgentRequest,
)

from src.agents.research_agent import (
    ResearchAgent,
)


def display_data(
    data: Any,
) -> None:
    """
    Display dataclass-based tool responses in
    a readable form without changing their
    underlying contracts.
    """

    if data is None:

        print("None")

        return

    if isinstance(
        data,
        list,
    ):

        for index, item in enumerate(
            data,
            start=1,
        ):

            print()
            print(
                f"Result {index}"
            )

            print("-" * 70)

            display_data(
                item
            )

        return

    if is_dataclass(
        data
    ):

        pprint(
            asdict(
                data
            ),

            sort_dicts=False,
        )

        return

    pprint(
        data,
        sort_dicts=False,
    )


def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "Run the deterministic Research "
            "Intelligence Agent"
        )
    )

    parser.add_argument(
        "query",
        type=str,
        help=(
            "Natural-language research request"
        ),
    )

    args = (
        parser.parse_args()
    )

    agent = (
        ResearchAgent()
    )

    response = (
        agent.run(
            ResearchAgentRequest(
                query=args.query
            )
        )
    )

    print()
    print("=" * 70)
    print("RESEARCH INTELLIGENCE AGENT")
    print("=" * 70)

    print(
        f"Query   : {response.query}"
    )

    print(
        f"Intent  : "
        f"{response.intent.value}"
    )

    print(
        f"Status  : {response.status}"
    )

    print(
        f"Message : {response.message}"
    )

    if response.paper_ids:

        print(
            "Papers  : "
            + ", ".join(
                response.paper_ids
            )
        )

    if response.evidence_id:

        print(
            "Evidence: "
            f"{response.evidence_id}"
        )

    if response.missing_fields:

        print(
            "Missing : "
            + ", ".join(
                response.missing_fields
            )
        )

    print()
    print("-" * 70)
    print("RESULT")
    print("-" * 70)

    display_data(
        response.data
    )

    print()
    print("-" * 70)
    print("EXECUTION TRACE")
    print("-" * 70)

    if not response.trace:

        print(
            "No tool executed."
        )

    else:

        for trace in (
            response.trace
        ):

            print(
                f"Step {trace.step}: "
                f"{trace.tool_name} "
                f"[{trace.status}]"
            )

            print(
                f"Inputs: "
                f"{trace.inputs}"
            )

            if trace.error:

                print(
                    f"Error : "
                    f"{trace.error}"
                )

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()