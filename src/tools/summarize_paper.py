import json
from dataclasses import dataclass, field
from pathlib import Path

from src.config import settings
from src.models import PaperProfile


SUMMARY_CATEGORIES = (
    "methodology",
    "findings",
    "limitations",
    "future_work",
)


@dataclass
class SummaryEvidence:
    """
    One evidence passage used in a structured
    paper summary.
    """

    category: str
    page_number: int
    snippet: str
    matched_keyword: str


@dataclass
class PaperSummary:
    """
    Deterministic structured summary of one
    research paper.

    This object contains extracted metadata and
    evidence. It does not contain LLM-generated
    interpretation.
    """

    paper_id: str
    filename: str

    title: str
    year: int | None
    authors: list[str]

    abstract: str | None

    research_questions: list[str]

    sections: list[str]

    evidence: dict[
        str,
        list[SummaryEvidence],
    ] = field(
        default_factory=dict
    )


class SummarizePaperTool:
    """
    Build a structured evidence-backed profile
    for one paper.

    Phase 6 intentionally avoids LLM-generated
    summaries.

    The tool exposes deterministic research
    structure that can later be supplied to the
    research agent.
    """

    def __init__(
        self,
        metadata_directory: Path | None = None,
    ) -> None:

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
        Return the metadata JSON path for a paper.
        """

        return (
            self.metadata_directory
            / f"{paper_id}.json"
        )


    def _load_profile(
        self,
        paper_id: str,
    ) -> PaperProfile:
        """
        Load and validate a paper metadata profile.
        """

        if not paper_id.strip():

            raise ValueError(
                "paper_id cannot be empty"
            )

        path = self._metadata_path(
            paper_id
        )

        if not path.exists():

            raise FileNotFoundError(
                "Paper metadata not found: "
                f"{paper_id}"
            )

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        return PaperProfile.model_validate(
            data
        )


    def _group_evidence(
        self,
        profile: PaperProfile,
    ) -> dict[
        str,
        list[SummaryEvidence],
    ]:
        """
        Group Phase 3 research signals into
        summary categories.
        """

        grouped: dict[
            str,
            list[SummaryEvidence],
        ] = {
            category: []
            for category
            in SUMMARY_CATEGORIES
        }

        for signal in (
            profile.research_signals
        ):

            if (
                signal.category
                not in grouped
            ):
                continue

            grouped[
                signal.category
            ].append(
                SummaryEvidence(
                    category=(
                        signal.category
                    ),
                    page_number=(
                        signal.page_number
                    ),
                    snippet=(
                        signal.snippet
                    ),
                    matched_keyword=(
                        signal.matched_keyword
                    ),
                )
            )

        return grouped


    def summarize(
        self,
        paper_id: str,
    ) -> PaperSummary:
        """
        Build the structured summary.
        """

        profile = (
            self._load_profile(
                paper_id
            )
        )

        section_names = [
            section.canonical_name
            for section
            in profile.sections
        ]

        evidence = (
            self._group_evidence(
                profile
            )
        )

        return PaperSummary(
            paper_id=profile.paper_id,
            filename=profile.filename,

            title=profile.title,
            year=profile.year,
            authors=list(
                profile.authors
            ),

            abstract=profile.abstract,

            research_questions=list(
                profile.research_questions
            ),

            sections=section_names,

            evidence=evidence,
        )


def summarize_paper(
    paper_id: str,
) -> PaperSummary:
    """
    Convenience function for callers that do not
    need to manage a tool instance.
    """

    tool = SummarizePaperTool()

    return tool.summarize(
        paper_id
    )