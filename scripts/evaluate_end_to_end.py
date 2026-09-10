import json
from dataclasses import asdict
from pathlib import Path

from src.evaluation.benchmark_loader import (
    load_end_to_end_benchmark,
)

from src.evaluation.end_to_end_evaluator import (
    EndToEndEvaluator,
)

from src.evaluation.end_to_end_metrics import (
    calculate_end_to_end_metrics,
)


BENCHMARK_PATH = Path(
    "evaluation/benchmarks/"
    "end_to_end_benchmark.json"
)

RESULT_PATH = Path(
    "evaluation/results/"
    "end_to_end_results.json"
)


def main() -> None:

    cases = load_end_to_end_benchmark(
        BENCHMARK_PATH
    )

    evaluator = EndToEndEvaluator()

    results = [
        evaluator.evaluate_case(
            case,
            top_k=8,
            evidence_per_paper=8,
        )
        for case in cases
    ]

    metrics = calculate_end_to_end_metrics(
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
        "End-to-End Evaluation"
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
        "Mean Stage Success Rate: "
        f"{metrics.mean_stage_success_rate:.2%}"
    )

    print(
        "Answer Success Rate: "
        f"{metrics.answer_success_rate:.2%}"
    )

    print(
        "Comparison Success Rate: "
        f"{metrics.comparison_success_rate:.2%}"
    )

    print(
        "Gap Analysis Success Rate: "
        f"{metrics.gap_analysis_success_rate:.2%}"
    )

    print(
        "Literature Review Success Rate: "
        f"{metrics.literature_review_success_rate:.2%}"
    )

    print(
        "Mean Comparison Paper Coverage: "
        f"{metrics.mean_comparison_paper_coverage:.2%}"
    )

    print(
        "Mean Gap Paper Coverage: "
        f"{metrics.mean_gap_paper_coverage:.2%}"
    )

    print(
        "Mean Literature Review Paper Coverage: "
        f"{metrics.mean_literature_review_paper_coverage:.2%}"
    )

    print(
        f"Total Answer Claims: "
        f"{metrics.total_answer_claims}"
    )

    print(
        f"Total Answer Evidence: "
        f"{metrics.total_answer_evidence}"
    )

    print(
        f"Total Comparison Findings: "
        f"{metrics.total_comparison_findings}"
    )

    print(
        f"Total Gap Candidates: "
        f"{metrics.total_gap_candidates}"
    )

    print(
        f"Total Review Findings: "
        f"{metrics.total_review_findings}"
    )

    print(
        f"Total Review Citations: "
        f"{metrics.total_review_citations}"
    )

    print(
        f"Total Shared Evidence IDs: "
        f"{metrics.total_shared_evidence_ids}"
    )

    print()

    for result in results:

        print(
            f"{result.workflow_id}: "
            f"{result.query}"
        )

        print(
            "  Answer Generated: "
            f"{result.answer_generated}"
        )

        print(
            "  Answer Claims: "
            f"{result.answer_claim_count}"
        )

        print(
            "  Answer Evidence: "
            f"{result.answer_evidence_count}"
        )

        print(
            "  Answer Validation: "
            f"{result.answer_validation_valid}"
        )

        print(
            "  Comparison Generated: "
            f"{result.comparison_generated}"
        )

        print(
            "  Comparison Profiles: "
            f"{result.comparison_profile_count}"
        )

        print(
            "  Comparison Matrix Rows: "
            f"{result.comparison_matrix_row_count}"
        )

        print(
            "  Comparison Findings: "
            f"{result.comparison_finding_count}"
        )

        print(
            "  Comparison Paper Coverage: "
            f"{result.comparison_paper_coverage:.2%}"
        )

        print(
            "  Gap Analysis Generated: "
            f"{result.gap_analysis_generated}"
        )

        print(
            "  Gap Signals: "
            f"{result.gap_signal_count}"
        )

        print(
            "  Gap Candidates: "
            f"{result.gap_candidate_count}"
        )

        print(
            "  Gap Validation: "
            f"{result.gap_validation_valid}"
        )

        print(
            "  Gap Paper Coverage: "
            f"{result.gap_paper_coverage:.2%}"
        )

        print(
            "  Literature Review Generated: "
            f"{result.literature_review_generated}"
        )

        print(
            "  Literature Review Sections: "
            f"{result.literature_review_section_count}"
        )

        print(
            "  Literature Review Findings: "
            f"{result.literature_review_finding_count}"
        )

        print(
            "  Literature Review Citations: "
            f"{result.literature_review_citation_count}"
        )

        print(
            "  Literature Review Validation: "
            f"{result.literature_review_validation_valid}"
        )

        print(
            "  Literature Review Paper Coverage: "
            f"{result.literature_review_paper_coverage:.2%}"
        )

        print(
            "  Shared Evidence IDs: "
            f"{result.shared_evidence_id_count}"
        )

        print(
            "  Invalid Comparison Paper References:",
            (
                ", ".join(
                    result.invalid_comparison_paper_references
                )
                or "None"
            ),
        )

        print(
            "  Invalid Gap Paper References:",
            (
                ", ".join(
                    result.invalid_gap_paper_references
                )
                or "None"
            ),
        )

        print(
            "  Invalid Review Paper References:",
            (
                ", ".join(
                    result.invalid_review_paper_references
                )
                or "None"
            ),
        )

        print(
            "  Stage Success: "
            f"{result.stage_success_count}/"
            f"{result.total_stage_count}"
        )

        print(
            "  Stage Success Rate: "
            f"{result.stage_success_rate:.2%}"
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