from pathlib import Path

import numpy as np

from src.models import PaperChunk
from src.retrieval.faiss_store import (
    FaissStore,
)


def create_chunks(
) -> list[PaperChunk]:

    first_text = (
        "Mutation testing improves "
        "test quality."
    )

    second_text = (
        "Coverage-guided generation "
        "improves branch coverage."
    )

    return [
        PaperChunk(
            chunk_id=(
                "paper_chunk_0000"
            ),
            paper_id="paper",
            text=first_text,
            page_number=1,
            section="methodology",
            chunk_index=0,
            character_count=len(
                first_text
            ),
        ),
        PaperChunk(
            chunk_id=(
                "paper_chunk_0001"
            ),
            paper_id="paper",
            text=second_text,
            page_number=2,
            section="results",
            chunk_index=1,
            character_count=len(
                second_text
            ),
        ),
    ]


def test_faiss_store_build_and_load(
    tmp_path: Path,
):

    store = FaissStore(
        tmp_path
    )

    embeddings = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
        ],
        dtype=np.float32,
    )

    chunks = create_chunks()

    store.build(
        embeddings=embeddings,
        chunks=chunks,
    )

    assert (
        store.index_path.exists()
    )

    assert (
        store.metadata_path.exists()
    )

    index = store.load_index()

    assert index.ntotal == 2

    loaded_chunks = (
        store.load_chunks()
    )

    assert len(
        loaded_chunks
    ) == 2


def test_faiss_search_returns_best_match(
    tmp_path: Path,
):

    store = FaissStore(
        tmp_path
    )

    embeddings = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
        ],
        dtype=np.float32,
    )

    chunks = create_chunks()

    store.build(
        embeddings=embeddings,
        chunks=chunks,
    )

    query = np.array(
        [
            [1.0, 0.0]
        ],
        dtype=np.float32,
    )

    scores, indexes = (
        store.search(
            query_embedding=query,
            top_k=1,
        )
    )

    assert indexes[
        0
    ][0] == 0

    assert scores[
        0
    ][0] > 0.99