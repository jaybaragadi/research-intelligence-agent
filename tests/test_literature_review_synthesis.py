from src.analysis.literature_review_models import (
    LiteratureReviewEvidence,
    LiteratureReviewEvidenceAggregation,
    LiteratureReviewEvidenceBundle,
    LiteratureReviewSectionType,
)

from src.analysis.literature_review_synthesis import (
    LiteratureReviewSynthesisBuilder,
)


def make_evidence(
    evidence_id: str,
    paper_id: str,
) -> LiteratureReviewEvidence:

    return LiteratureReviewEvidence(
        evidence_id=evidence_id,
        paper_id=paper_id,
        page_number=1,
        section="methodology",
        text="Evidence text.",
        citation_text=(
            f"{paper_id}, p. 1"
        ),
    )


def test_cross_paper_finding_created_for_two_papers():

    aggregation = (
        LiteratureReviewEvidenceAggregation(
            query="Review feedback.",
            paper_ids=[
                "03_mutap",
                "05_coverup",
            ],
            bundles=[
                LiteratureReviewEvidenceBundle(
                    section_type=(
                        LiteratureReviewSectionType
                        .FEEDBACK_AND_ITERATION
                    ),
                    evidence=[
                        make_evidence(
                            "E1",
                            "03_mutap",
                        ),
                        make_evidence(
                            "E2",
                            "05_coverup",
                        ),
                    ],
                )
            ],
        )
    )

    synthesis = (
        LiteratureReviewSynthesisBuilder()
        .build(
            aggregation
        )
    )

    assert len(
        synthesis.findings
    ) == 1

    finding = synthesis.findings[0]

    assert (
        finding.is_cross_paper
        is True
    )

    assert (
        finding.support_count
        == 2
    )

    assert finding.paper_ids == [
        "03_mutap",
        "05_coverup",
    ]


def test_single_paper_finding_is_not_cross_paper():

    aggregation = (
        LiteratureReviewEvidenceAggregation(
            query="Review future work.",
            paper_ids=[
                "09_hits",
            ],
            bundles=[
                LiteratureReviewEvidenceBundle(
                    section_type=(
                        LiteratureReviewSectionType
                        .FUTURE_DIRECTIONS
                    ),
                    evidence=[
                        make_evidence(
                            "E1",
                            "09_hits",
                        )
                    ],
                )
            ],
        )
    )

    synthesis = (
        LiteratureReviewSynthesisBuilder()
        .build(
            aggregation
        )
    )

    finding = synthesis.findings[0]

    assert (
        finding.is_cross_paper
        is False
    )

    assert (
        finding.support_count
        == 1
    )


def test_finding_preserves_evidence_ids():

    aggregation = (
        LiteratureReviewEvidenceAggregation(
            query="Review strategies.",
            paper_ids=[
                "03_mutap",
                "05_coverup",
            ],
            bundles=[
                LiteratureReviewEvidenceBundle(
                    section_type=(
                        LiteratureReviewSectionType
                        .GENERATION_STRATEGIES
                    ),
                    evidence=[
                        make_evidence(
                            "E1",
                            "03_mutap",
                        ),
                        make_evidence(
                            "E2",
                            "05_coverup",
                        ),
                    ],
                )
            ],
        )
    )

    synthesis = (
        LiteratureReviewSynthesisBuilder()
        .build(
            aggregation
        )
    )

    assert (
        synthesis.findings[0]
        .evidence_ids
        == [
            "E1",
            "E2",
        ]
    )


def test_duplicate_evidence_id_for_same_paper_is_removed():

    evidence = make_evidence(
        "E1",
        "03_mutap",
    )

    aggregation = (
        LiteratureReviewEvidenceAggregation(
            query="Review strategies.",
            paper_ids=[
                "03_mutap",
            ],
            bundles=[
                LiteratureReviewEvidenceBundle(
                    section_type=(
                        LiteratureReviewSectionType
                        .GENERATION_STRATEGIES
                    ),
                    evidence=[
                        evidence,
                        evidence,
                    ],
                )
            ],
        )
    )

    synthesis = (
        LiteratureReviewSynthesisBuilder()
        .build(
            aggregation
        )
    )

    assert (
        synthesis.findings[0]
        .evidence_ids
        == [
            "E1",
        ]
    )


