from src.analysis.literature_review_models import (
    LiteratureReview,
    LiteratureReviewEvidence,
    LiteratureReviewSection,
    LiteratureReviewSectionType,
    LiteratureReviewValidationResult,
)

from src.analysis.literature_review_renderer import (
    LiteratureReviewMarkdownRenderer,
)


def build_review():

    evidence = (
        LiteratureReviewEvidence(
            evidence_id="E1",
            paper_id="03_mutap",
            page_number=5,
            section="methodology",
            text=(
                "Mutation feedback guides "
                "test generation."
            ),
            citation_text=(
                "MuTAP (2023), p. 5"
            ),
        )
    )

    section = (
        LiteratureReviewSection(
            section_type=(
                LiteratureReviewSectionType
                .GENERATION_STRATEGIES
            ),
            title=(
                "Test Generation Strategies"
            ),
            objective=(
                "Summarize generation strategies."
            ),
            findings=[],
            evidence=[
                evidence
            ],
            narrative=(
                "The indexed study uses "
                "structured test generation. [E1]"
            ),
        )
    )

    return LiteratureReview(
        query=(
            "How are LLMs used for "
            "test generation?"
        ),
        paper_ids=[
            "03_mutap"
        ],
        title=(
            "LLMs for Software Testing"
        ),
        sections=[
            section
        ],
        citations=[
            "MuTAP (2023), p. 5"
        ],
        validation=(
            LiteratureReviewValidationResult(
                valid=True,
                issues=[],
            )
        ),
    )


def test_renderer_contains_title():

    markdown = (
        LiteratureReviewMarkdownRenderer()
        .render(
            build_review()
        )
    )

    assert (
        "# LLMs for Software Testing"
        in markdown
    )


def test_renderer_contains_query():

    markdown = (
        LiteratureReviewMarkdownRenderer()
        .render(
            build_review()
        )
    )

    assert (
        "How are LLMs used for "
        "test generation?"
        in markdown
    )


def test_renderer_contains_section():

    markdown = (
        LiteratureReviewMarkdownRenderer()
        .render(
            build_review()
        )
    )

    assert (
        "## Test Generation Strategies"
        in markdown
    )


def test_renderer_contains_evidence_marker():

    markdown = (
        LiteratureReviewMarkdownRenderer()
        .render(
            build_review()
        )
    )

    assert (
        "[E1]"
        in markdown
    )


def test_renderer_contains_paper_id():

    markdown = (
        LiteratureReviewMarkdownRenderer()
        .render(
            build_review()
        )
    )

    assert (
        "`03_mutap`"
        in markdown
    )


def test_renderer_contains_page_and_section():

    markdown = (
        LiteratureReviewMarkdownRenderer()
        .render(
            build_review()
        )
    )

    assert (
        "p. 5, methodology"
        in markdown
    )


def test_renderer_contains_citation_index():

    markdown = (
        LiteratureReviewMarkdownRenderer()
        .render(
            build_review()
        )
    )

    assert (
        "## Citation Index"
        in markdown
    )

    assert (
        "MuTAP (2023), p. 5"
        in markdown
    )


def test_renderer_contains_scope_note():

    markdown = (
        LiteratureReviewMarkdownRenderer()
        .render(
            build_review()
        )
    )

    assert (
        "indexed corpus only"
        in markdown
    )


def test_renderer_contains_validation():

    markdown = (
        LiteratureReviewMarkdownRenderer()
        .render(
            build_review()
        )
    )

    assert (
        "## Grounding Validation"
        in markdown
    )

    assert (
        "**Valid:** True"
        in markdown
    )


def test_renderer_collapses_evidence_whitespace():

    evidence = LiteratureReviewEvidence(
        evidence_id="E1",
        paper_id="03_mutap",
        page_number=5,
        section="methodology",
        text=(
            "Mutation   feedback\n"
            "guides     test generation."
        ),
        citation_text=(
            "MuTAP (2023), p. 5"
        ),
    )

    section = LiteratureReviewSection(
        section_type=(
            LiteratureReviewSectionType
            .GENERATION_STRATEGIES
        ),
        title=(
            "Test Generation Strategies"
        ),
        objective=(
            "Summarize generation strategies."
        ),
        findings=[],
        evidence=[
            evidence
        ],
        narrative=(
            "The indexed study uses "
            "structured test generation. [E1]"
        ),
    )

    review = LiteratureReview(
        query=(
            "How are LLMs used for "
            "test generation?"
        ),
        paper_ids=[
            "03_mutap"
        ],
        title=(
            "LLMs for Software Testing"
        ),
        sections=[
            section
        ],
        citations=[
            "MuTAP (2023), p. 5"
        ],
        validation=(
            LiteratureReviewValidationResult(
                valid=True,
                issues=[],
            )
        ),
    )

    markdown = (
        LiteratureReviewMarkdownRenderer()
        .render(
            review
        )
    )

    assert (
        "Mutation feedback guides "
        "test generation."
        in markdown
    )