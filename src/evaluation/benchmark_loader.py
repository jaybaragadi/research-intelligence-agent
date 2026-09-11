import json
from pathlib import Path

from src.evaluation.models import (
    ComparisonBenchmarkCase,
    EndToEndBenchmarkCase,
    GapBenchmarkCase,
    GroundingBenchmarkCase,
    LiteratureReviewBenchmarkCase,
    RetrievalBenchmarkCase,
)


def load_end_to_end_benchmark(
    path: str | Path,
) -> list[EndToEndBenchmarkCase]:

    benchmark_path = Path(path)

    with benchmark_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        raw_cases = json.load(file)

    return [
        EndToEndBenchmarkCase(
            workflow_id=item["workflow_id"],
            query=item["query"],
            paper_ids=item["paper_ids"],
            title=item["title"],
            description=item.get(
                "description",
                "",
            ),
        )
        for item in raw_cases
    ]


def load_literature_review_benchmark(
    path: str | Path,
) -> list[LiteratureReviewBenchmarkCase]:

    benchmark_path = Path(path)

    with benchmark_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        raw_cases = json.load(file)

    return [
        LiteratureReviewBenchmarkCase(
            review_id=item["review_id"],
            title=item["title"],
            query=item["query"],
            paper_ids=item["paper_ids"],
            description=item.get(
                "description",
                "",
            ),
        )
        for item in raw_cases
    ]


def load_gap_benchmark(
    path: str | Path,
) -> list[GapBenchmarkCase]:

    benchmark_path = Path(path)

    with benchmark_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        raw_cases = json.load(file)

    return [
        GapBenchmarkCase(
            gap_id=item["gap_id"],
            query=item["query"],
            paper_ids=item["paper_ids"],
            description=item.get(
                "description",
                "",
            ),
        )
        for item in raw_cases
    ]


def load_comparison_benchmark(
    path: str | Path,
) -> list[ComparisonBenchmarkCase]:

    benchmark_path = Path(path)

    with benchmark_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        raw_cases = json.load(file)

    return [
        ComparisonBenchmarkCase(
            comparison_id=item["comparison_id"],
            query=item["query"],
            paper_ids=item["paper_ids"],
            description=item.get(
                "description",
                "",
            ),
        )
        for item in raw_cases
    ]


def load_grounding_benchmark(
    path: str | Path,
) -> list[GroundingBenchmarkCase]:

    benchmark_path = Path(path)

    with benchmark_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        raw_cases = json.load(file)

    return [
        GroundingBenchmarkCase(
            question_id=item["question_id"],
            query=item["query"],
            expected_papers=item.get(
                "expected_papers",
                [],
            ),
        )
        for item in raw_cases
    ]


def load_retrieval_benchmark(
    path: str | Path,
) -> list[RetrievalBenchmarkCase]:

    benchmark_path = Path(path)

    with benchmark_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        raw_cases = json.load(file)

    return [
        RetrievalBenchmarkCase(
            question_id=item["question_id"],
            query=item["query"],
            expected_papers=item["expected_papers"],
            description=item.get(
                "description",
                "",
            ),
        )
        for item in raw_cases
    ]
