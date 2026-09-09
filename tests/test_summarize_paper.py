import json

import pytest

from src.tools.summarize_paper import (
    SummarizePaperTool,
)


def create_metadata_file(
    tmp_path,
) -> None:

    payload = {
        "paper_id": "paper_a",
        "filename": "paper_a.pdf",
        "title": "Example Research Paper",
        "authors": [
            "Researcher One",
            "Researcher Two",
        ],
        "year": 2025,
        "abstract": (
            "This paper studies automated "
            "test generation."
        ),
        "sections": [
            {
                "canonical_name": "methodology",
                "matched_heading": "Methodology",
                "page_number": 3,
            },
            {
                "canonical_name": "results",
                "matched_heading": "Results",
                "page_number": 7,
            },
        ],
        "research_questions": [
            (
                "How can automated test "
                "generation be improved?"
            )
        ],
        "research_signals": [
            {
                "category": "methodology",
                "page_number": 3,
                "snippet": (
                    "The approach uses iterative "
                    "test generation."
                ),
                "matched_keyword": "approach",
            },
            {
                "category": "findings",
                "page_number": 7,
                "snippet": (
                    "The approach improves "
                    "coverage."
                ),
                "matched_keyword": "improves",
            },
            {
                "category": "limitations",
                "page_number": 9,
                "snippet": (
                    "The evaluation uses a "
                    "small benchmark."
                ),
                "matched_keyword": "limitation",
            },
        ],
    }

    path = (
        tmp_path
        / "paper_a.json"
    )

    path.write_text(
        json.dumps(payload),
        encoding="utf-8",
    )


def test_summary_loads_metadata(
    tmp_path,
):

    create_metadata_file(
        tmp_path
    )

    tool = SummarizePaperTool(
        metadata_directory=tmp_path
    )

    summary = tool.summarize(
        "paper_a"
    )

    assert (
        summary.paper_id
        == "paper_a"
    )

    assert (
        summary.title
        == "Example Research Paper"
    )

    assert summary.year == 2025

    assert len(
        summary.authors
    ) == 2

    assert len(
        summary.research_questions
    ) == 1


def test_summary_groups_evidence(
    tmp_path,
):

    create_metadata_file(
        tmp_path
    )

    tool = SummarizePaperTool(
        metadata_directory=tmp_path
    )

    summary = tool.summarize(
        "paper_a"
    )

    assert (
        len(
            summary.evidence[
                "methodology"
            ]
        )
        == 1
    )

    assert (
        len(
            summary.evidence[
                "findings"
            ]
        )
        == 1
    )

    assert (
        len(
            summary.evidence[
                "limitations"
            ]
        )
        == 1
    )

    assert (
        summary.evidence[
            "future_work"
        ]
        == []
    )


def test_summary_preserves_provenance(
    tmp_path,
):

    create_metadata_file(
        tmp_path
    )

    tool = SummarizePaperTool(
        metadata_directory=tmp_path
    )

    summary = tool.summarize(
        "paper_a"
    )

    evidence = (
        summary.evidence[
            "methodology"
        ][0]
    )

    assert (
        evidence.page_number
        == 3
    )

    assert (
        evidence.matched_keyword
        == "approach"
    )


def test_summary_rejects_empty_paper_id(
    tmp_path,
):

    tool = SummarizePaperTool(
        metadata_directory=tmp_path
    )

    with pytest.raises(
        ValueError,
        match="paper_id cannot be empty",
    ):

        tool.summarize(
            "   "
        )


def test_summary_rejects_unknown_paper(
    tmp_path,
):

    tool = SummarizePaperTool(
        metadata_directory=tmp_path
    )

    with pytest.raises(
        FileNotFoundError,
        match="Paper metadata not found",
    ):

        tool.summarize(
            "missing_paper"
        )