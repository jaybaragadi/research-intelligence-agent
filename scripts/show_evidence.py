import argparse

from src.tools.citation_tool import (
    CitationTool,
)
from src.tools.evidence_tool import (
    EvidenceTool,
)


def main() -> None:

    parser = argparse.ArgumentParser(
        description=("Resolve a research evidence ID " "and generate its citation")
    )

    parser.add_argument(
        "evidence_id",
        type=str,
        help=("Chunk/evidence identifier, " "for example " "08_telpa_chunk_0040"),
    )

    args = parser.parse_args()

    evidence_tool = EvidenceTool()

    citation_tool = CitationTool(evidence_tool=(evidence_tool))

    evidence = evidence_tool.get(args.evidence_id)

    citation = citation_tool.cite(args.evidence_id)

    print()
    print("=" * 70)
    print("VALIDATED RESEARCH EVIDENCE")
    print("=" * 70)

    print(f"Evidence ID : " f"{evidence.evidence_id}")

    print(f"Paper       : " f"{evidence.paper_id}")

    print(f"Page        : " f"{evidence.page_number}")

    print(f"Section     : " f"{evidence.section}")

    print(f"Chunk       : " f"{evidence.chunk_id}")

    print()

    print(evidence.text)

    print()
    print("-" * 70)
    print("CITATION")
    print("-" * 70)

    print(citation.citation_text)

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
