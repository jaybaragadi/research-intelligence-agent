from src.generation.query_focus import (
    build_comparison_focus_query,
)


def test_focus_query_removes_paper_names():

    result = build_comparison_focus_query(
        query=("Compare how MuTAP and " "CoverUp improve generated tests"),
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    assert result == "improve generated tests"


def test_focus_query_handles_long_paper_name():

    result = build_comparison_focus_query(
        query=("Compare Coding Before Testing " "and TELPA for feedback"),
        paper_ids=[
            "10_coding_before_testing",
            "08_telpa",
        ],
    )

    assert result == "feedback"


def test_focus_query_never_returns_empty():

    original = "Compare MuTAP and CoverUp"

    result = build_comparison_focus_query(
        query=original,
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    assert result
