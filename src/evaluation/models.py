from dataclasses import dataclass


@dataclass
class RetrievalBenchmarkCase:
    question_id: str
    query: str
    expected_papers: list[str]
    description: str = ""


@dataclass
class RetrievalEvaluationResult:
    question_id: str
    query: str
    expected_papers: list[str]

    retrieved_papers: list[str]
    unique_retrieved_papers: list[str]

    hit_at_1: bool
    hit_at_3: bool
    hit_at_5: bool

    reciprocal_rank: float

    recall_at_3: float
    recall_at_5: float
    recall_at_10: float

    matched_papers: list[str]
    missing_expected_papers: list[str]


@dataclass
class GroundingBenchmarkCase:
    question_id: str
    query: str
    expected_papers: list[str]


@dataclass
class GroundingEvaluationResult:
    question_id: str
    query: str

    claim_count: int
    evidence_count: int

    claims_with_evidence: int
    claims_without_evidence: int

    referenced_evidence_count: int
    missing_evidence_references: list[str]

    evidence_with_complete_provenance: int
    evidence_with_incomplete_provenance: int

    backend_validation_valid: bool
    backend_validation_issue_count: int

    evidence_papers: list[str]
    expected_papers: list[str]
    matched_expected_papers: list[str]

    claim_evidence_coverage: float
    provenance_completeness: float
    expected_paper_recall: float


@dataclass
class ComparisonBenchmarkCase:
    comparison_id: str
    query: str
    paper_ids: list[str]
    description: str = ""


@dataclass
class ComparisonEvaluationResult:
    comparison_id: str
    query: str

    requested_papers: list[str]
    profile_papers: list[str]
    matrix_papers: list[str]

    missing_profile_papers: list[str]
    missing_matrix_papers: list[str]

    profile_paper_coverage: float
    matrix_paper_coverage: float

    dimension_count: int
    matrix_cell_count: int
    populated_cell_count: int
    empty_cell_count: int
    matrix_population_rate: float

    profile_evidence_count: int
    profile_evidence_ids: list[str]

    populated_cell_evidence_reference_count: int
    missing_cell_evidence_references: list[str]
    cell_evidence_reference_integrity: float

    finding_count: int
    finding_evidence_reference_count: int
    missing_finding_evidence_references: list[str]
    finding_evidence_reference_integrity: float

    invalid_finding_paper_references: list[str]

    structural_valid: bool


@dataclass
class GapBenchmarkCase:
    gap_id: str
    query: str
    paper_ids: list[str]
    description: str = ""


@dataclass
class GapEvaluationResult:
    gap_id: str
    query: str

    requested_papers: list[str]
    signal_papers: list[str]
    missing_signal_papers: list[str]
    signal_paper_coverage: float

    signal_count: int
    candidate_count: int

    explicit_candidate_count: int
    corpus_imbalance_candidate_count: int
    insufficient_evidence_candidate_count: int

    candidate_evidence_reference_count: int
    missing_candidate_evidence_references: list[str]
    candidate_evidence_reference_integrity: float

    invalid_candidate_paper_references: list[str]

    dimension_coverage_count: int
    populated_dimension_count: int
    dimension_population_rate: float

    backend_validation_valid: bool
    backend_validation_issue_count: int

    structural_valid: bool


@dataclass
class LiteratureReviewBenchmarkCase:
    review_id: str
    title: str
    query: str
    paper_ids: list[str]
    description: str = ""


@dataclass
class LiteratureReviewEvaluationResult:
    review_id: str
    title: str
    query: str

    requested_papers: list[str]
    review_papers: list[str]
    missing_review_papers: list[str]
    invalid_review_papers: list[str]
    review_paper_coverage: float

    section_count: int
    expected_section_count: int
    section_structure_complete: bool
    missing_section_types: list[str]
    duplicate_section_types: list[str]

    finding_count: int
    findings_with_evidence: int
    findings_without_evidence: int
    finding_evidence_coverage: float

    evidence_count: int
    unique_evidence_count: int

    finding_evidence_reference_count: int
    missing_finding_evidence_references: list[str]
    finding_evidence_reference_integrity: float

    invalid_finding_paper_references: list[str]

    evidence_with_complete_provenance: int
    evidence_with_incomplete_provenance: int
    provenance_completeness: float

    citation_count: int

    backend_validation_valid: bool
    backend_validation_issue_count: int

    corpus_scope_note_present: bool

    structural_valid: bool


@dataclass
class EndToEndBenchmarkCase:
    workflow_id: str
    query: str
    paper_ids: list[str]
    title: str
    description: str = ""


@dataclass
class EndToEndEvaluationResult:
    workflow_id: str
    query: str
    requested_papers: list[str]

    answer_generated: bool
    answer_claim_count: int
    answer_evidence_count: int
    answer_validation_valid: bool

    comparison_generated: bool
    comparison_profile_count: int
    comparison_matrix_row_count: int
    comparison_finding_count: int
    comparison_paper_coverage: float

    gap_analysis_generated: bool
    gap_signal_count: int
    gap_candidate_count: int
    gap_validation_valid: bool
    gap_paper_coverage: float

    literature_review_generated: bool
    literature_review_section_count: int
    literature_review_finding_count: int
    literature_review_citation_count: int
    literature_review_validation_valid: bool
    literature_review_paper_coverage: float

    shared_evidence_id_count: int

    invalid_comparison_paper_references: list[str]
    invalid_gap_paper_references: list[str]
    invalid_review_paper_references: list[str]

    stage_success_count: int
    total_stage_count: int
    stage_success_rate: float

    structural_valid: bool
