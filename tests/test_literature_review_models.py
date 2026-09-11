from src.analysis.literature_review_models import (
    LiteratureReview,
    LiteratureReviewEvidence,
    LiteratureReviewFinding,
    LiteratureReviewPlan,
    LiteratureReviewSection,
    LiteratureReviewSectionType,
    LiteratureReviewValidationResult,
)


def test_literature_review_evidence_preserves_provenance():

    evidence = LiteratureReviewEvidence(
        evidence_id="E1",
        paper_id="03_mutap",
        page_number=13,
        section="threats_to_validity",
        text="Example evidence.",
        citation_text="MuTAP (2023), p. 13",
    )

    assert evidence.evidence_id == "E1"
    assert evidence.paper_id == "03_mutap"
    assert evidence.page_number == 13
    assert evidence.section == "threats_to_validity"


def test_literature_review_finding_links_to_evidence():

    finding = LiteratureReviewFinding(
        finding_id="F1",
        section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
        statement=(
            "Several approaches augment LLM generation "
            "with traditional testing feedback."
        ),
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
        evidence_ids=[
            "E1",
            "E2",
        ],
    )

    assert finding.finding_id == "F1"

    assert finding.paper_ids == [
        "03_mutap",
        "05_coverup",
    ]

    assert finding.evidence_ids == [
        "E1",
        "E2",
    ]


def test_literature_review_section_groups_findings():

    finding = LiteratureReviewFinding(
        finding_id="F1",
        section_type=(LiteratureReviewSectionType.QUALITY_AND_EVALUATION),
        statement=("Evaluation commonly uses structural coverage."),
    )

    section = LiteratureReviewSection(
        section_type=(LiteratureReviewSectionType.QUALITY_AND_EVALUATION),
        title="Quality and Evaluation",
        objective=("Describe how generated tests are evaluated."),
        findings=[finding],
    )

    assert len(section.findings) == 1

    assert section.findings[0].finding_id == "F1"


def test_literature_review_plan_preserves_paper_order():

    plan = LiteratureReviewPlan(
        query="Review LLM-based automated test generation.",
        paper_ids=[
            "01_testpilot",
            "03_mutap",
            "05_coverup",
        ],
    )

    assert plan.paper_ids == [
        "01_testpilot",
        "03_mutap",
        "05_coverup",
    ]


def test_literature_review_has_corpus_scope_note():

    review = LiteratureReview(
        query="Review test generation research.",
        paper_ids=[
            "01_testpilot",
            "03_mutap",
        ],
        title=("LLM-Based Automated Test Generation"),
        sections=[],
        validation=(LiteratureReviewValidationResult(valid=True)),
    )

    assert "indexed corpus" in review.corpus_scope_note

    assert "exhaustive" in review.corpus_scope_note
