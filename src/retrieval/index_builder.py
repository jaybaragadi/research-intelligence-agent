from dataclasses import dataclass

from src.config import settings
from src.retrieval.chunk_loader import (
    load_all_chunks,
)
from src.retrieval.embedding_model import (
    EmbeddingModel,
)
from src.retrieval.faiss_store import (
    FaissStore,
)


@dataclass
class IndexBuildSummary:
    chunk_count: int
    embedding_dimension: int
    index_path: str
    metadata_path: str


def build_vector_index() -> IndexBuildSummary:
    """
    Build the semantic retrieval index from all
    Phase-4 chunks.
    """

    chunks = load_all_chunks(settings.chunks_dir)

    if not chunks:

        raise RuntimeError("No chunks found. " "Run Phase 4 before Phase 5.")

    print(f"Loaded {len(chunks)} chunks.")

    texts = [chunk.text for chunk in chunks]

    embedding_model = EmbeddingModel(settings.embedding_model)

    print()
    print("Generating embeddings...")

    embeddings = embedding_model.encode_documents(texts)

    print()
    print("Embedding matrix:")

    print(f"    Rows      : " f"{embeddings.shape[0]}")

    print(f"    Dimension : " f"{embeddings.shape[1]}")

    store = FaissStore(settings.vector_store_dir)

    store.build(
        embeddings=embeddings,
        chunks=chunks,
    )

    return IndexBuildSummary(
        chunk_count=len(chunks),
        embedding_dimension=(embeddings.shape[1]),
        index_path=str(store.index_path),
        metadata_path=str(store.metadata_path),
    )
