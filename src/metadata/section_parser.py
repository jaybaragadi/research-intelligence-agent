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
        "background and motivation",
    ],

    "related_work": [
        "related work",
        "related works",
        "literature review",
    ],

    "methodology": [
        "methodology",
        "methods",
        "method",
        "our approach",
        "proposed approach",
        "approach",
        "framework",
    ],

    "experimental_setup": [
        "experimental setup",
        "experiment setup",
        "evaluation setup",
        "study setup",
        "experimental design",
        "experiment design",
    ],

    "evaluation": [
        "evaluation",
        "empirical evaluation",
        "experiments",
        "empirical study",
    ],

    "results": [
        "results",
        "experimental results",
        "evaluation results",
        "results and discussion",
    ],

    "discussion": [
        "discussion",
        "results and discussion",
    ],

    "limitations": [
        "limitations",
        "limitations and future work",
    ],

    "threats_to_validity": [
        "threats to validity",
        "threat to validity",
        "validity threats",
    ],

    "future_work": [
        "future work",
        "future directions",
        "limitations and future work",
        "conclusion and future work",
    ],

    "conclusion": [
        "conclusion",
        "conclusions",
        "conclusion and future work",
    ],

    "references": [
        "references",
        "bibliography",
    ],
}


def build_numbered_heading_pattern(
    heading: str,
) -> re.Pattern[str]:
    """
    Detect explicitly numbered section headings.

    Examples:
        1 Introduction
        1. Introduction
        2.3 Experimental Setup
        III. Evaluation
        IV RESULTS

    Numbered headings are reliable even when PDF line breaks
    have been flattened during text cleaning.
    """

    escaped = re.escape(
        heading
    )

    return re.compile(
        rf"\b(?:"
        rf"\d+(?:\.\d+)*\.?"
        rf"|[IVXLC]+\.?"
        rf")"
        rf"\s+"
        rf"{escaped}"
        rf"\b",
        flags=re.IGNORECASE,
    )


def build_plain_heading_pattern(
    heading: str,
) -> re.Pattern[str]:
    """
    Conservative fallback for headings without numbering.
    """

    escaped = re.escape(
        heading
    )

    return re.compile(
        rf"(?:"
        rf"^"
        rf"|(?<=[.!?])\s+"
        rf"|(?<=\n)"
        rf")"
        rf"{escaped}"
        rf"(?=\s|:|$)",
        flags=re.IGNORECASE,
    )


def find_heading(
    text: str,
    alias: str,
) -> bool:
    """
    Search for a section heading using numbered-heading
    detection first, then a conservative plain-heading fallback.
    """

    numbered = build_numbered_heading_pattern(
        alias
    )

    if numbered.search(text):
        return True

    plain = build_plain_heading_pattern(
        alias
    )

    return bool(
        plain.search(text)
    )


def discover_sections(
    paper: ExtractedPaper,
) -> list[SectionLocation]:
    """
    Discover common academic-paper sections.

    Only the first occurrence of each canonical section is kept.
    """

    discovered: list[SectionLocation] = []

    for canonical_name, aliases in SECTION_ALIASES.items():

        found = False

        for page in paper.pages:

            for alias in aliases:

                if find_heading(
                    page.text,
                    alias,
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