from src.analysis.comparative_service import (
    ComparativeAnalysisService,
)

from src.generation.models import (
    EvidencePackage,
    GroundingEvidence,
)


class FakeCompareTool:

    def compare(
        self,
        paper_ids,
        query,
        evidence_per_paper=6,
    ):

        return {
            "paper_ids": paper_ids,
            "query": query,
        }


class FakePackageBuilder:

    def from_comparison(
        self,
        response,
    ):

        return EvidencePackage(
            query=response["query"],

            evidence=[
                GroundingEvidence(
                    evidence_id=(
                        "03_mutap_chunk_0001"
                    ),

                    label="E1",

                    paper_id="03_mutap",

                    page_number=1,

                    section="methodology",

                    text=(
                        "Surviving mutants are "
                        "used as feedback to "
                        "improve generated tests."
                    ),

                    citation_text=(
                        "MuTAP citation"
                    ),
                ),

                GroundingEvidence(
                    evidence_id=(
                        "05_coverup_chunk_0001"
                    ),

                    label="E2",

                    paper_id="05_coverup",

                    page_number=1,

                    section="methodology",

                    text=(
                        "Coverage feedback is "
                        "used iteratively to "
                        "improve generated tests."
                    ),

                    citation_text=(
                        "CoverUp citation"
                    ),
                ),
            ],
        )


def build_service():

    return ComparativeAnalysisService(
        compare_tool=(
            FakeCompareTool()
        ),

        package_builder=(
            FakePackageBuilder()
        ),
    )


def test_service_preserves_original_query():

    query = (
        "Compare how MuTAP and "
        "CoverUp improve generated tests"
    )

    result = (
        build_service()
        .analyze(
            paper_ids=[
                "03_mutap",
                "05_coverup",
            ],

            query=query,
        )
    )

    assert (
        result.query
        == query
    )


def test_service_builds_profiles():

    result = (
        build_service()
        .analyze(
            paper_ids=[
                "03_mutap",
                "05_coverup",
            ],

            query=(
                "Compare feedback"
            ),
        )
    )

    assert len(
        result.profiles
    ) == 2


def test_service_builds_feedback_matrix():

    result = (
        build_service()
        .analyze(
            paper_ids=[
                "03_mutap",
                "05_coverup",
            ],

            query=(
                "Compare feedback"
            ),
        )
    )

    feedback = next(
        row
        for row in result.matrix
        if (
            row.dimension
            == "feedback_signal"
        )
    )

    assert all(
        cell.summary is not None
        for cell
        in feedback.cells
    )


def test_service_creates_shared_findings():

    result = (
        build_service()
        .analyze(
            paper_ids=[
                "03_mutap",
                "05_coverup",
            ],

            query=(
                "Compare feedback"
            ),
        )
    )

    assert any(
        finding.finding_type
        == "shared_dimension"

        for finding
        in result.findings
    )


def test_service_requires_two_papers():

    import pytest

    with pytest.raises(
        ValueError
    ):

        (
            build_service()
            .analyze(
                paper_ids=[
                    "03_mutap"
                ],

                query="Compare",
            )
        )