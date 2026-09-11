from src.analysis.comparison_models import (
    DimensionEvidence,
)
from src.analysis.paper_profiler import (
    ComparativePaperProfiler,
)


def make_item(
    paper_id: str,
    dimension: str,
    score: float,
    evidence_id: str,
):

    return DimensionEvidence(
        evidence_id=evidence_id,
        paper_id=paper_id,
        dimension=dimension,
        page_number=3,
        section="methodology",
        text="Evidence",
        citation_text="Citation",
        relevance_score=score,
    )


def test_builds_profiles_in_requested_order():

    profiles = ComparativePaperProfiler().build_profiles(
        requested_papers=[
            "03_mutap",
            "05_coverup",
        ],
        classified_evidence=[
            make_item(
                "05_coverup",
                "feedback_signal",
                2.0,
                "coverup_1",
            ),
            make_item(
                "03_mutap",
                "feedback_signal",
                2.0,
                "mutap_1",
            ),
        ],
    )

    assert [profile.paper_id for profile in profiles] == [
        "03_mutap",
        "05_coverup",
    ]


def test_evidence_sorted_by_relevance():

    profiles = ComparativePaperProfiler().build_profiles(
        requested_papers=["03_mutap"],
        classified_evidence=[
            make_item(
                "03_mutap",
                "feedback_signal",
                1.0,
                "weak",
            ),
            make_item(
                "03_mutap",
                "feedback_signal",
                3.0,
                "strong",
            ),
        ],
    )

    evidence = profiles[0].dimensions[0].evidence

    assert evidence[0].evidence_id == "strong"


def test_profile_exists_without_evidence():

    profiles = ComparativePaperProfiler().build_profiles(
        requested_papers=[
            "03_mutap",
            "05_coverup",
        ],
        classified_evidence=[],
    )

    assert len(profiles) == 2

    assert profiles[0].dimensions == []
