import json
from pathlib import Path

import faiss
import numpy as np

from src.models import PaperChunk

INDEX_FILENAME = "research_chunks.faiss"
METADATA_FILENAME = "research_chunks_metadata.json"


class FaissStore:
    """
    Persistent FAISS vector store for research chunks.

    FAISS stores vectors.

    The JSON metadata file stores the mapping:

        FAISS row
            ↓
        PaperChunk

    This keeps semantic retrieval connected to
    paper/page/section provenance.
    """

    def __init__(
        self,
        vector_store_directory: Path,
    ) -> None:

        self.vector_store_directory = vector_store_directory

        self.index_path = vector_store_directory / INDEX_FILENAME

        self.metadata_path = vector_store_directory / METADATA_FILENAME

    def build(
        self,
        embeddings: np.ndarray,
        chunks: list[PaperChunk],
    ) -> None:
        """
        Create and persist a FAISS cosine-similarity
        index.
        """

        if embeddings.ndim != 2:

            raise ValueError("Embeddings must be a " "2-dimensional array")

        if len(embeddings) != len(chunks):

            raise ValueError("Embedding count must match " "chunk count")

        if len(chunks) == 0:

            raise ValueError("Cannot build index with " "zero chunks")

        self.vector_store_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatIP(dimension)

        index.add(embeddings.astype(np.float32))

        faiss.write_index(
            index,
            str(self.index_path),
        )

        metadata = {
            "vector_count": len(chunks),
            "dimension": dimension,
            "chunks": [chunk.model_dump(mode="json") for chunk in chunks],
        }

        self.metadata_path.write_text(
            json.dumps(
                metadata,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def load_index(
        self,
    ) -> faiss.Index:
        """
        Load persisted FAISS index.
        """

        if not self.index_path.exists():

            raise FileNotFoundError("FAISS index not found: " f"{self.index_path}")

        return faiss.read_index(str(self.index_path))

    def load_chunks(
        self,
    ) -> list[PaperChunk]:
        """
        Load metadata associated with FAISS rows.
        """

        if not self.metadata_path.exists():

            raise FileNotFoundError(
                "Vector metadata not found: " f"{self.metadata_path}"
            )

        data = json.loads(self.metadata_path.read_text(encoding="utf-8"))

        return [PaperChunk.model_validate(chunk) for chunk in data["chunks"]]

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int,
    ) -> tuple[
        np.ndarray,
        np.ndarray,
    ]:
        """
        Search FAISS and return:

        scores
        vector indexes
        """

        if top_k <= 0:

            raise ValueError("top_k must be positive")

        index = self.load_index()

        query_embedding = query_embedding.astype(np.float32)

        scores, indexes = index.search(
            query_embedding,
            top_k,
        )

        return scores, indexes
