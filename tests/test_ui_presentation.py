from src.ui.presentation import (
    evidence_section,
    evidence_title,
    grounding_status,
)

from src.ui.presentation import (
    comparison_cell_status,
    coverage_label,
    dimension_label,
    page_intro,
    evidence_section,
    evidence_title,
    gap_confidence_label,
    gap_type_label,
    grounding_status,
    join_evidence_ids,
    literature_review_filename,
    result_section_label,
    review_section_label,
    review_validation_status,
    search_result_title,
    search_score_label,
    signal_type_label,
)

from src.analysis.gap_analysis_service import (
    ResearchGapAnalysisService,
)


def test_page_intro():

    title, description = page_intro(
        "Research Q&A",
        "Ask evidence-grounded questions.",
    )

    assert title == "Research Q&A"
    assert description == "Ask evidence-grounded questions."

    
def test_search_result_title():

    assert (
        search_result_title(
            rank=1,
            paper_id="03_mutap",
            page_number=7,
        )
        == "#1 | 03_mutap | Page 7"
    )


def test_search_score_label():

    assert (
        search_score_label(
            0.812345
        )
        == "0.8123"
    )


def test_result_section_label():

    assert (
        result_section_label(
            "methodology"
        )
        == "methodology"
    )


def test_result_section_label_missing():

    assert (
        result_section_label(
            None
        )
        == "Unspecified"
    )

def test_review_section_label():

    assert (
        review_section_label(
            "feedback_and_iteration"
        )
        == "Feedback And Iteration"
    )


def test_literature_review_filename():

    assert (
        literature_review_filename(
            "MuTAP and CoverUp Literature Review"
        )
        == "mutap_and_coverup_literature_review.md"
    )


def test_literature_review_filename_empty():

    assert (
        literature_review_filename(
            ""
        )
        == "literature_review.md"
    )


def test_review_validation_status_valid():

    class Validation:
        valid = True

    assert (
        review_validation_status(
            Validation()
        )
        == "Valid"
    )


def test_review_validation_status_invalid():

    class Validation:
        valid = False

    assert (
        review_validation_status(
            Validation()
        )
        == "Invalid"
    )


def test_review_validation_status_none():

    assert (
        review_validation_status(
            None
        )
        == "Not Available"
    )


def test_gap_type_label_explicit():

    assert (
        gap_type_label(
            "explicit"
        )
        == "Explicit Gap"
    )


def test_gap_type_label_corpus_imbalance():

    assert (
        gap_type_label(
            "corpus_imbalance"
        )
        == "Corpus Imbalance"
    )


def test_gap_type_label_insufficient_evidence():

    assert (
        gap_type_label(
            "insufficient_evidence"
        )
        == "Insufficient Evidence"
    )


def test_gap_confidence_label():

    assert (
        gap_confidence_label(
            "high"
        )
        == "High"
    )


def test_signal_type_label():

    assert (
        signal_type_label(
            "future_work"
        )
        == "Future Work"
    )


def test_coverage_label():

    assert (
        coverage_label(
            "feedback_signal",
            6,
            10,
        )
        == "Feedback Signal: 6/10 papers"
    )

def test_evidence_title():

    result = evidence_title(
        evidence_id="03_mutap_chunk_0085",
        paper_id="03_mutap",
        page_number=13,
    )

    assert result == (
        "03_mutap_chunk_0085 | "
        "03_mutap | Page 13"
    )


def test_evidence_section():

    assert (
        evidence_section(
            "methodology"
        )
        == "methodology"
    )


def test_missing_evidence_section():

    assert (
        evidence_section(
            None
        )
        == "Unspecified"
    )


def test_grounding_status_valid():

    assert (
        grounding_status(
            True
        )
        == "Yes"
    )


def test_grounding_status_invalid():

    assert (
        grounding_status(
            False
        )
        == "No"
    )



def test_dimension_label_known_dimension():

    assert (
        dimension_label(
            "generation_strategy"
        )
        == "Generation Strategy"
    )


def test_dimension_label_unknown_dimension():

    assert (
        dimension_label(
            "new_research_dimension"
        )
        == "New Research Dimension"
    )


def test_comparison_cell_status_with_summary():

    assert (
        comparison_cell_status(
            "Uses mutation feedback."
        )
        == "Uses mutation feedback."
    )


def test_comparison_cell_status_without_summary():

    result = (
        comparison_cell_status(
            None
        )
    )

    assert (
        "No matching validated evidence"
        in result
    )


def test_join_evidence_ids():

    result = join_evidence_ids(
        [
            "E1",
            "E2",
        ]
    )

    assert result == "E1, E2"


def test_join_empty_evidence_ids():

    assert (
        join_evidence_ids([])
        == "None"
    )

