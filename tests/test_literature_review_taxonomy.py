from src.analysis.literature_review_models import (
    LiteratureReviewSectionType,
)
from src.analysis.literature_review_taxonomy import (
    LITERATURE_REVIEW_SECTIONS,
)


def test_review_taxonomy_contains_expected_sections():

    section_types = {
        definition.section_type for definition in LITERATURE_REVIEW_SECTIONS
    }

    assert LiteratureReviewSectionType.INTRODUCTION in section_types

    assert LiteratureReviewSectionType.GENERATION_STRATEGIES in section_types

    assert LiteratureReviewSectionType.FEEDBACK_AND_ITERATION in section_types

    assert LiteratureReviewSectionType.QUALITY_AND_EVALUATION in section_types

    assert LiteratureReviewSectionType.LIMITATIONS_AND_GAPS in section_types

    assert LiteratureReviewSectionType.FUTURE_DIRECTIONS in section_types

    assert LiteratureReviewSectionType.CONCLUSION in section_types


def test_generation_strategy_section_uses_generation_dimension():

    definition = next(
        item
        for item in LITERATURE_REVIEW_SECTIONS
        if item.section_type == LiteratureReviewSectionType.GENERATION_STRATEGIES
    )

    assert "generation_strategy" in definition.source_dimensions


def test_feedback_section_uses_feedback_and_iteration_dimensions():

    definition = next(
        item
        for item in LITERATURE_REVIEW_SECTIONS
        if item.section_type == LiteratureReviewSectionType.FEEDBACK_AND_ITERATION
    )

    assert "feedback_signal" in definition.source_dimensions

    assert "iteration_strategy" in definition.source_dimensions


def test_limitations_section_accepts_gap_signals():

    definition = next(
        item
        for item in LITERATURE_REVIEW_SECTIONS
        if item.section_type == LiteratureReviewSectionType.LIMITATIONS_AND_GAPS
    )

    assert definition.include_gap_signals is True


def test_future_directions_accepts_gap_signals():

    definition = next(
        item
        for item in LITERATURE_REVIEW_SECTIONS
        if item.section_type == LiteratureReviewSectionType.FUTURE_DIRECTIONS
    )

    assert definition.include_gap_signals is True
