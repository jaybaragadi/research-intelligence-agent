from src.evaluation.models import (
    RetrievalBenchmarkCase,
)
from src.evaluation.retrieval_evaluator import (
    RetrievalEvaluator,
)
from src.evaluation.retrieval_metrics import (
    calculate_retrieval_metrics,
)
from src.tools.search_papers import (
    PaperSearchResponse,
    PaperSearchResult,
)


class FakeSearchTool:

    def __init__(
        self,
        paper_ids: list[str],
    ) -> None:

        self.paper_ids = paper_ids

    def search(
        self,
        query: str,
        top_k: int | None = None,
    ) -> PaperSearchResponse:

        results = []

        for rank, paper_id in enumerate(
            self.paper_ids,
            start=1,
        ):

            results.append(
                PaperSearchResult(
                    rank=rank,
                    paper_id=paper_id,
                    page_number=1,
                    section="Test",
                    score=1.0,
                    raw_score=1.0,
                    lexical_score=0.0,
                    chunk_id=(f"{paper_id}_chunk"),
                    text="Evidence",
                )
            )

        return PaperSearchResponse(
            query=query,
            result_count=len(results),
            results=results,
        )


def test_retrieval_evaluator_hit_at_1():

    case = RetrievalBenchmarkCase(
        question_id="R1",
        query="mutation testing",
        expected_papers=[
            "03_mutap",
        ],
    )

    evaluator = RetrievalEvaluator(
        search_tool=FakeSearchTool(
            [
                "03_mutap",
                "05_coverup",
            ]
        )
    )

    result = evaluator.evaluate_case(case)

    assert result.hit_at_1 is True
    assert result.hit_at_3 is True
    assert result.hit_at_5 is True
    assert result.reciprocal_rank == 1.0

    assert result.unique_retrieved_papers == [
        "03_mutap",
        "05_coverup",
    ]

    assert result.recall_at_3 == 1.0
    assert result.recall_at_5 == 1.0
    assert result.recall_at_10 == 1.0


def test_retrieval_evaluator_rank_two():

    case = RetrievalBenchmarkCase(
        question_id="R1",
        query="mutation testing",
        expected_papers=[
            "03_mutap",
        ],
    )

    evaluator = RetrievalEvaluator(
        search_tool=FakeSearchTool(
            [
                "05_coverup",
                "03_mutap",
            ]
        )
    )

    result = evaluator.evaluate_case(case)

    assert result.hit_at_1 is False
    assert result.hit_at_3 is True
    assert result.reciprocal_rank == 0.5

    assert result.recall_at_3 == 1.0


def test_retrieval_metrics():

    case = RetrievalBenchmarkCase(
        question_id="R1",
        query="test",
        expected_papers=[
            "03_mutap",
        ],
    )

    result_one = RetrievalEvaluator(
        search_tool=FakeSearchTool(
            [
                "03_mutap",
            ]
        )
    ).evaluate_case(case)

    result_two = RetrievalEvaluator(
        search_tool=FakeSearchTool(
            [
                "05_coverup",
                "03_mutap",
            ]
        )
    ).evaluate_case(case)

    metrics = calculate_retrieval_metrics(
        [
            result_one,
            result_two,
        ]
    )

    assert metrics.case_count == 2
    assert metrics.hit_at_1 == 0.5
    assert metrics.hit_at_3 == 1.0
    assert metrics.hit_at_5 == 1.0
    assert metrics.mean_reciprocal_rank == 0.75

    assert metrics.mean_recall_at_3 == 1.0

    assert metrics.mean_recall_at_5 == 1.0

    assert metrics.mean_recall_at_10 == 1.0


def test_recall_tracks_multiple_expected_papers():

    case = RetrievalBenchmarkCase(
        question_id="R4",
        query="iterative feedback",
        expected_papers=[
            "03_mutap",
            "05_coverup",
            "06_chatunitest",
        ],
    )

    evaluator = RetrievalEvaluator(
        search_tool=FakeSearchTool(
            [
                "03_mutap",
                "03_mutap",
                "08_telpa",
                "06_chatunitest",
                "10_coding_before_testing",
            ]
        )
    )

    result = evaluator.evaluate_case(
        case,
        top_k=10,
    )

    assert result.hit_at_1 is True

    assert result.recall_at_3 == 1 / 3

    assert result.recall_at_5 == 2 / 3

    assert result.recall_at_10 == 2 / 3

    assert result.missing_expected_papers == [
        "05_coverup",
    ]
