from scripts.generate_evaluation_report import (
    build_report,
)


def build_test_data():

    return {
        "retrieval": {
            "metrics": {
                "case_count": 5,
                "hit_at_1": 0.4,
                "hit_at_3": 0.4,
                "hit_at_5": 0.6,
                "mean_reciprocal_rank": 0.5119,
                "mean_recall_at_3": 0.2444,
                "mean_recall_at_5": 0.4889,
                "mean_recall_at_10": 0.8222,
            }
        },
        "grounding": {
            "metrics": {
                "case_count": 5,
                "backend_validation_pass_rate": 1.0,
                "mean_claim_evidence_coverage": 1.0,
                "mean_provenance_completeness": 1.0,
                "evidence_reference_integrity": 1.0,
                "mean_expected_paper_recall": 0.7556,
            }
        },
        "comparison": {
            "metrics": {
                "case_count": 3,
                "structural_pass_rate": 1.0,
                "mean_profile_paper_coverage": 1.0,
                "mean_matrix_paper_coverage": 1.0,
                "mean_matrix_population_rate": 0.7407,
                "cell_evidence_reference_integrity": 1.0,
                "finding_evidence_reference_integrity": 1.0,
            }
        },
        "gaps": {
            "metrics": {
                "case_count": 3,
                "structural_pass_rate": 1.0,
                "mean_signal_paper_coverage": 1.0,
                "backend_validation_pass_rate": 1.0,
                "candidate_evidence_reference_integrity": 1.0,
                "mean_dimension_population_rate": 0.9444,
                "total_candidates": 14,
                "total_explicit_candidates": 14,
                "total_corpus_imbalance_candidates": 0,
                "total_insufficient_evidence_candidates": 0,
            }
        },
        "literature_review": {
            "metrics": {
                "case_count": 3,
                "structural_pass_rate": 1.0,
                "backend_validation_pass_rate": 1.0,
                "mean_review_paper_coverage": 1.0,
                "section_structure_pass_rate": 1.0,
                "mean_finding_evidence_coverage": 1.0,
                "finding_evidence_reference_integrity": 1.0,
                "mean_provenance_completeness": 1.0,
                "corpus_scope_note_pass_rate": 1.0,
                "total_findings": 17,
                "total_evidence_placements": 212,
                "total_citations": 159,
            }
        },
        "end_to_end": {
            "metrics": {
                "case_count": 3,
                "structural_pass_rate": 1.0,
                "mean_stage_success_rate": 1.0,
                "answer_success_rate": 1.0,
                "comparison_success_rate": 1.0,
                "gap_analysis_success_rate": 1.0,
                "literature_review_success_rate": 1.0,
                "mean_comparison_paper_coverage": 1.0,
                "mean_gap_paper_coverage": 1.0,
                "mean_literature_review_paper_coverage": 1.0,
                "total_answer_claims": 15,
                "total_answer_evidence": 24,
                "total_comparison_findings": 16,
                "total_gap_candidates": 16,
                "total_review_findings": 17,
                "total_review_citations": 160,
                "total_shared_evidence_ids": 160,
            }
        },
    }


def test_report_contains_key_metrics():

    report = build_report(build_test_data())

    assert "40.00%" in report
    assert "60.00%" in report
    assert "0.5119" in report
    assert "82.22%" in report
    assert "75.56%" in report
    assert "74.07%" in report
    assert "94.44%" in report


def test_report_contains_limitations():

    report = build_report(build_test_data())

    assert "## 10. Known Limitations" in report

    assert "Structural grounding" in report

    assert "Missing evidence is not " "treated as proof" in report

    assert "retrieval ranking" in report.lower()


def test_report_contains_all_evaluation_sections():

    report = build_report(build_test_data())

    assert "## 3. Retrieval Evaluation" in report

    assert "## 4. Grounding Evaluation" in report

    assert "## 5. Comparative-Analysis Evaluation" in report

    assert "## 6. Research-Gap Evaluation" in report

    assert "## 7. Literature-Review Evaluation" in report

    assert "## 8. End-to-End Evaluation" in report
