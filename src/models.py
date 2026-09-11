from pathlib import Path

from pydantic import BaseModel, Field


class PaperMetadata(BaseModel):
    """
    Structured metadata extracted from a research paper.
    """

    paper_id: str

    title: str = "Unknown Title"

    authors: list[str] = Field(default_factory=list)

    year: int | None = None

    abstract: str | None = None

    methodology: str | None = None

    datasets: list[str] = Field(default_factory=list)

    metrics: list[str] = Field(default_factory=list)

    findings: list[str] = Field(default_factory=list)

    limitations: list[str] = Field(default_factory=list)

    future_work: list[str] = Field(default_factory=list)

    source_path: Path | None = None


class PaperChunk(BaseModel):
    """
    Searchable research-paper text segment with provenance.
    """

    chunk_id: str

    paper_id: str

    text: str

    page_number: int

    section: str | None = None

    chunk_index: int

    character_count: int


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

    common_methods: list[str] = Field(default_factory=list)

    differences: list[str] = Field(default_factory=list)

    agreements: list[str] = Field(default_factory=list)

    contradictions: list[str] = Field(default_factory=list)

    limitations: list[str] = Field(default_factory=list)


class ExtractedPage(BaseModel):
    """Text extracted from one PDF page."""

    page_number: int
    text: str
    character_count: int


class ExtractedPaper(BaseModel):
    """Structured raw extraction from one research paper."""

    paper_id: str
    filename: str
    source_path: Path

    total_pages: int
    extracted_pages: int
    empty_pages: int

    pages: list[ExtractedPage] = Field(default_factory=list)


class SectionLocation(BaseModel):
    """Location of a recognized research-paper section."""

    canonical_name: str
    matched_heading: str
    page_number: int


class ResearchSignal(BaseModel):
    """
    Candidate evidence found in a paper for a research category.

    This is deliberately called a signal because Phase 3 does not
    yet ask an LLM to interpret the passage.
    """

    category: str
    page_number: int
    snippet: str
    matched_keyword: str


class PaperProfile(BaseModel):
    """
    Structured Phase 3 representation of a research paper.
    """

    paper_id: str
    filename: str

    title: str = "Unknown Title"

    authors: list[str] = Field(default_factory=list)

    year: int | None = None

    abstract: str | None = None

    sections: list[SectionLocation] = Field(default_factory=list)

    research_questions: list[str] = Field(default_factory=list)

    research_signals: list[ResearchSignal] = Field(default_factory=list)
