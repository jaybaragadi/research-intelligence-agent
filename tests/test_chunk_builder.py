from pathlib import Path

import pytest

from src.chunking.chunk_builder import (
    create_page_chunks,
)

from src.models import (
    ExtractedPage,
    ExtractedPaper,
    PaperProfile,
    SectionLocation,
)


def create_test_data():

    text = (
        "Large language models are used for software testing. "
        "They can generate unit tests automatically. "
        "Researchers evaluate generated tests using coverage. "
        "Branch coverage is frequently used as an evaluation metric. "
        "Mutation testing can also measure fault detection ability."
    )

    paper = ExtractedPaper(
        paper_id="test",
        filename="test.pdf",
        source_path=Path(
            "test.pdf"
        ),
        total_pages=1,
        extracted_pages=1,
        empty_pages=0,
        pages=[
            ExtractedPage(
                page_number=1,
                text=text,
                character_count=len(
                    text
                ),
            )
        ],
    )

    profile = PaperProfile(
        paper_id="test",
        filename="test.pdf",
        title="Test Paper",
        sections=[
            SectionLocation(
                canonical_name="introduction",
                matched_heading="introduction",
                page_number=1,
            )
        ],
    )

    return paper, profile


def test_create_chunks():

    paper, profile = (
        create_test_data()
    )

    chunks = create_page_chunks(
        paper=paper,
        profile=profile,
        chunk_size=140,
        chunk_overlap=40,
    )

    assert len(chunks) >= 2


def test_chunks_keep_provenance():

    paper, profile = (
        create_test_data()
    )

    chunks = create_page_chunks(
        paper=paper,
        profile=profile,
        chunk_size=140,
        chunk_overlap=40,
    )

    for chunk in chunks:

        assert chunk.paper_id == "test"
        assert chunk.page_number == 1
        assert chunk.section == "introduction"


def test_chunk_ids_are_unique():

    paper, profile = (
        create_test_data()
    )

    chunks = create_page_chunks(
        paper=paper,
        profile=profile,
        chunk_size=140,
        chunk_overlap=40,
    )

    chunk_ids = [
        chunk.chunk_id
        for chunk in chunks
    ]

    assert len(
        chunk_ids
    ) == len(
        set(chunk_ids)
    )


def test_invalid_chunk_size():

    paper, profile = (
        create_test_data()
    )

    with pytest.raises(
        ValueError
    ):
        create_page_chunks(
            paper=paper,
            profile=profile,
            chunk_size=0,
            chunk_overlap=0,
        )


def test_overlap_must_be_smaller_than_chunk():

    paper, profile = (
        create_test_data()
    )

    with pytest.raises(
        ValueError
    ):
        create_page_chunks(
            paper=paper,
            profile=profile,
            chunk_size=100,
            chunk_overlap=100,
        )

def test_long_sentence_is_split():

    long_sentence = (
        "word " * 400
    ).strip()

    paper = ExtractedPaper(
        paper_id="test",
        filename="test.pdf",
        source_path=Path("test.pdf"),
        total_pages=1,
        extracted_pages=1,
        empty_pages=0,
        pages=[
            ExtractedPage(
                page_number=1,
                text=long_sentence,
                character_count=len(
                    long_sentence
                ),
            )
        ],
    )

    profile = PaperProfile(
        paper_id="test",
        filename="test.pdf",
        title="Test Paper",
        sections=[],
    )

    chunks = create_page_chunks(
        paper=paper,
        profile=profile,
        chunk_size=500,
        chunk_overlap=100,
    )

    assert len(chunks) > 1

    assert all(
        chunk.character_count <= 500
        for chunk in chunks
    )