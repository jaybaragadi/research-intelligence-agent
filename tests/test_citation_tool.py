import json

from src.tools.citation_tool import (
    CitationTool,
)
from src.tools.evidence_tool import (
    EvidenceRecord,
)


class FakeEvidenceTool:
    """
    Deterministic evidence resolver.
    """

    def get(
        self,
        evidence_id: str,
    ) -> EvidenceRecord:

        return EvidenceRecord(
            evidence_id=(evidence_id),
            chunk_id=(evidence_id),
            paper_id="paper_a",
            page_number=5,
            section="methodology",
            text=("The approach uses " "coverage-guided feedback."),
        )

    def get_many(
        self,
        evidence_ids: list[str],
    ) -> list[EvidenceRecord]:

        return [self.get(evidence_id) for evidence_id in dict.fromkeys(evidence_ids)]


def create_metadata(
    tmp_path,
) -> None:

    payload = {
        "paper_id": "paper_a",
        "filename": "paper_a.pdf",
        "title": ("Example Research Paper"),
        "authors": ["Researcher One"],
        "year": 2025,
        "abstract": ("Example abstract."),
        "sections": [],
        "research_questions": [],
        "research_signals": [],
    }

    path = tmp_path / "paper_a.json"

    path.write_text(
        json.dumps(payload),
        encoding="utf-8",
    )


def test_citation_uses_validated_evidence(
    tmp_path,
):

    create_metadata(tmp_path)

    tool = CitationTool(
        evidence_tool=(FakeEvidenceTool()),
        metadata_directory=(tmp_path),
    )

    citation = tool.cite("paper_a_chunk_0001")

    assert citation.paper_id == "paper_a"

    assert citation.page_number == 5

    assert citation.section == "methodology"


def test_citation_includes_title_and_year(
    tmp_path,
):

    create_metadata(tmp_path)

    tool = CitationTool(
        evidence_tool=(FakeEvidenceTool()),
        metadata_directory=(tmp_path),
    )

    citation = tool.cite("paper_a_chunk_0001")

    assert citation.title == "Example Research Paper"

    assert citation.year == 2025

    assert "Example Research Paper" in citation.citation_text

    assert "2025" in citation.citation_text


def test_citation_contains_page_and_chunk(
    tmp_path,
):

    create_metadata(tmp_path)

    tool = CitationTool(
        evidence_tool=(FakeEvidenceTool()),
        metadata_directory=(tmp_path),
    )

    citation = tool.cite("paper_a_chunk_0001")

    assert "p. 5" in citation.citation_text

    assert "paper_a_chunk_0001" in citation.citation_text


def test_citation_falls_back_without_metadata(
    tmp_path,
):

    tool = CitationTool(
        evidence_tool=(FakeEvidenceTool()),
        metadata_directory=(tmp_path),
    )

    citation = tool.cite("paper_a_chunk_0001")

    assert citation.title == "paper_a"

    assert citation.year is None

    assert citation.citation_text.startswith("paper_a")


def test_cite_many_preserves_order(
    tmp_path,
):

    create_metadata(tmp_path)

    tool = CitationTool(
        evidence_tool=(FakeEvidenceTool()),
        metadata_directory=(tmp_path),
    )

    citations = tool.cite_many(
        [
            "paper_a_chunk_0001",
            "paper_a_chunk_0002",
        ]
    )

    assert [citation.evidence_id for citation in citations] == [
        "paper_a_chunk_0001",
        "paper_a_chunk_0002",
    ]
