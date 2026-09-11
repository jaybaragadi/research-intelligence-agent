import argparse

from src.tools.summarize_paper import (
    SummarizePaperTool,
)


def main() -> None:

    parser = argparse.ArgumentParser(
        description=("Create a structured evidence-backed " "research paper summary")
    )

    parser.add_argument(
        "paper_id",
        type=str,
        help=("Paper identifier, for example " "08_telpa"),
    )

    args = parser.parse_args()

    tool = SummarizePaperTool()

    summary = tool.summarize(args.paper_id)

    print()
    print("=" * 70)
    print("STRUCTURED PAPER SUMMARY")
    print("=" * 70)

    print(f"Paper : {summary.paper_id}")

    print(f"Title : {summary.title}")

    print(f"Year  : {summary.year}")

    print(
        "Authors: "
        + (", ".join(summary.authors) if summary.authors else "Not extracted")
    )

    print()
    print("ABSTRACT")
    print("-" * 70)

    print(summary.abstract or "No abstract extracted.")

    print()
    print("RESEARCH QUESTIONS")
    print("-" * 70)

    if summary.research_questions:

        for index, question in enumerate(
            summary.research_questions,
            start=1,
        ):

            print(f"{index}. {question}")

    else:

        print("No explicit research questions " "were extracted.")

    print()
    print("SECTIONS")
    print("-" * 70)

    if summary.sections:

        for section in summary.sections:

            print(f"- {section}")

    else:

        print("No section structure extracted.")

    print()
    print("RESEARCH EVIDENCE")
    print("=" * 70)

    for category, evidence_items in summary.evidence.items():

        print()
        print(category.upper())

        print("-" * 70)

        if not evidence_items:

            print("No evidence extracted.")

            continue

        for evidence in evidence_items:

            print(
                f"Page {evidence.page_number}"
                f" | keyword="
                f"{evidence.matched_keyword}"
            )

            print(evidence.snippet)

            print()


if __name__ == "__main__":
    main()
