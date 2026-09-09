from dataclasses import dataclass

from src.config import settings
from src.retrieval.faiss_store import (
    FaissStore,
)


@dataclass
class EvidenceRecord:
    """
    One validated piece of research evidence.

    The evidence ID is the original chunk ID
    created during Phase 4.

    Because chunk IDs map back to the exact
    indexed source passage, they form the
    provenance backbone for later agent claims.
    """

    evidence_id: str

    chunk_id: str

    paper_id: str

    page_number: int

    section: str | None

    text: str


class EvidenceTool:
    """
    Resolve evidence IDs back to exact indexed
    research-paper chunks.

    This tool prevents later components from
    manufacturing page numbers, sections, or
    evidence text.

    Evidence is always resolved from the
    persisted vector-store metadata.
    """

    def __init__(
        self,
        store: FaissStore | None = None,
    ) -> None:

        self.store = (
            store
            if store is not None
            else FaissStore(
                settings.vector_store_dir
            )
        )

        self._evidence_index: dict[
            str,
            EvidenceRecord,
        ] | None = None

    def _build_evidence_index(
        self,
    ) -> dict[
        str,
        EvidenceRecord,
    ]:
        """
        Build an in-memory mapping from
        chunk ID to exact evidence record.

        The index is created lazily and reused
        for the lifetime of this tool instance.
        """

        chunks = (
            self.store.load_chunks()
        )

        evidence_index: dict[
            str,
            EvidenceRecord,
        ] = {}

        for chunk in chunks:

            record = EvidenceRecord(
                evidence_id=(
                    chunk.chunk_id
                ),

                chunk_id=(
                    chunk.chunk_id
                ),

                paper_id=(
                    chunk.paper_id
                ),

                page_number=(
                    chunk.page_number
                ),

                section=(
                    chunk.section
                ),

                text=(
                    chunk.text
                ),
            )

            evidence_index[
                chunk.chunk_id
            ] = record

        return evidence_index

    @property
    def evidence_index(
        self,
    ) -> dict[
        str,
        EvidenceRecord,
    ]:
        """
        Lazily load evidence metadata.
        """

        if (
            self._evidence_index
            is None
        ):
            self._evidence_index = (
                self._build_evidence_index()
            )

        return self._evidence_index

    def get(
        self,
        evidence_id: str,
    ) -> EvidenceRecord:
        """
        Resolve one evidence ID.

        Raises
        ------
        ValueError
            If the ID is blank.

        KeyError
            If the evidence ID does not exist
            in the indexed corpus.
        """

        evidence_id = (
            evidence_id.strip()
        )

        if not evidence_id:

            raise ValueError(
                "evidence_id cannot be empty"
            )

        if (
            evidence_id
            not in self.evidence_index
        ):
            raise KeyError(
                "Evidence not found: "
                f"{evidence_id}"
            )

        return (
            self.evidence_index[
                evidence_id
            ]
        )

    def get_many(
        self,
        evidence_ids: list[str],
    ) -> list[
        EvidenceRecord
    ]:
        """
        Resolve multiple evidence IDs while
        preserving caller order.

        Duplicate evidence IDs are removed.
        """

        cleaned_ids = [
            evidence_id.strip()

            for evidence_id
            in evidence_ids

            if evidence_id.strip()
        ]

        if not cleaned_ids:

            raise ValueError(
                "At least one evidence ID is required"
            )

        unique_ids = list(
            dict.fromkeys(
                cleaned_ids
            )
        )

        return [
            self.get(
                evidence_id
            )

            for evidence_id
            in unique_ids
        ]

    def validate(
        self,
        evidence_id: str,
        paper_id: str | None = None,
        page_number: int | None = None,
        section: str | None = None,
    ) -> bool:
        """
        Validate expected provenance against
        the indexed source record.

        This will later allow the agent layer to
        verify that a proposed citation actually
        belongs to the claimed source.
        """

        record = self.get(
            evidence_id
        )

        if (
            paper_id is not None
            and record.paper_id
            != paper_id
        ):
            return False

        if (
            page_number is not None
            and record.page_number
            != page_number
        ):
            return False

        if (
            section is not None
            and record.section
            != section
        ):
            return False

        return True


def get_evidence(
    evidence_id: str,
) -> EvidenceRecord:
    """
    Convenience wrapper.
    """

    tool = EvidenceTool()

    return tool.get(
        evidence_id
    )