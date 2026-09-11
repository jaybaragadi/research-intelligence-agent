from src.analysis.comparison_matrix import (
    ComparisonMatrixBuilder,
)
from src.analysis.comparison_models import (
    DimensionEvidence,
    PaperAnalysisProfile,
    PaperDimensionAnalysis,
)


def profile(
    paper_id: str,
    dimension: str,
    text: str,
):

    return PaperAnalysisProfile(
        paper_id=paper_id,
        dimensions=[
            PaperDimensionAnalysis(
                dimension=dimension,
                evidence=[
                    DimensionEvidence(
                        evidence_id=(f"{paper_id}_e1"),
                        paper_id=paper_id,
                        dimension=dimension,
                        page_number=2,
                        section="methodology",
                        text=text,
                        citation_text="Citation",
                        relevance_score=2.0,
                    )
                ],
            )
        ],
    )


def test_matrix_contains_all_dimensions():

    rows = ComparisonMatrixBuilder().build(
        requested_papers=[
            "03_mutap",
            "05_coverup",
        ],
        profiles=[],
    )

    assert len(rows) >= 5


def test_matrix_preserves_paper_order():

    rows = ComparisonMatrixBuilder().build(
        requested_papers=[
            "03_mutap",
            "05_coverup",
        ],
        profiles=[],
    )

    assert [cell.paper_id for cell in rows[0].cells] == [
        "03_mutap",
        "05_coverup",
    ]


def test_matrix_uses_strongest_evidence():

    rows = ComparisonMatrixBuilder().build(
        requested_papers=[
            "03_mutap",
            "05_coverup",
        ],
        profiles=[
            profile(
                "03_mutap",
                "feedback_signal",
                ("Surviving mutants are " "used as feedback."),
            )
        ],
    )

    row = next(row for row in rows if (row.dimension == "feedback_signal"))

    assert row.cells[0].summary == ("Surviving mutants are " "used as feedback.")


def test_empty_cell_is_none():

    rows = ComparisonMatrixBuilder().build(
        requested_papers=["03_mutap"],
        profiles=[],
    )

    assert all(row.cells[0].summary is None for row in rows)
