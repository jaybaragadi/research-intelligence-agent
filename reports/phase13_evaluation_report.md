# Phase 13 Evaluation Report

## Research Intelligence Agent

This report summarizes the evaluation of the Research Intelligence Agent over the indexed software-testing research corpus.

The evaluation measures retrieval, grounding, comparative analysis, research-gap analysis, literature-review generation, and end-to-end workflow integrity.

> Scope note: These results apply to the current indexed corpus and benchmark cases. They should not be interpreted as universal accuracy over the full research literature.

## 1. Evaluation Scope

The evaluation suite contains six layers:

1. Retrieval evaluation
2. Grounding evaluation
3. Comparative-analysis evaluation
4. Research-gap evaluation
5. Literature-review evaluation
6. End-to-end workflow evaluation

The system uses deterministic validation and evidence/provenance checks. Structural validation does not by itself prove semantic entailment or universal research correctness.

## 2. Evaluation Summary

| Evaluation | Metric | Result |
|---|---|---:|
| Retrieval | Hit@1 | 40.00% |
| Retrieval | Hit@5 | 60.00% |
| Retrieval | MRR | 0.5119 |
| Retrieval | Mean Recall@10 | 82.22% |
| Grounding | Backend validation | 100.00% |
| Grounding | Claim-evidence coverage | 100.00% |
| Grounding | Provenance completeness | 100.00% |
| Grounding | Expected-paper recall | 75.56% |
| Comparison | Structural pass rate | 100.00% |
| Comparison | Matrix population | 74.07% |
| Research Gaps | Structural pass rate | 100.00% |
| Research Gaps | Dimension population | 94.44% |
| Literature Review | Structural pass rate | 100.00% |
| Literature Review | Finding-evidence coverage | 100.00% |
| End-to-End | Structural pass rate | 100.00% |
| End-to-End | Mean stage success | 100.00% |

## 3. Retrieval Evaluation

The retrieval benchmark contained 5 cases.

- Hit@1: 40.00%
- Hit@3: 40.00%
- Hit@5: 60.00%
- Mean Reciprocal Rank: 0.5119
- Mean Recall@3: 24.44%
- Mean Recall@5: 48.89%
- Mean Recall@10: 82.22%

Interpretation: the current hybrid semantic/lexical retriever generally discovers relevant papers within the larger top-10 candidate set, while early-ranking quality and multi-paper coverage remain opportunities for improvement.

The retrieval benchmark is preserved as an unbiased baseline rather than tuning the retriever directly against these evaluation questions.

## 4. Grounding Evaluation

The grounding benchmark contained 5 cases.

- Backend validation pass rate: 100.00%
- Claim-evidence coverage: 100.00%
- Provenance completeness: 100.00%
- Evidence-reference integrity: 100.00%
- Mean expected-paper recall: 75.56%

Interpretation: generated claims preserved structural evidence traceability and paper/page provenance. Expected-paper recall was lower than structural grounding metrics, demonstrating that retrieval coverage and grounding integrity are separate concerns.

These checks establish structural grounding. They do not independently prove semantic entailment between every claim and supporting passage.

## 5. Comparative-Analysis Evaluation

- Cases: 3
- Structural pass rate: 100.00%
- Mean profile paper coverage: 100.00%
- Mean matrix paper coverage: 100.00%
- Mean matrix population rate: 74.07%
- Cell evidence-reference integrity: 100.00%
- Finding evidence-reference integrity: 100.00%

Interpretation: requested papers were preserved through comparison profiles and matrices, and populated cells retained valid evidence references. Empty matrix cells are allowed when the indexed evidence does not support a comparison dimension.

Matrix population is a coverage measure, not a comparison-accuracy score.

## 6. Research-Gap Evaluation

- Cases: 3
- Structural pass rate: 100.00%
- Signal paper coverage: 100.00%
- Backend validation pass rate: 100.00%
- Candidate evidence-reference integrity: 100.00%
- Mean dimension population rate: 94.44%
- Total candidates: 14
- Explicit candidates: 14
- Corpus-imbalance candidates: 0
- Insufficient-evidence candidates: 0

Interpretation: the evaluated cases produced evidence-backed explicit gap candidates without requiring every gap taxonomy category to appear.

The system intentionally distinguishes missing evidence in the indexed corpus from evidence that a topic is globally absent from the research literature.

## 7. Literature-Review Evaluation

- Cases: 3
- Structural pass rate: 100.00%
- Backend validation pass rate: 100.00%
- Review paper coverage: 100.00%
- Section structure pass rate: 100.00%
- Finding-evidence coverage: 100.00%
- Finding evidence-reference integrity: 100.00%
- Provenance completeness: 100.00%
- Corpus-scope note pass rate: 100.00%
- Total findings: 17
- Total evidence placements: 212
- Total citations: 159

Interpretation: literature reviews preserved the expected eight-section structure, evidence-backed findings, citations, provenance, and indexed-corpus scope statement.

## 8. End-to-End Evaluation

- Cases: 3
- Structural pass rate: 100.00%
- Mean stage success rate: 100.00%
- Answer success rate: 100.00%
- Comparison success rate: 100.00%
- Gap-analysis success rate: 100.00%
- Literature-review success rate: 100.00%
- Comparison paper coverage: 100.00%
- Gap paper coverage: 100.00%
- Literature-review paper coverage: 100.00%
- Total answer claims: 15
- Total comparison findings: 16
- Total gap candidates: 16
- Total review findings: 17
- Total review citations: 160
- Shared evidence IDs: 160

Interpretation: all benchmark workflows completed grounded answering, comparative analysis, gap analysis, and literature review generation while preserving stage-level validation and requested-paper scope where applicable.

End-to-end structural success should not be interpreted as 100% semantic accuracy.

## 9. Regression Status

The final Phase 13.6 regression baseline contained 372 passing automated tests.

```text
372 passed
```

## 10. Known Limitations

1. The evaluation corpus contains only the currently indexed research papers and is not an exhaustive representation of software-testing literature.
2. Retrieval ranking remains the clearest measured weakness. Relevant papers are often discovered within the top-10 results but are not consistently ranked in the first few positions.
3. Structural grounding verifies that claims reference existing evidence and retain provenance; it does not fully measure semantic entailment.
4. The comparison evaluation measures paper coverage, matrix population, and evidence-reference integrity rather than human-rated comparative correctness.
5. Research-gap findings apply to the indexed corpus. Missing evidence is not treated as proof of a universal literature gap.
6. Literature-review evaluation measures structure, evidence coverage, provenance, and citations rather than expert-rated writing quality.
7. The current benchmark sets are small and intended as reproducible engineering baselines rather than statistically comprehensive academic evaluations.

## 11. Overall Conclusion

The Research Intelligence Agent demonstrates an evidence-grounded research workflow spanning semantic retrieval, grounded question answering, comparative analysis, research-gap analysis, and literature-review generation.

The strongest measured properties are evidence traceability, provenance preservation, structural validation, requested-paper coverage, and end-to-end workflow reliability.

The primary measured improvement area is retrieval ranking. The baseline indicates stronger top-10 discovery than early-rank performance, providing a concrete target for future retriever improvements.

The evaluation therefore supports the system as a reproducible research intelligence prototype while explicitly preserving the limitations of its corpus, benchmarks, retrieval quality, and structural evaluation methodology.
