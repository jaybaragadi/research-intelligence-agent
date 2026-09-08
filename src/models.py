from pathlib import Path

from pydantic import BaseModel, Field


class PaperMetadata(BaseModel):
    """Structured metadata extracted from a research paper."""

    paper_id: str

    title: str = "Unknown Title"

    authors: list[str] = Field(
        default_factory=list
    )

    year: int | None = None

    abstract: str | None = None

    methodology: str | None = None

    datasets: list[str] = Field(
        default_factory=list
    )

    metrics: list[str] = Field(
        default_factory=list
    )

    findings: list[str] = Field(
        default_factory=list
    )

    limitations: list[str] = Field(
        default_factory=list
    )

    future_work: list[str] = Field(
        default_factory=list
    )

    source_path: Path | None = None


class PaperChunk(BaseModel):
    """A searchable text segment extracted from a paper."""

    chunk_id: str

    paper_id: str

    text: str

    page_number: int | None = None

    section: str | None = None

    chunk_index: int


class SearchResult(BaseModel):
    """One result returned from semantic research search."""

    paper_id: str

    chunk_id: str

    text: str

    score: float

    page_number: int | None = None

    section: str | None = None


class Evidence(BaseModel):
    """Evidence supporting a research claim."""

    paper_id: str

    claim: str

    supporting_text: str

    page_number: int | None = None

    section: str | None = None


class PaperComparison(BaseModel):
    """Structured comparison between research papers."""

    paper_ids: list[str]

    common_methods: list[str] = Field(
        default_factory=list
    )

    differences: list[str] = Field(
        default_factory=list
    )

    agreements: list[str] = Field(
        default_factory=list
    )

    contradictions: list[str] = Field(
        default_factory=list
    )

    limitations: list[str] = Field(
        default_factory=list
    )