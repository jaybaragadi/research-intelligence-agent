import pytest

from src.analysis.literature_review_renderer import (
    LiteratureReviewMarkdownRenderer,
)

from src.analysis.literature_review_service import (
    LiteratureReviewService,
)


TEST_QUERY = (
    "How do LLM-based approaches improve "
    "automated software test generation?"
)

TEST_PAPERS = [
    "03_mutap",
    "05_coverup",
]


@pytest.fixture(scope="module")
def real_review():

    service = LiteratureReviewService()

    return service.generate(
        query=TEST_QUERY,
        paper_ids=TEST_PAPERS,
        title="Integration Test Review",
        evidence_per_paper=6,
    )


def test_real_pipeline_generates_review(
    real_review,
):

    assert real_review is not None

    assert real_review.query == TEST_QUERY

    assert (
        real_review.paper_ids
        == TEST_PAPERS
    )


def test_real_pipeline_grounding_is_valid(
    real_review,
):

    assert (
        real_review.validation
        is not None
    )

    assert (
        real_review.validation.valid
        is True
    )

    assert (
        real_review.validation.issues
        == []
    )


def test_real_pipeline_generates_all_review_sections(
    real_review,
):

    assert (
        len(real_review.sections)
        == 8
    )


def test_real_pipeline_contains_supported_findings(
    real_review,
):

    findings = [
        finding
        for section in real_review.sections
        for finding in section.findings
    ]

    assert findings

    assert any(
        finding.evidence_ids
        for finding in findings
    )


def test_real_pipeline_evidence_has_provenance(
    real_review,
):

    evidence_items = [
        evidence
        for section in real_review.sections
        for evidence in section.evidence
    ]

    assert evidence_items

    for evidence in evidence_items:

        assert evidence.evidence_id

        assert (
            evidence.paper_id
            in TEST_PAPERS
        )

        assert (
            evidence.page_number
            > 0
        )

        assert (
            evidence.text.strip()
        )

        assert (
            evidence.citation_text.strip()
        )


def test_real_pipeline_findings_reference_known_evidence(
    real_review,
):

    known_evidence_ids = {
        evidence.evidence_id
        for section in real_review.sections
        for evidence in section.evidence
    }

    for section in real_review.sections:

        for finding in section.findings:

            assert (
                finding.evidence_ids
            )

            for evidence_id in finding.evidence_ids:

                assert (
                    evidence_id
                    in known_evidence_ids
                )


def test_real_pipeline_citations_are_present(
    real_review,
):

    assert real_review.citations

    assert all(
        citation.strip()
        for citation
        in real_review.citations
    )


def test_real_pipeline_renders_markdown(
    real_review,
):

    markdown = (
        LiteratureReviewMarkdownRenderer()
        .render(
            real_review
        )
    )

    assert (
        "# Integration Test Review"
        in markdown
    )

    assert (
        "## Scope Note"
        in markdown
    )

    assert (
        "## Grounding Validation"
        in markdown
    )

    assert (
        "**Valid:** True"
        in markdown
    )


def test_real_pipeline_markdown_contains_evidence_markers(
    real_review,
):

    markdown = (
        LiteratureReviewMarkdownRenderer()
        .render(
            real_review
        )
    )

    evidence_ids = {
        evidence.evidence_id
        for section in real_review.sections
        for evidence in section.evidence
    }

    assert evidence_ids

    assert any(
        f"[{evidence_id}]"
        in markdown
        for evidence_id
        in evidence_ids
    )


def test_real_pipeline_scope_note_is_preserved(
    real_review,
):

    assert (
        "indexed corpus only"
        in real_review
        .corpus_scope_note
        .lower()
    )