import json
from dataclasses import asdict
from pathlib import Path

from src.evaluation.benchmark_loader import (
    load_retrieval_benchmark,
)
from src.evaluation.retrieval_evaluator import (
    RetrievalEvaluator,
)
from src.evaluation.retrieval_metrics import (
    calculate_retrieval_metrics,
)

BENCHMARK_PATH = Path("evaluation/benchmarks/" "retrieval_benchmark.json")

RESULT_PATH = Path("evaluation/results/" "retrieval_results.json")


def main() -> None:

    cases = load_retrieval_benchmark(BENCHMARK_PATH)

    evaluator = RetrievalEvaluator()

    results = [
        evaluator.evaluate_case(
            case,
            top_k=10,
        )
        for case in cases
    ]

    metrics = calculate_retrieval_metrics(results)

    output = {
        "metrics": asdict(metrics),
        "results": [asdict(result) for result in results],
    }

    RESULT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    RESULT_PATH.write_text(
        json.dumps(
            output,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print("Retrieval Evaluation")
    print("====================")

    print(f"Cases: {metrics.case_count}")

    print(f"Hit@1: " f"{metrics.hit_at_1:.2%}")

    print(f"Hit@3: " f"{metrics.hit_at_3:.2%}")

    print(f"Hit@5: " f"{metrics.hit_at_5:.2%}")

    print(f"MRR: " f"{metrics.mean_reciprocal_rank:.4f}")

    print(f"Mean Recall@3: " f"{metrics.mean_recall_at_3:.2%}")

    print(f"Mean Recall@5: " f"{metrics.mean_recall_at_5:.2%}")

    print(f"Mean Recall@10: " f"{metrics.mean_recall_at_10:.2%}")

    print()

    for result in results:

        print(f"{result.question_id}: " f"{result.query}")

        print(
            "  Expected:",
            ", ".join(result.expected_papers),
        )

        print(
            "  Retrieved:",
            ", ".join(result.retrieved_papers),
        )

        print(
            "  Unique papers:",
            ", ".join(result.unique_retrieved_papers),
        )

        print(f"  Hit@1: {result.hit_at_1:.2%}")

        print(f"  Hit@3: {result.hit_at_3:.2%}")

        print(f"  Hit@5: {result.hit_at_5:.2%}")

        print(
            "  Matched:",
            ", ".join(result.matched_papers) or "None",
        )

        print(
            "  Missing:",
            ", ".join(result.missing_expected_papers) or "None",
        )

        print(f"  RR: " f"{result.reciprocal_rank:.4f}")

        print(f"  Recall@3: " f"{result.recall_at_3:.2%}")

        print(f"  Recall@5: " f"{result.recall_at_5:.2%}")

        print(f"  Recall@10: " f"{result.recall_at_10:.2%}")

        print()

    print("Saved evaluation results to:")

    print(RESULT_PATH)


if __name__ == "__main__":
    main()
