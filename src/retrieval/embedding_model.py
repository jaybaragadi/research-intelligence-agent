import numpy as np
from sentence_transformers import (
    SentenceTransformer,
)


class EmbeddingModel:
    """
    Local sentence-transformer embedding model.

    The model converts research chunks and user
    questions into dense vectors.

    Embeddings are normalized so FAISS inner-product
    search becomes cosine-similarity search.
    """

    def __init__(
        self,
        model_name: str,
    ) -> None:

        self.model_name = model_name

        self._model: SentenceTransformer | None = None

    @property
    def model(
        self,
    ) -> SentenceTransformer:

        if self._model is None:

            print(f"Loading embedding model: " f"{self.model_name}")

            self._model = SentenceTransformer(self.model_name)

        return self._model

    def encode_documents(
        self,
        texts: list[str],
    ) -> np.ndarray:
        """
        Embed document chunks.
        """

        if not texts:

            return np.empty(
                (0, 0),
                dtype=np.float32,
            )

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        return np.asarray(
            embeddings,
            dtype=np.float32,
        )

    def encode_query(
        self,
        query: str,
    ) -> np.ndarray:
        """
        Embed one research question.
        """

        if not query.strip():

            raise ValueError("Query cannot be empty")

        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return np.asarray(
            embedding,
            dtype=np.float32,
        )
