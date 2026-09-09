import json
from dataclasses import dataclass
from pathlib import Path

from src.config import settings
from src.models import PaperProfile
from src.tools.evidence_tool import (
    EvidenceRecord,
    EvidenceTool,
)


@dataclass
class CitationRecord:
    """
    Citation generated from validated evidence.

    The citation includes both human-readable
    research metadata and machine-verifiable
    provenance.
    """

    evidence_id: str

    paper_id: str

    title: str

    year: int | None

    page_number: int

    section: str | None

    chunk_id: str

    citation_text: str


class CitationTool:
    """
    Convert validated evidence into stable
    research citations.

    Citation provenance comes from EvidenceTool.

    Paper title/year come from Phase 3 metadata.

    The tool never accepts arbitrary page or
    paper values from the caller.
    """

    def __init__(
        self,
        evidence_tool: (
            EvidenceTool
            | None
        ) = None,
        metadata_directory: (
            Path
            | None
        ) = None,
    ) -> None:

        self.evidence_tool = (
            evidence_tool
            if evidence_tool is not None
            else EvidenceTool()
        )

        self.metadata_directory = (
            metadata_directory
            if metadata_directory is not None
            else settings.metadata_dir
        )

    def _metadata_path(
        self,
        paper_id: str,
    ) -> Path:
        """
        Return the Phase 3 metadata path.
        """

        return (
            self.metadata_directory
            / f"{paper_id}.json"
        )

    def _load_profile(
        self,
        paper_id: str,
    ) -> PaperProfile | None:
        """
        Load paper metadata when available.

        Missing metadata does not invalidate the
        evidence itself, so citation generation
        can fall back to the paper ID.
        """

        path = (
            self._metadata_path(
                paper_id
            )
        )

        if not path.exists():
            return None

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        return (
            PaperProfile.model_validate(
                data
            )
        )

    def _format_citation(
        self,
        evidence: EvidenceRecord,
        profile: PaperProfile | None,
    ) -> str:
        """
        Produce a stable human-readable
        evidence citation.
        """

        if profile is not None:

            source_name = (
                profile.title
            )

            year_text = (
                f" ({profile.year})"
                if profile.year
                is not None
                else ""
            )

        else:

            source_name = (
                evidence.paper_id
            )

            year_text = ""

        location_parts = [
            f"p. {evidence.page_number}"
        ]

        if evidence.section:

            location_parts.append(
                evidence.section
            )

        location_text = (
            ", ".join(
                location_parts
            )
        )

        return (
            f"{source_name}"
            f"{year_text}, "
            f"{location_text} "
            f"[{evidence.chunk_id}]"
        )

    def cite(
        self,
        evidence_id: str,
    ) -> CitationRecord:
        """
        Generate a citation from one validated
        evidence ID.
        """

        evidence = (
            self.evidence_tool.get(
                evidence_id
            )
        )

        profile = (
            self._load_profile(
                evidence.paper_id
            )
        )

        title = (
            profile.title
            if profile is not None
            else evidence.paper_id
        )

        year = (
            profile.year
            if profile is not None
            else None
        )

        citation_text = (
            self._format_citation(
                evidence=evidence,
                profile=profile,
            )
        )

        return CitationRecord(
            evidence_id=(
                evidence.evidence_id
            ),

            paper_id=(
                evidence.paper_id
            ),

            title=(
                title
            ),

            year=(
                year
            ),

            page_number=(
                evidence.page_number
            ),

            section=(
                evidence.section
            ),

            chunk_id=(
                evidence.chunk_id
            ),

            citation_text=(
                citation_text
            ),
        )

    def cite_many(
        self,
        evidence_ids: list[str],
    ) -> list[
        CitationRecord
    ]:
        """
        Generate citations for several evidence
        IDs while preserving caller order.
        """

        evidence_records = (
            self.evidence_tool.get_many(
                evidence_ids
            )
        )

        return [
            self.cite(
                evidence.evidence_id
            )

            for evidence
            in evidence_records
        ]


def cite_evidence(
    evidence_id: str,
) -> CitationRecord:
    """
    Convenience wrapper.
    """

    tool = CitationTool()

    return tool.cite(
        evidence_id
    )