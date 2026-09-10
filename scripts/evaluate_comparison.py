import json
from dataclasses import asdict
from pathlib import Path

from src.evaluation.benchmark_loader import (
    load_comparison_benchmark,
)

from src.evaluation.comparison_evaluator import (
    ComparisonEvaluator,
)

from src.evaluation.comparison_metrics import (
    calculate_comparison_metrics,
)


BENCHMARK_PATH = Path(
    "evaluation/benchmarks/"
    "comparison_benchmark.json"
)

RESULT_PATH = Path(
    "evaluation/results/"
    "comparison_results.json"
)


def main() -> None:

    cases = load_comparison_benchmark(
        BENCHMARK_PATH
    )

    evaluator = ComparisonEvaluator()

    results = [
        evaluator.evaluate_case(
            case,
            evidence_per_paper=6,
        )
        for case in cases
    ]

    metrics = calculate_comparison_metrics(
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
        "Comparison Evaluation"
    )
    print(
        "====================="
    )

    print(
        f"Cases: {metrics.case_count}"
    )

    print(
        "Structural Pass Rate: "
        f"{metrics.structural_pass_rate:.2%}"
    )

    print(
        "Mean Profile Paper Coverage: "
        f"{metrics.mean_profile_paper_coverage:.2%}"
    )

    print(
        "Mean Matrix Paper Coverage: "
        f"{metrics.mean_matrix_paper_coverage:.2%}"
    )

    print(
        "Mean Matrix Population Rate: "
        f"{metrics.mean_matrix_population_rate:.2%}"
    )

    print(
        "Cell Evidence Reference Integrity: "
        f"{metrics.cell_evidence_reference_integrity:.2%}"
    )

    print(
        "Finding Evidence Reference Integrity: "
        f"{metrics.finding_evidence_reference_integrity:.2%}"
    )

    print()

    for result in results:

        print(
            f"{result.comparison_id}: "
            f"{result.query}"
        )

        print(
            "  Requested Papers:",
            ", ".join(
                result.requested_papers
            ),
        )

        print(
            "  Profile Papers:",
            (
                ", ".join(
                    result.profile_papers
                )
                or "None"
            ),
        )

        print(
            "  Matrix Papers:",
            (
                ", ".join(
                    result.matrix_papers
                )
                or "None"
            ),
        )

        print(
            "  Missing Profile Papers:",
            (
                ", ".join(
                    result.missing_profile_papers
                )
                or "None"
            ),
        )

        print(
            "  Missing Matrix Papers:",
            (
                ", ".join(
                    result.missing_matrix_papers
                )
                or "None"
            ),
        )

        print(
            "  Profile Paper Coverage: "
            f"{result.profile_paper_coverage:.2%}"
        )

        print(
            "  Matrix Paper Coverage: "
            f"{result.matrix_paper_coverage:.2%}"
        )

        print(
            f"  Dimensions: "
            f"{result.dimension_count}"
        )

        print(
            f"  Matrix Cells: "
            f"{result.matrix_cell_count}"
        )

        print(
            f"  Populated Cells: "
            f"{result.populated_cell_count}"
        )

        print(
            f"  Empty Cells: "
            f"{result.empty_cell_count}"
        )

        print(
            "  Matrix Population Rate: "
            f"{result.matrix_population_rate:.2%}"
        )

        print(
            f"  Profile Evidence Items: "
            f"{result.profile_evidence_count}"
        )

        print(
            "  Missing Cell Evidence References:",
            (
                ", ".join(
                    result.missing_cell_evidence_references
                )
                or "None"
            ),
        )

        print(
            "  Cell Evidence Integrity: "
            f"{result.cell_evidence_reference_integrity:.2%}"
        )

        print(
            f"  Findings: "
            f"{result.finding_count}"
        )

        print(
            "  Missing Finding Evidence References:",
            (
                ", ".join(
                    result.missing_finding_evidence_references
                )
                or "None"
            ),
        )

        print(
            "  Finding Evidence Integrity: "
            f"{result.finding_evidence_reference_integrity:.2%}"
        )

        print(
            "  Invalid Finding Paper References:",
            (
                ", ".join(
                    result.invalid_finding_paper_references
                )
                or "None"
            ),
        )

        print(
            "  Structural Valid: "
            f"{result.structural_valid}"
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