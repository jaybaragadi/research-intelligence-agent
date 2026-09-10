import json
from dataclasses import asdict
from pathlib import Path

from src.evaluation.benchmark_loader import (
    load_literature_review_benchmark,
)

from src.evaluation.literature_review_evaluator import (
    LiteratureReviewEvaluator,
)

from src.evaluation.literature_review_metrics import (
    calculate_literature_review_metrics,
)


BENCHMARK_PATH = Path(
    "evaluation/benchmarks/"
    "literature_review_benchmark.json"
)

RESULT_PATH = Path(
    "evaluation/results/"
    "literature_review_results.json"
)


def main() -> None:

    cases = load_literature_review_benchmark(
        BENCHMARK_PATH
    )

    evaluator = LiteratureReviewEvaluator()

    results = [
        evaluator.evaluate_case(
            case,
            evidence_per_paper=8,
        )
        for case in cases
    ]

    metrics = (
        calculate_literature_review_metrics(
            results
        )
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
        "Literature-Review Evaluation"
    )
    print(
        "============================"
    )

    print(
        f"Cases: {metrics.case_count}"
    )

    print(
        "Structural Pass Rate: "
        f"{metrics.structural_pass_rate:.2%}"
    )

    print(
        "Backend Validation Pass Rate: "
        f"{metrics.backend_validation_pass_rate:.2%}"
    )

    print(
        "Mean Review Paper Coverage: "
        f"{metrics.mean_review_paper_coverage:.2%}"
    )

    print(
        "Section Structure Pass Rate: "
        f"{metrics.section_structure_pass_rate:.2%}"
    )

    print(
        "Mean Finding Evidence Coverage: "
        f"{metrics.mean_finding_evidence_coverage:.2%}"
    )

    print(
        "Finding Evidence Reference Integrity: "
        f"{metrics.finding_evidence_reference_integrity:.2%}"
    )

    print(
        "Mean Provenance Completeness: "
        f"{metrics.mean_provenance_completeness:.2%}"
    )

    print(
        "Corpus Scope Note Pass Rate: "
        f"{metrics.corpus_scope_note_pass_rate:.2%}"
    )

    print(
        f"Total Findings: "
        f"{metrics.total_findings}"
    )

    print(
        f"Total Evidence Placements: "
        f"{metrics.total_evidence_placements}"
    )

    print(
        f"Total Citations: "
        f"{metrics.total_citations}"
    )

    print()

    for result in results:

        print(
            f"{result.review_id}: "
            f"{result.title}"
        )

        print(
            "  Review Paper Coverage: "
            f"{result.review_paper_coverage:.2%}"
        )

        print(
            "  Missing Review Papers:",
            (
                ", ".join(
                    result.missing_review_papers
                )
                or "None"
            ),
        )

        print(
            "  Invalid Review Papers:",
            (
                ", ".join(
                    result.invalid_review_papers
                )
                or "None"
            ),
        )

        print(
            "  Sections: "
            f"{result.section_count}/"
            f"{result.expected_section_count}"
        )

        print(
            "  Section Structure Complete: "
            f"{result.section_structure_complete}"
        )

        print(
            "  Missing Section Types:",
            (
                ", ".join(
                    result.missing_section_types
                )
                or "None"
            ),
        )

        print(
            "  Duplicate Section Types:",
            (
                ", ".join(
                    result.duplicate_section_types
                )
                or "None"
            ),
        )

        print(
            f"  Findings: "
            f"{result.finding_count}"
        )

        print(
            "  Findings With Evidence: "
            f"{result.findings_with_evidence}"
        )

        print(
            "  Findings Without Evidence: "
            f"{result.findings_without_evidence}"
        )

        print(
            "  Finding Evidence Coverage: "
            f"{result.finding_evidence_coverage:.2%}"
        )

        print(
            "  Evidence Placements: "
            f"{result.evidence_count}"
        )

        print(
            "  Unique Evidence Items: "
            f"{result.unique_evidence_count}"
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
            "  Provenance Completeness: "
            f"{result.provenance_completeness:.2%}"
        )

        print(
            f"  Citations: "
            f"{result.citation_count}"
        )

        print(
            "  Corpus Scope Note Present: "
            f"{result.corpus_scope_note_present}"
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