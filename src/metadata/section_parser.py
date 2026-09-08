import re

from src.models import (
    ExtractedPaper,
    SectionLocation,
)


SECTION_ALIASES: dict[str, list[str]] = {
    "abstract": [
        "abstract",
    ],
    "introduction": [
        "introduction",
    ],
    "background": [
        "background",
        "preliminaries",
    ],
    "related_work": [
        "related work",
        "related works",
    ],
    "methodology": [
        "methodology",
        "method",
        "methods",
        "approach",
        "proposed approach",
        "our approach",
    ],
    "experimental_setup": [
        "experimental setup",
        "experiment setup",
        "evaluation setup",
        "study setup",
    ],
    "evaluation": [
        "evaluation",
        "experiments",
        "empirical evaluation",
    ],
    "results": [
        "results",
        "experimental results",
        "evaluation results",
    ],
    "discussion": [
        "discussion",
    ],
    "limitations": [
        "limitations",
    ],
    "threats_to_validity": [
        "threats to validity",
        "threat to validity",
    ],
    "future_work": [
        "future work",
        "future directions",
    ],
    "conclusion": [
        "conclusion",
        "conclusions",
    ],
    "references": [
        "references",
        "bibliography",
    ],
}


def heading_pattern(
    heading: str,
) -> re.Pattern[str]:
    """
    Create a reasonably conservative section-heading pattern.

    Handles headings such as:

    Introduction
    1 Introduction
    1. Introduction
    III. RESULTS
    """

    escaped = re.escape(
        heading
    )

    return re.compile(
        rf"(?:^|[\n.!?]\s+)"
        rf"(?:"
        rf"\d+(?:\.\d+)*\.?\s+"
        rf"|[IVX]+\.?\s+"
        rf")?"
        rf"{escaped}"
        rf"\b",
        flags=re.IGNORECASE,
    )


def discover_sections(
    paper: ExtractedPaper,
) -> list[SectionLocation]:
    """
    Find the first occurrence of common research sections.
    """

    discovered: list[SectionLocation] = []

    for canonical_name, aliases in SECTION_ALIASES.items():

        found = False

        for page in paper.pages:

            for alias in aliases:

                pattern = heading_pattern(
                    alias
                )

                if pattern.search(
                    page.text
                ):
                    discovered.append(
                        SectionLocation(
                            canonical_name=canonical_name,
                            matched_heading=alias,
                            page_number=page.page_number,
                        )
                    )

                    found = True
                    break

            if found:
                break

    return sorted(
        discovered,
        key=lambda section: (
            section.page_number,
            section.canonical_name,
        ),
    )