from pathlib import Path

import pytest

from src.models import (
    PaperChunk,
)
from src.tools.evidence_tool import (
    EvidenceTool,
)


class FakeEvidenceStore:
    """
    Deterministic vector metadata store.
    """

    def load_chunks(
        self,
    ) -> list[PaperChunk]:

        text_a = (
            "Mutation testing evaluates "
            "the effectiveness of tests."
        )

        text_b = (
            "Coverage feedback guides "
            "iterative test generation."
        )

        return [
            PaperChunk(
                chunk_id=(
                    "paper_a_chunk_0001"
                ),

                paper_id="paper_a",

                text=text_a,

                page_number=3,

                section=(
                    "methodology"
                ),

                chunk_index=1,

                character_count=(
                    len(text_a)
                ),
            ),

            PaperChunk(
                chunk_id=(
                    "paper_b_chunk_0002"
                ),

                paper_id="paper_b",

                text=text_b,

                page_number=7,

                section=(
                    "results"
                ),

                chunk_index=2,

                character_count=(
                    len(text_b)
                ),
            ),
        ]


def test_get_evidence_resolves_chunk():

    tool = EvidenceTool(
        store=FakeEvidenceStore()
    )

    evidence = tool.get(
        "paper_a_chunk_0001"
    )

    assert (
        evidence.evidence_id
        == "paper_a_chunk_0001"
    )

    assert (
        evidence.paper_id
        == "paper_a"
    )

    assert (
        evidence.page_number
        == 3
    )

    assert (
        evidence.section
        == "methodology"
    )


def test_get_many_preserves_order():

    tool = EvidenceTool(
        store=FakeEvidenceStore()
    )

    results = tool.get_many(
        [
            "paper_b_chunk_0002",
            "paper_a_chunk_0001",
        ]
    )

    assert [
        result.paper_id
        for result
        in results
    ] == [
        "paper_b",
        "paper_a",
    ]


def test_get_many_removes_duplicates():

    tool = EvidenceTool(
        store=FakeEvidenceStore()
    )

    results = tool.get_many(
        [
            "paper_a_chunk_0001",
            "paper_a_chunk_0001",
        ]
    )

    assert len(
        results
    ) == 1


def test_validate_correct_provenance():

    tool = EvidenceTool(
        store=FakeEvidenceStore()
    )

    assert tool.validate(
        evidence_id=(
            "paper_a_chunk_0001"
        ),

        paper_id="paper_a",

        page_number=3,

        section="methodology",
    )


def test_validate_rejects_wrong_page():

    tool = EvidenceTool(
        store=FakeEvidenceStore()
    )

    assert not tool.validate(
        evidence_id=(
            "paper_a_chunk_0001"
        ),

        page_number=99,
    )


def test_get_rejects_empty_id():

    tool = EvidenceTool(
        store=FakeEvidenceStore()
    )

    with pytest.raises(
        ValueError,

        match=(
            "evidence_id cannot be empty"
        ),
    ):

        tool.get(
            "   "
        )


def test_get_rejects_unknown_evidence():

    tool = EvidenceTool(
        store=FakeEvidenceStore()
    )

    with pytest.raises(
        KeyError,

        match=(
            "Evidence not found"
        ),
    ):

        tool.get(
            "missing_chunk"
        )