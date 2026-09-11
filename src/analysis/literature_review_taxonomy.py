from __future__ import annotations

from dataclasses import dataclass

from src.analysis.literature_review_models import (
    LiteratureReviewSectionType,
)


@dataclass(frozen=True)
class LiteratureReviewSectionDefinition:
    section_type: LiteratureReviewSectionType

    title: str

    objective: str

    source_dimensions: tuple[str, ...] = ()

    include_gap_signals: bool = False


LITERATURE_REVIEW_SECTIONS = (
    LiteratureReviewSectionDefinition(
        section_type=(LiteratureReviewSectionType.INTRODUCTION),
        title="Introduction",
        objective=(
            "Introduce the research topic and describe "
            "the scope of the indexed corpus."
        ),
    ),
    LiteratureReviewSectionDefinition(
        section_type=(LiteratureReviewSectionType.RESEARCH_LANDSCAPE),
        title="Research Landscape",
        objective=(
            "Summarize the major methodological patterns "
            "represented across the indexed papers."
        ),
        source_dimensions=("generation_strategy",),
    ),
    LiteratureReviewSectionDefinition(
        section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
        title="Test Generation Strategies",
        objective=(
            "Compare how studies generate, augment, or " "guide LLM-produced tests."
        ),
        source_dimensions=("generation_strategy",),
    ),
    LiteratureReviewSectionDefinition(
        section_type=(LiteratureReviewSectionType.FEEDBACK_AND_ITERATION),
        title="Feedback and Iterative Refinement",
        objective=(
            "Describe how feedback signals and iterative "
            "processes are used to improve generated tests."
        ),
        source_dimensions=(
            "feedback_signal",
            "iteration_strategy",
        ),
    ),
    LiteratureReviewSectionDefinition(
        section_type=(LiteratureReviewSectionType.QUALITY_AND_EVALUATION),
        title="Test Quality and Evaluation",
        objective=(
            "Synthesize the quality objectives, metrics, "
            "and evaluation methods used across studies."
        ),
        source_dimensions=(
            "quality_objective",
            "evaluation_method",
        ),
    ),
    LiteratureReviewSectionDefinition(
        section_type=(LiteratureReviewSectionType.LIMITATIONS_AND_GAPS),
        title="Limitations and Research Gaps",
        objective=(
            "Summarize explicitly reported limitations "
            "and corpus-level underrepresented areas "
            "without treating missing evidence as a "
            "universal literature gap."
        ),
        source_dimensions=("limitations",),
        include_gap_signals=True,
    ),
    LiteratureReviewSectionDefinition(
        section_type=(LiteratureReviewSectionType.FUTURE_DIRECTIONS),
        title="Future Research Directions",
        objective=(
            "Summarize future-work directions explicitly "
            "reported in the indexed papers."
        ),
        include_gap_signals=True,
    ),
    LiteratureReviewSectionDefinition(
        section_type=(LiteratureReviewSectionType.CONCLUSION),
        title="Conclusion",
        objective=(
            "Summarize the overall evidence patterns " "found in the indexed corpus."
        ),
    ),
)
