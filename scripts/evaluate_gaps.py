import json
from dataclasses import asdict
from pathlib import Path

from src.evaluation.benchmark_loader import (
    load_gap_benchmark,
)

from src.evaluation.gap_evaluator import (
    GapEvaluator,
)

from src.evaluation.gap_metrics import (
    calculate_gap_metrics,
)


BENCHMARK_PATH = Path(
    "evaluation/benchmarks/"
    "gap_benchmark.json"
)

RESULT_PATH = Path(
    "evaluation/results/"
    "gap_results.json"
)


def main() -> None:

    cases = load_gap_benchmark(
        BENCHMARK_PATH
    )

    evaluator = GapEvaluator()

    results = [
        evaluator.evaluate_case(
            case,
            evidence_per_paper=8,
        )
        for case in cases
    ]

    metrics = calculate_gap_metrics(
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
        "Research-Gap Evaluation"
    )
    print(
        "======================="
    )

    print(
        f"Cases: {metrics.case_count}"
    )

    print(
        "Structural Pass Rate: "
        f"{metrics.structural_pass_rate:.2%}"
    )

    print(
        "Mean Signal Paper Coverage: "
        f"{metrics.mean_signal_paper_coverage:.2%}"
    )

    print(
        "Backend Validation Pass Rate: "
        f"{metrics.backend_validation_pass_rate:.2%}"
    )

    print(
        "Candidate Evidence Reference Integrity: "
        f"{metrics.candidate_evidence_reference_integrity:.2%}"
    )

    print(
        "Mean Dimension Population Rate: "
        f"{metrics.mean_dimension_population_rate:.2%}"
    )

    print(
        f"Total Candidates: "
        f"{metrics.total_candidates}"
    )

    print(
        f"Explicit Candidates: "
        f"{metrics.total_explicit_candidates}"
    )

    print(
        "Corpus-Imbalance Candidates: "
        f"{metrics.total_corpus_imbalance_candidates}"
    )

    print(
        "Insufficient-Evidence Candidates: "
        f"{metrics.total_insufficient_evidence_candidates}"
    )

    print()

    for result in results:

        print(
            f"{result.gap_id}: "
            f"{result.query}"
        )

        print(
            "  Requested Papers:",
            ", ".join(
                result.requested_papers
            ),
        )

        print(
            "  Signal Papers:",
            (
                ", ".join(
                    result.signal_papers
                )
                or "None"
            ),
        )

        print(
            "  Missing Signal Papers:",
            (
                ", ".join(
                    result.missing_signal_papers
                )
                or "None"
            ),
        )

        print(
            "  Signal Paper Coverage: "
            f"{result.signal_paper_coverage:.2%}"
        )

        print(
            f"  Signals: "
            f"{result.signal_count}"
        )

        print(
            f"  Candidates: "
            f"{result.candidate_count}"
        )

        print(
            f"  Explicit Candidates: "
            f"{result.explicit_candidate_count}"
        )

        print(
            "  Corpus-Imbalance Candidates: "
            f"{result.corpus_imbalance_candidate_count}"
        )

        print(
            "  Insufficient-Evidence Candidates: "
            f"{result.insufficient_evidence_candidate_count}"
        )

        print(
            "  Missing Candidate Evidence References:",
            (
                ", ".join(
                    result.missing_candidate_evidence_references
                )
                or "None"
            ),
        )

        print(
            "  Candidate Evidence Integrity: "
            f"{result.candidate_evidence_reference_integrity:.2%}"
        )

        print(
            "  Invalid Candidate Paper References:",
            (
                ", ".join(
                    result.invalid_candidate_paper_references
                )
                or "None"
            ),
        )

        print(
            "  Dimension Coverage Entries: "
            f"{result.dimension_coverage_count}"
        )

        print(
            "  Populated Dimensions: "
            f"{result.populated_dimension_count}"
        )

        print(
            "  Dimension Population Rate: "
            f"{result.dimension_population_rate:.2%}"
        )

        print(
            "  Backend Validation: "
            f"{result.backend_validation_valid}"
        )

        print(
            "  Backend Validation Issues: "
            f"{result.backend_validation_issue_count}"
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