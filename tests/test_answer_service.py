from src.generation.answer_service import (
    GroundedAnswerService,
)

from src.generation.models import (
    EvidencePackage,
    GeneratedClaim,
    GeneratedDraft,
    GroundingEvidence,
)

from src.tools.search_papers import (
    PaperSearchResponse,
)


class FakeSearchTool:

    def search(
        self,
        query: str,
        top_k: int = 5,
    ):

        return PaperSearchResponse(
            query=query,
            result_count=0,
            results=[],
        )


class FakeCompareTool:

    def compare(
        self,
        paper_ids,
        query,
        evidence_per_paper=3,
    ):

        return {
            "query": query
        }


class FakePackageBuilder:

    def _package(
        self,
        query: str,
    ):

        return EvidencePackage(
            query=query,

            evidence=[
                GroundingEvidence(
                    evidence_id=(
                        "paper_a_chunk_0001"
                    ),

                    label="E1",

                    paper_id="paper_a",

                    page_number=3,

                    section="methodology",

                    text="Validated evidence.",

                    citation_text="Citation",
                )
            ],
        )

    def from_search(
        self,
        response,
    ):

        return self._package(
            response.query
        )

    def from_comparison(
        self,
        response,
    ):

        return self._package(
            response["query"]
        )


class FakeGenerator:

    def generate(
        self,
        package,
    ):

        return GeneratedDraft(
            query=package.query,

            answer_text=(
                "Grounded claim [E1]"
            ),

            claims=[
                GeneratedClaim(
                    claim_id="C1",

                    text="Grounded claim",

                    evidence_ids=[
                        "paper_a_chunk_0001"
                    ],
                )
            ],
        )


def build_service():

    return GroundedAnswerService(
        search_tool=(
            FakeSearchTool()
        ),

        compare_tool=(
            FakeCompareTool()
        ),

        package_builder=(
            FakePackageBuilder()
        ),

        generator=(
            FakeGenerator()
        ),
    )


def test_answer_search_returns_valid_grounded_answer():

    answer = (
        build_service()
        .answer_search(
            "How is feedback used?"
        )
    )

    assert (
        answer.validation.is_valid
    )

    assert len(
        answer.claims
    ) == 1


def test_answer_search_preserves_query():

    query = (
        "How is feedback used?"
    )

    answer = (
        build_service()
        .answer_search(
            query
        )
    )

    assert (
        answer.query
        == query
    )


def test_answer_comparison_returns_valid_answer():

    answer = (
        build_service()
        .answer_comparison(
            paper_ids=[
                "03_mutap",
                "05_coverup",
            ],

            query=(
                "Compare feedback approaches"
            ),
        )
    )

    assert (
        answer.validation.is_valid
    )

    assert (
        "[E1]"
        in answer.answer_text
    )