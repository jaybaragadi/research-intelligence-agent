import json
from dataclasses import asdict
from pathlib import Path

from src.evaluation.benchmark_loader import (
    load_grounding_benchmark,
)

from src.evaluation.grounding_evaluator import (
    GroundingEvaluator,
)

from src.evaluation.grounding_metrics import (
    calculate_grounding_metrics,
)


BENCHMARK_PATH = Path(
    "evaluation/benchmarks/"
    "grounding_benchmark.json"
)

RESULT_PATH = Path(
    "evaluation/results/"
    "grounding_results.json"
)


def main() -> None:

    cases = load_grounding_benchmark(
        BENCHMARK_PATH
    )

    evaluator = GroundingEvaluator()

    results = [
        evaluator.evaluate_case(
            case,
            top_k=8,
        )
        for case in cases
    ]

    metrics = calculate_grounding_metrics(
        results
    )

    output = {
        "metrics": asdict(
            metrics
        ),
        "results": [
            asdict(result)
            for result in results
        ],
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
    print(
        "Grounding Evaluation"
    )
    print(
        "===================="
    )

    print(
        f"Cases: {metrics.case_count}"
    )

    print(
        "Backend Validation Pass Rate: "
        f"{metrics.backend_validation_pass_rate:.2%}"
    )

    print(
        "Claim Evidence Coverage: "
        f"{metrics.mean_claim_evidence_coverage:.2%}"
    )

    print(
        "Provenance Completeness: "
        f"{metrics.mean_provenance_completeness:.2%}"
    )

    print(
        "Evidence Reference Integrity: "
        f"{metrics.evidence_reference_integrity:.2%}"
    )

    print(
        "Mean Expected Paper Recall: "
        f"{metrics.mean_expected_paper_recall:.2%}"
    )

    print()

    for result in results:

        print(
            f"{result.question_id}: "
            f"{result.query}"
        )

        print(
            f"  Claims: "
            f"{result.claim_count}"
        )

        print(
            f"  Evidence: "
            f"{result.evidence_count}"
        )

        print(
            "  Claim Evidence Coverage: "
            f"{result.claim_evidence_coverage:.2%}"
        )

        print(
            "  Provenance Completeness: "
            f"{result.provenance_completeness:.2%}"
        )

        print(
            "  Backend Validation: "
            f"{result.backend_validation_valid}"
        )

        print(
            "  Missing Evidence References:",
            (
                ", ".join(
                    result.missing_evidence_references
                )
                or "None"
            ),
        )

        print(
            "  Evidence Papers:",
            (
                ", ".join(
                    result.evidence_papers
                )
                or "None"
            ),
        )

        print(
            "  Expected Papers:",
            (
                ", ".join(
                    result.expected_papers
                )
                or "None"
            ),
        )

        print(
            "  Matched Expected Papers:",
            (
                ", ".join(
                    result.matched_expected_papers
                )
                or "None"
            ),
        )

        print(
            "  Expected Paper Recall: "
            f"{result.expected_paper_recall:.2%}"
        )

        print()

    print(
        "Saved evaluation results to:"
    )
    print(
        RESULT_PATH
    )


if __name__ == "__main__":
    main()