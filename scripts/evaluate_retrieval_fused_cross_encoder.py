import json
from dataclasses import asdict
from pathlib import Path

from src.evaluation.benchmark_loader import load_retrieval_benchmark
from src.evaluation.retrieval_evaluator import RetrievalEvaluator
from src.evaluation.retrieval_metrics import calculate_retrieval_metrics
from src.retrieval.fused_cross_encoder_reranker import (
    FusedCrossEncoderReranker,
)
from src.tools.search_papers import SearchPapersTool

BENCHMARK_PATH = Path("evaluation/benchmarks/retrieval_benchmark.json")

RESULT_PATH = Path("evaluation/results/retrieval_fused_cross_encoder_results.json")


def main() -> None:
    cases = load_retrieval_benchmark(BENCHMARK_PATH)

    reranker = FusedCrossEncoderReranker(
        candidate_k=30,
        cross_encoder_weight=0.5,
    )

    search_tool = SearchPapersTool(
        retriever=reranker,
    )

    evaluator = RetrievalEvaluator(
        search_tool=search_tool,
    )

    results = [
        evaluator.evaluate_case(
            case,
            top_k=10,
        )
        for case in cases
    ]

    metrics = calculate_retrieval_metrics(results)

    output = {
        "configuration": {
            "retriever": ("fused_cross_encoder_reranker"),
            "candidate_k": 30,
            "cross_encoder_weight": 0.5,
        },
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
    print("Fused Cross-Encoder Retrieval Evaluation")
    print("========================================")

    print(f"Cases: {metrics.case_count}")

    print(f"Hit@1: {metrics.hit_at_1:.2%}")

    print(f"Hit@3: {metrics.hit_at_3:.2%}")

    print(f"Hit@5: {metrics.hit_at_5:.2%}")

    print("MRR: " f"{metrics.mean_reciprocal_rank:.4f}")

    print("Mean Recall@3: " f"{metrics.mean_recall_at_3:.2%}")

    print("Mean Recall@5: " f"{metrics.mean_recall_at_5:.2%}")

    print("Mean Recall@10: " f"{metrics.mean_recall_at_10:.2%}")

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

        print(f"  Hit@1: " f"{result.hit_at_1:.2%}")

        print(f"  Hit@3: " f"{result.hit_at_3:.2%}")

        print(f"  Hit@5: " f"{result.hit_at_5:.2%}")

        print(
            "  Matched:",
            ", ".join(result.matched_papers) or "None",
        )

        print(
            "  Missing:",
            ", ".join(result.missing_expected_papers) or "None",
        )

        print("  RR: " f"{result.reciprocal_rank:.4f}")

        print("  Recall@3: " f"{result.recall_at_3:.2%}")

        print("  Recall@5: " f"{result.recall_at_5:.2%}")

        print("  Recall@10: " f"{result.recall_at_10:.2%}")

        print()

    print("Saved fused cross-encoder " "evaluation results to:")

    print(RESULT_PATH)


if __name__ == "__main__":
    main()
