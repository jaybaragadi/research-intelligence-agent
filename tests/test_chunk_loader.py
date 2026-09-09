import json

from src.retrieval.chunk_loader import (
    discover_chunk_files,
    load_chunks_from_file,
)


def test_discover_chunk_files(
    tmp_path,
):
    first = (
        tmp_path
        / "paper_a.json"
    )

    second = (
        tmp_path
        / "paper_b.json"
    )

    first.write_text(
        "{}",
        encoding="utf-8",
    )

    second.write_text(
        "{}",
        encoding="utf-8",
    )

    files = (
        discover_chunk_files(
            tmp_path
        )
    )

    assert len(files) == 2


def test_load_chunks_from_file(
    tmp_path,
):
    text = (
        "Mutation testing evaluates "
        "generated unit tests."
    )

    payload = {
        "paper_id": "paper_a",

        "chunk_count": 1,

        "chunks": [
            {
                "chunk_id": (
                    "paper_a_chunk_0000"
                ),

                "paper_id": (
                    "paper_a"
                ),

                "text": text,

                "page_number": 3,

                "section": (
                    "methodology"
                ),

                "chunk_index": 0,

                "character_count": (
                    len(text)
                ),
            }
        ],
    }

    path = (
        tmp_path
        / "paper_a.json"
    )

    path.write_text(
        json.dumps(
            payload
        ),

        encoding="utf-8",
    )

    chunks = (
        load_chunks_from_file(
            path
        )
    )

    assert len(chunks) == 1

    assert (
        chunks[0].paper_id
        == "paper_a"
    )

    assert (
        chunks[0].page_number
        == 3
    )

    assert (
        chunks[0].section
        == "methodology"
    )