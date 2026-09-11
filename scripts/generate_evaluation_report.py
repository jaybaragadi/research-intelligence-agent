import json
from pathlib import Path
from typing import Any

RESULTS_DIR = Path("evaluation/results")
REPORT_PATH = Path("reports/phase13_evaluation_report.md")


RESULT_FILES = {
    "retrieval": (RESULTS_DIR / "retrieval_results.json"),
    "grounding": (RESULTS_DIR / "grounding_results.json"),
    "comparison": (RESULTS_DIR / "comparison_results.json"),
    "gaps": (RESULTS_DIR / "gap_results.json"),
    "literature_review": (RESULTS_DIR / "literature_review_results.json"),
    "end_to_end": (RESULTS_DIR / "end_to_end_results.json"),
}


def load_json(
    path: Path,
) -> dict[str, Any]:

    if not path.exists():

        raise FileNotFoundError(f"Missing evaluation result: {path}")

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def percent(
    value: float,
) -> str:

    return f"{value:.2%}"


def decimal(
    value: float,
) -> str:

    return f"{value:.4f}"


def build_report(
    data: dict[str, dict[str, Any]],
) -> str:

    retrieval = data["retrieval"]["metrics"]

    grounding = data["grounding"]["metrics"]

    comparison = data["comparison"]["metrics"]

    gaps = data["gaps"]["metrics"]

    review = data["literature_review"]["metrics"]

    end_to_end = data["end_to_end"]["metrics"]

    lines = [
        "# Phase 13 Evaluation Report",
        "",
        "## Research Intelligence Agent",
        "",
        (
            "This report summarizes the evaluation "
            "of the Research Intelligence Agent over "
            "the indexed software-testing research "
            "corpus."
        ),
        "",
        (
            "The evaluation measures retrieval, "
            "grounding, comparative analysis, "
            "research-gap analysis, literature-review "
            "generation, and end-to-end workflow "
            "integrity."
        ),
        "",
        (
            "> Scope note: These results apply to the "
            "current indexed corpus and benchmark "
            "cases. They should not be interpreted as "
            "universal accuracy over the full research "
            "literature."
        ),
        "",
        "## 1. Evaluation Scope",
        "",
        "The evaluation suite contains six layers:",
        "",
        "1. Retrieval evaluation",
        "2. Grounding evaluation",
        "3. Comparative-analysis evaluation",
        "4. Research-gap evaluation",
        "5. Literature-review evaluation",
        "6. End-to-end workflow evaluation",
        "",
        (
            "The system uses deterministic validation "
            "and evidence/provenance checks. Structural "
            "validation does not by itself prove "
            "semantic entailment or universal research "
            "correctness."
        ),
        "",
        "## 2. Evaluation Summary",
        "",
        "| Evaluation | Metric | Result |",
        "|---|---|---:|",
        ("| Retrieval | Hit@1 | " f"{percent(retrieval['hit_at_1'])} |"),
        ("| Retrieval | Hit@5 | " f"{percent(retrieval['hit_at_5'])} |"),
        ("| Retrieval | MRR | " f"{decimal(retrieval['mean_reciprocal_rank'])} |"),
        (
            "| Retrieval | Mean Recall@10 | "
            f"{percent(retrieval['mean_recall_at_10'])} |"
        ),
        (
            "| Grounding | Backend validation | "
            f"{percent(grounding['backend_validation_pass_rate'])} |"
        ),
        (
            "| Grounding | Claim-evidence coverage | "
            f"{percent(grounding['mean_claim_evidence_coverage'])} |"
        ),
        (
            "| Grounding | Provenance completeness | "
            f"{percent(grounding['mean_provenance_completeness'])} |"
        ),
        (
            "| Grounding | Expected-paper recall | "
            f"{percent(grounding['mean_expected_paper_recall'])} |"
        ),
        (
            "| Comparison | Structural pass rate | "
            f"{percent(comparison['structural_pass_rate'])} |"
        ),
        (
            "| Comparison | Matrix population | "
            f"{percent(comparison['mean_matrix_population_rate'])} |"
        ),
        (
            "| Research Gaps | Structural pass rate | "
            f"{percent(gaps['structural_pass_rate'])} |"
        ),
        (
            "| Research Gaps | Dimension population | "
            f"{percent(gaps['mean_dimension_population_rate'])} |"
        ),
        (
            "| Literature Review | Structural pass rate | "
            f"{percent(review['structural_pass_rate'])} |"
        ),
        (
            "| Literature Review | Finding-evidence coverage | "
            f"{percent(review['mean_finding_evidence_coverage'])} |"
        ),
        (
            "| End-to-End | Structural pass rate | "
            f"{percent(end_to_end['structural_pass_rate'])} |"
        ),
        (
            "| End-to-End | Mean stage success | "
            f"{percent(end_to_end['mean_stage_success_rate'])} |"
        ),
        "",
        "## 3. Retrieval Evaluation",
        "",
        (f"The retrieval benchmark contained " f"{retrieval['case_count']} cases."),
        "",
        (f"- Hit@1: " f"{percent(retrieval['hit_at_1'])}"),
        (f"- Hit@3: " f"{percent(retrieval['hit_at_3'])}"),
        (f"- Hit@5: " f"{percent(retrieval['hit_at_5'])}"),
        (f"- Mean Reciprocal Rank: " f"{decimal(retrieval['mean_reciprocal_rank'])}"),
        (f"- Mean Recall@3: " f"{percent(retrieval['mean_recall_at_3'])}"),
        (f"- Mean Recall@5: " f"{percent(retrieval['mean_recall_at_5'])}"),
        (f"- Mean Recall@10: " f"{percent(retrieval['mean_recall_at_10'])}"),
        "",
        (
            "Interpretation: the current hybrid "
            "semantic/lexical retriever generally "
            "discovers relevant papers within the "
            "larger top-10 candidate set, while "
            "early-ranking quality and multi-paper "
            "coverage remain opportunities for "
            "improvement."
        ),
        "",
        (
            "The retrieval benchmark is preserved as "
            "an unbiased baseline rather than tuning "
            "the retriever directly against these "
            "evaluation questions."
        ),
        "",
        "## 4. Grounding Evaluation",
        "",
        (f"The grounding benchmark contained " f"{grounding['case_count']} cases."),
        "",
        (
            f"- Backend validation pass rate: "
            f"{percent(grounding['backend_validation_pass_rate'])}"
        ),
        (
            f"- Claim-evidence coverage: "
            f"{percent(grounding['mean_claim_evidence_coverage'])}"
        ),
        (
            f"- Provenance completeness: "
            f"{percent(grounding['mean_provenance_completeness'])}"
        ),
        (
            f"- Evidence-reference integrity: "
            f"{percent(grounding['evidence_reference_integrity'])}"
        ),
        (
            f"- Mean expected-paper recall: "
            f"{percent(grounding['mean_expected_paper_recall'])}"
        ),
        "",
        (
            "Interpretation: generated claims preserved "
            "structural evidence traceability and "
            "paper/page provenance. Expected-paper "
            "recall was lower than structural grounding "
            "metrics, demonstrating that retrieval "
            "coverage and grounding integrity are "
            "separate concerns."
        ),
        "",
        (
            "These checks establish structural "
            "grounding. They do not independently prove "
            "semantic entailment between every claim "
            "and supporting passage."
        ),
        "",
        "## 5. Comparative-Analysis Evaluation",
        "",
        (f"- Cases: " f"{comparison['case_count']}"),
        (f"- Structural pass rate: " f"{percent(comparison['structural_pass_rate'])}"),
        (
            f"- Mean profile paper coverage: "
            f"{percent(comparison['mean_profile_paper_coverage'])}"
        ),
        (
            f"- Mean matrix paper coverage: "
            f"{percent(comparison['mean_matrix_paper_coverage'])}"
        ),
        (
            f"- Mean matrix population rate: "
            f"{percent(comparison['mean_matrix_population_rate'])}"
        ),
        (
            f"- Cell evidence-reference integrity: "
            f"{percent(comparison['cell_evidence_reference_integrity'])}"
        ),
        (
            f"- Finding evidence-reference integrity: "
            f"{percent(comparison['finding_evidence_reference_integrity'])}"
        ),
        "",
        (
            "Interpretation: requested papers were "
            "preserved through comparison profiles and "
            "matrices, and populated cells retained "
            "valid evidence references. Empty matrix "
            "cells are allowed when the indexed evidence "
            "does not support a comparison dimension."
        ),
        "",
        (
            "Matrix population is a coverage measure, "
            "not a comparison-accuracy score."
        ),
        "",
        "## 6. Research-Gap Evaluation",
        "",
        (f"- Cases: " f"{gaps['case_count']}"),
        (f"- Structural pass rate: " f"{percent(gaps['structural_pass_rate'])}"),
        (f"- Signal paper coverage: " f"{percent(gaps['mean_signal_paper_coverage'])}"),
        (
            f"- Backend validation pass rate: "
            f"{percent(gaps['backend_validation_pass_rate'])}"
        ),
        (
            f"- Candidate evidence-reference integrity: "
            f"{percent(gaps['candidate_evidence_reference_integrity'])}"
        ),
        (
            f"- Mean dimension population rate: "
            f"{percent(gaps['mean_dimension_population_rate'])}"
        ),
        (f"- Total candidates: " f"{gaps['total_candidates']}"),
        (f"- Explicit candidates: " f"{gaps['total_explicit_candidates']}"),
        (
            f"- Corpus-imbalance candidates: "
            f"{gaps['total_corpus_imbalance_candidates']}"
        ),
        (
            f"- Insufficient-evidence candidates: "
            f"{gaps['total_insufficient_evidence_candidates']}"
        ),
        "",
        (
            "Interpretation: the evaluated cases "
            "produced evidence-backed explicit gap "
            "candidates without requiring every gap "
            "taxonomy category to appear."
        ),
        "",
        (
            "The system intentionally distinguishes "
            "missing evidence in the indexed corpus "
            "from evidence that a topic is globally "
            "absent from the research literature."
        ),
        "",
        "## 7. Literature-Review Evaluation",
        "",
        (f"- Cases: " f"{review['case_count']}"),
        (f"- Structural pass rate: " f"{percent(review['structural_pass_rate'])}"),
        (
            f"- Backend validation pass rate: "
            f"{percent(review['backend_validation_pass_rate'])}"
        ),
        (
            f"- Review paper coverage: "
            f"{percent(review['mean_review_paper_coverage'])}"
        ),
        (
            f"- Section structure pass rate: "
            f"{percent(review['section_structure_pass_rate'])}"
        ),
        (
            f"- Finding-evidence coverage: "
            f"{percent(review['mean_finding_evidence_coverage'])}"
        ),
        (
            f"- Finding evidence-reference integrity: "
            f"{percent(review['finding_evidence_reference_integrity'])}"
        ),
        (
            f"- Provenance completeness: "
            f"{percent(review['mean_provenance_completeness'])}"
        ),
        (
            f"- Corpus-scope note pass rate: "
            f"{percent(review['corpus_scope_note_pass_rate'])}"
        ),
        (f"- Total findings: " f"{review['total_findings']}"),
        (f"- Total evidence placements: " f"{review['total_evidence_placements']}"),
        (f"- Total citations: " f"{review['total_citations']}"),
        "",
        (
            "Interpretation: literature reviews "
            "preserved the expected eight-section "
            "structure, evidence-backed findings, "
            "citations, provenance, and indexed-corpus "
            "scope statement."
        ),
        "",
        "## 8. End-to-End Evaluation",
        "",
        (f"- Cases: " f"{end_to_end['case_count']}"),
        (f"- Structural pass rate: " f"{percent(end_to_end['structural_pass_rate'])}"),
        (
            f"- Mean stage success rate: "
            f"{percent(end_to_end['mean_stage_success_rate'])}"
        ),
        (f"- Answer success rate: " f"{percent(end_to_end['answer_success_rate'])}"),
        (
            f"- Comparison success rate: "
            f"{percent(end_to_end['comparison_success_rate'])}"
        ),
        (
            f"- Gap-analysis success rate: "
            f"{percent(end_to_end['gap_analysis_success_rate'])}"
        ),
        (
            f"- Literature-review success rate: "
            f"{percent(end_to_end['literature_review_success_rate'])}"
        ),
        (
            f"- Comparison paper coverage: "
            f"{percent(end_to_end['mean_comparison_paper_coverage'])}"
        ),
        (f"- Gap paper coverage: " f"{percent(end_to_end['mean_gap_paper_coverage'])}"),
        (
            f"- Literature-review paper coverage: "
            f"{percent(end_to_end['mean_literature_review_paper_coverage'])}"
        ),
        (f"- Total answer claims: " f"{end_to_end['total_answer_claims']}"),
        (f"- Total comparison findings: " f"{end_to_end['total_comparison_findings']}"),
        (f"- Total gap candidates: " f"{end_to_end['total_gap_candidates']}"),
        (f"- Total review findings: " f"{end_to_end['total_review_findings']}"),
        (f"- Total review citations: " f"{end_to_end['total_review_citations']}"),
        (f"- Shared evidence IDs: " f"{end_to_end['total_shared_evidence_ids']}"),
        "",
        (
            "Interpretation: all benchmark workflows "
            "completed grounded answering, comparative "
            "analysis, gap analysis, and literature "
            "review generation while preserving "
            "stage-level validation and requested-paper "
            "scope where applicable."
        ),
        "",
        (
            "End-to-end structural success should not "
            "be interpreted as 100% semantic accuracy."
        ),
        "",
        "## 9. Regression Status",
        "",
        (
            "The final Phase 13.6 regression baseline "
            "contained 372 passing automated tests."
        ),
        "",
        "```text",
        "372 passed",
        "```",
        "",
        "## 10. Known Limitations",
        "",
        (
            "1. The evaluation corpus contains only "
            "the currently indexed research papers and "
            "is not an exhaustive representation of "
            "software-testing literature."
        ),
        (
            "2. Retrieval ranking remains the clearest "
            "measured weakness. Relevant papers are "
            "often discovered within the top-10 results "
            "but are not consistently ranked in the "
            "first few positions."
        ),
        (
            "3. Structural grounding verifies that "
            "claims reference existing evidence and "
            "retain provenance; it does not fully "
            "measure semantic entailment."
        ),
        (
            "4. The comparison evaluation measures "
            "paper coverage, matrix population, and "
            "evidence-reference integrity rather than "
            "human-rated comparative correctness."
        ),
        (
            "5. Research-gap findings apply to the "
            "indexed corpus. Missing evidence is not "
            "treated as proof of a universal literature "
            "gap."
        ),
        (
            "6. Literature-review evaluation measures "
            "structure, evidence coverage, provenance, "
            "and citations rather than expert-rated "
            "writing quality."
        ),
        (
            "7. The current benchmark sets are small "
            "and intended as reproducible engineering "
            "baselines rather than statistically "
            "comprehensive academic evaluations."
        ),
        "",
        "## 11. Overall Conclusion",
        "",
        (
            "The Research Intelligence Agent "
            "demonstrates an evidence-grounded research "
            "workflow spanning semantic retrieval, "
            "grounded question answering, comparative "
            "analysis, research-gap analysis, and "
            "literature-review generation."
        ),
        "",
        (
            "The strongest measured properties are "
            "evidence traceability, provenance "
            "preservation, structural validation, "
            "requested-paper coverage, and end-to-end "
            "workflow reliability."
        ),
        "",
        (
            "The primary measured improvement area is "
            "retrieval ranking. The baseline indicates "
            "stronger top-10 discovery than early-rank "
            "performance, providing a concrete target "
            "for future retriever improvements."
        ),
        "",
        (
            "The evaluation therefore supports the "
            "system as a reproducible research "
            "intelligence prototype while explicitly "
            "preserving the limitations of its corpus, "
            "benchmarks, retrieval quality, and "
            "structural evaluation methodology."
        ),
        "",
    ]

    return "\n".join(lines)


def main() -> None:

    data = {name: load_json(path) for name, path in RESULT_FILES.items()}

    report = build_report(data)

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        report,
        encoding="utf-8",
    )

    print("Phase 13 evaluation report generated:")

    print(REPORT_PATH)


if __name__ == "__main__":
    main()
