from functools import lru_cache

from src.analysis.comparative_service import (
    ComparativeAnalysisService,
)
from src.analysis.gap_analysis_service import (
    ResearchGapAnalysisService,
)
from src.analysis.literature_review_renderer import (
    LiteratureReviewMarkdownRenderer,
)
from src.analysis.literature_review_service import (
    LiteratureReviewService,
)
from src.generation.answer_service import (
    GroundedAnswerService,
)
from src.tools.search_papers import (
    SearchPapersTool,
)


@lru_cache(maxsize=1)
def get_search_papers_tool() -> SearchPapersTool:
    """
    Return one shared Phase 6 paper-search tool.

    Retrieval remains inside the frozen backend.
    The UI only presents the returned evidence.
    """

    return SearchPapersTool()


@lru_cache(maxsize=1)
def get_grounded_answer_service() -> GroundedAnswerService:
    return GroundedAnswerService()


@lru_cache(maxsize=1)
def get_comparative_analysis_service() -> ComparativeAnalysisService:
    return ComparativeAnalysisService()


@lru_cache(maxsize=1)
def get_research_gap_analysis_service() -> ResearchGapAnalysisService:
    """
    Return one shared Phase 10 research-gap service.

    Gap detection, evidence classification,
    coverage analysis, and validation remain
    inside the frozen backend.
    """

    return ResearchGapAnalysisService()


@lru_cache(maxsize=1)
def get_literature_review_service() -> LiteratureReviewService:
    """
    Return one shared Phase 11 literature-review service.

    Review planning, evidence aggregation, synthesis,
    grounding validation, and deterministic generation
    remain inside the frozen backend.
    """

    return LiteratureReviewService()


@lru_cache(maxsize=1)
def get_literature_review_renderer() -> LiteratureReviewMarkdownRenderer:
    """
    Return one shared Markdown renderer.
    """

    return LiteratureReviewMarkdownRenderer()