def test_different_evidence_from_same_paper_is_preserved():

    aggregation = (
        LiteratureReviewEvidenceAggregation(
            query="Review evaluation.",
            paper_ids=[
                "01_testpilot",
            ],
            bundles=[
                LiteratureReviewEvidenceBundle(
                    section_type=(
                        LiteratureReviewSectionType
                        .QUALITY_AND_EVALUATION
                    ),
                    evidence=[
                        make_evidence(
                            "E1",
                            "01_testpilot",
                        ),
                        make_evidence(
                            "E2",
                            "01_testpilot",
                        ),
                    ],
                )
            ],
        )
    )

    synthesis = (
        LiteratureReviewSynthesisBuilder()
        .build(
            aggregation
        )
    )

    assert (
        synthesis.findings[0]
        .evidence_ids
        == [
            "E1",
            "E2",
        ]
    )

    assert (
        synthesis.findings[0]
        .support_count
        == 1
    )


def test_findings_are_numbered_across_sections():

    aggregation = (
        LiteratureReviewEvidenceAggregation(
            query="Review research.",
            paper_ids=[
                "03_mutap",
                "05_coverup",
            ],
            bundles=[
                LiteratureReviewEvidenceBundle(
                    section_type=(
                        LiteratureReviewSectionType
                        .GENERATION_STRATEGIES
                    ),
                    evidence=[
                        make_evidence(
                            "E1",
                            "03_mutap",
                        )
                    ],
                ),
                LiteratureReviewEvidenceBundle(
                    section_type=(
                        LiteratureReviewSectionType
                        .FUTURE_DIRECTIONS
                    ),
                    evidence=[
                        make_evidence(
                            "E2",
                            "05_coverup",
                        )
                    ],
                ),
            ],
        )
    )

    synthesis = (
        LiteratureReviewSynthesisBuilder()
        .build(
            aggregation
        )
    )

    assert [
        finding.finding_id
        for finding
        in synthesis.findings
    ] == [
        "SF1",
        "SF2",
    ]


def test_feedback_section_uses_conservative_statement():

    aggregation = (
        LiteratureReviewEvidenceAggregation(
            query="Review feedback.",
            paper_ids=[
                "03_mutap",
                "05_coverup",
            ],
            bundles=[
                LiteratureReviewEvidenceBundle(
                    section_type=(
                        LiteratureReviewSectionType
                        .FEEDBACK_AND_ITERATION
                    ),
                    evidence=[
                        make_evidence(
                            "E1",
                            "03_mutap",
                        ),
                        make_evidence(
                            "E2",
                            "05_coverup",
                        ),
                    ],
                )
            ],
        )
    )

    synthesis = (
        LiteratureReviewSynthesisBuilder()
        .build(
            aggregation
        )
    )

    statement = (
        synthesis.findings[0]
        .statement
        .lower()
    )

    assert "multiple indexed studies" in statement

    assert (
        "feedback"
        in statement
        or "iterative"
        in statement
    )


def test_empty_bundle_creates_no_finding():

    aggregation = (
        LiteratureReviewEvidenceAggregation(
            query="Review research.",
            paper_ids=[
                "03_mutap",
            ],
            bundles=[
                LiteratureReviewEvidenceBundle(
                    section_type=(
                        LiteratureReviewSectionType
                        .GENERATION_STRATEGIES
                    ),
                    evidence=[],
                )
            ],
        )
    )

    synthesis = (
        LiteratureReviewSynthesisBuilder()
        .build(
            aggregation
        )
    )

    assert (
        synthesis.findings
        == []
    )


def test_build_preserves_query_and_paper_ids():

    aggregation = (
        LiteratureReviewEvidenceAggregation(
            query="Review LLM test generation.",
            paper_ids=[
                "01_testpilot",
                "03_mutap",
            ],
            bundles=[],
        )
    )

    synthesis = (
        LiteratureReviewSynthesisBuilder()
        .build(
            aggregation
        )
    )

    assert (
        synthesis.query
        == "Review LLM test generation."
    )

    assert synthesis.paper_ids == [
        "01_testpilot",
        "03_mutap",
    ]


def test_cross_paper_support_count_is_unique_paper_count():

    aggregation = (
        LiteratureReviewEvidenceAggregation(
            query="Review quality.",
            paper_ids=[
                "01_testpilot",
                "05_coverup",
            ],
            bundles=[
                LiteratureReviewEvidenceBundle(
                    section_type=(
                        LiteratureReviewSectionType
                        .QUALITY_AND_EVALUATION
                    ),
                    evidence=[
                        make_evidence(
                            "E1",
                            "01_testpilot",
                        ),
                        make_evidence(
                            "E2",
                            "01_testpilot",
                        ),
                        make_evidence(
                            "E3",
                            "05_coverup",
                        ),
                    ],
                )
            ],
        )
    )

    synthesis = (
        LiteratureReviewSynthesisBuilder()
        .build(
            aggregation
        )
    )

    assert (
        synthesis.findings[0]
        .support_count
        == 2
    )