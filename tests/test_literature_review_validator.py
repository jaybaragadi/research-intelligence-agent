from src.analysis.literature_review_models import (
    LiteratureReviewEvidence,
    LiteratureReviewEvidenceAggregation,
    LiteratureReviewEvidenceBundle,
    LiteratureReviewSectionType,
    LiteratureReviewSynthesis,
    LiteratureReviewSynthesisFinding,
    LiteratureReviewValidationIssueCode,
)
from src.analysis.literature_review_validator import (
    LiteratureReviewGroundingValidator,
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
        citation_text=(f"{paper_id}, p. 1"),
    )


def make_aggregation(
    evidence: list[LiteratureReviewEvidence],
    paper_ids: list[str],
) -> LiteratureReviewEvidenceAggregation:

    return LiteratureReviewEvidenceAggregation(
        query="Review research.",
        paper_ids=paper_ids,
        bundles=[
            LiteratureReviewEvidenceBundle(
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                evidence=evidence,
            )
        ],
    )


def issue_codes(result):

    return {issue.code for issue in result.issues}


def test_valid_single_paper_finding_passes():

    aggregation = make_aggregation(
        evidence=[
            make_evidence(
                "E1",
                "03_mutap",
            )
        ],
        paper_ids=["03_mutap"],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[
            LiteratureReviewSynthesisFinding(
                finding_id="SF1",
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                statement=("MuTAP contributes evidence " "about test generation."),
                paper_ids=["03_mutap"],
                evidence_ids=["E1"],
                support_count=1,
                is_cross_paper=False,
            )
        ],
    )

    result = LiteratureReviewGroundingValidator().validate(
        aggregation,
        synthesis,
    )

    assert result.valid is True

    assert result.issues == []


def test_valid_cross_paper_finding_passes():

    aggregation = make_aggregation(
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
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[
            LiteratureReviewSynthesisFinding(
                finding_id="SF1",
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                statement=(
                    "Multiple indexed studies use " "structured generation strategies."
                ),
                paper_ids=[
                    "03_mutap",
                    "05_coverup",
                ],
                evidence_ids=[
                    "E1",
                    "E2",
                ],
                support_count=2,
                is_cross_paper=True,
            )
        ],
    )

    result = LiteratureReviewGroundingValidator().validate(
        aggregation,
        synthesis,
    )

    assert result.valid is True


def test_unknown_evidence_id_is_rejected():

    aggregation = make_aggregation(
        evidence=[
            make_evidence(
                "E1",
                "03_mutap",
            )
        ],
        paper_ids=["03_mutap"],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[
            LiteratureReviewSynthesisFinding(
                finding_id="SF1",
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                statement="Finding.",
                paper_ids=["03_mutap"],
                evidence_ids=["E999"],
                support_count=1,
                is_cross_paper=False,
            )
        ],
    )

    result = LiteratureReviewGroundingValidator().validate(
        aggregation,
        synthesis,
    )

    assert result.valid is False

    assert LiteratureReviewValidationIssueCode.UNKNOWN_EVIDENCE_ID in issue_codes(
        result
    )


def test_paper_support_mismatch_is_rejected():

    aggregation = make_aggregation(
        evidence=[
            make_evidence(
                "E1",
                "03_mutap",
            )
        ],
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[
            LiteratureReviewSynthesisFinding(
                finding_id="SF1",
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                statement="Finding.",
                paper_ids=["05_coverup"],
                evidence_ids=["E1"],
                support_count=1,
                is_cross_paper=False,
            )
        ],
    )

    result = LiteratureReviewGroundingValidator().validate(
        aggregation,
        synthesis,
    )

    assert LiteratureReviewValidationIssueCode.PAPER_SUPPORT_MISMATCH in issue_codes(
        result
    )


def test_support_count_mismatch_is_rejected():

    aggregation = make_aggregation(
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
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[
            LiteratureReviewSynthesisFinding(
                finding_id="SF1",
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                statement="Finding.",
                paper_ids=[
                    "03_mutap",
                    "05_coverup",
                ],
                evidence_ids=[
                    "E1",
                    "E2",
                ],
                support_count=1,
                is_cross_paper=True,
            )
        ],
    )

    result = LiteratureReviewGroundingValidator().validate(
        aggregation,
        synthesis,
    )

    assert LiteratureReviewValidationIssueCode.SUPPORT_COUNT_MISMATCH in issue_codes(
        result
    )


def test_cross_paper_requires_two_unique_papers():

    aggregation = make_aggregation(
        evidence=[
            make_evidence(
                "E1",
                "03_mutap",
            ),
            make_evidence(
                "E2",
                "03_mutap",
            ),
        ],
        paper_ids=["03_mutap"],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[
            LiteratureReviewSynthesisFinding(
                finding_id="SF1",
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                statement="Finding.",
                paper_ids=["03_mutap"],
                evidence_ids=[
                    "E1",
                    "E2",
                ],
                support_count=1,
                is_cross_paper=True,
            )
        ],
    )

    result = LiteratureReviewGroundingValidator().validate(
        aggregation,
        synthesis,
    )

    assert (
        LiteratureReviewValidationIssueCode.CROSS_PAPER_SUPPORT_TOO_LOW
        in issue_codes(result)
    )


def test_single_paper_flag_rejects_multiple_supporting_papers():

    aggregation = make_aggregation(
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
        paper_ids=[
            "03_mutap",
            "05_coverup",
        ],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[
            LiteratureReviewSynthesisFinding(
                finding_id="SF1",
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                statement="Finding.",
                paper_ids=[
                    "03_mutap",
                    "05_coverup",
                ],
                evidence_ids=[
                    "E1",
                    "E2",
                ],
                support_count=2,
                is_cross_paper=False,
            )
        ],
    )

    result = LiteratureReviewGroundingValidator().validate(
        aggregation,
        synthesis,
    )

    assert (
        LiteratureReviewValidationIssueCode.SINGLE_PAPER_FLAG_MISMATCH
        in issue_codes(result)
    )


def test_duplicate_finding_ids_are_rejected():

    aggregation = make_aggregation(
        evidence=[
            make_evidence(
                "E1",
                "03_mutap",
            )
        ],
        paper_ids=["03_mutap"],
    )

    finding = LiteratureReviewSynthesisFinding(
        finding_id="SF1",
        section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
        statement="Finding.",
        paper_ids=["03_mutap"],
        evidence_ids=["E1"],
        support_count=1,
        is_cross_paper=False,
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[
            finding,
            finding,
        ],
    )

    result = LiteratureReviewGroundingValidator().validate(
        aggregation,
        synthesis,
    )

    assert LiteratureReviewValidationIssueCode.DUPLICATE_FINDING_ID in issue_codes(
        result
    )


def test_empty_statement_is_rejected():

    aggregation = make_aggregation(
        evidence=[
            make_evidence(
                "E1",
                "03_mutap",
            )
        ],
        paper_ids=["03_mutap"],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[
            LiteratureReviewSynthesisFinding(
                finding_id="SF1",
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                statement="   ",
                paper_ids=["03_mutap"],
                evidence_ids=["E1"],
                support_count=1,
                is_cross_paper=False,
            )
        ],
    )

    result = LiteratureReviewGroundingValidator().validate(
        aggregation,
        synthesis,
    )

    assert LiteratureReviewValidationIssueCode.EMPTY_FINDING_STATEMENT in issue_codes(
        result
    )


def test_finding_without_evidence_is_rejected():

    aggregation = make_aggregation(
        evidence=[],
        paper_ids=["03_mutap"],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[
            LiteratureReviewSynthesisFinding(
                finding_id="SF1",
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                statement="Finding.",
                paper_ids=["03_mutap"],
                evidence_ids=[],
                support_count=1,
                is_cross_paper=False,
            )
        ],
    )

    result = LiteratureReviewGroundingValidator().validate(
        aggregation,
        synthesis,
    )

    assert LiteratureReviewValidationIssueCode.FINDING_WITHOUT_EVIDENCE in issue_codes(
        result
    )


def test_duplicate_evidence_across_bundles_is_valid():

    evidence = make_evidence(
        "E1",
        "03_mutap",
    )

    aggregation = LiteratureReviewEvidenceAggregation(
        query="Review research.",
        paper_ids=["03_mutap"],
        bundles=[
            LiteratureReviewEvidenceBundle(
                section_type=(LiteratureReviewSectionType.RESEARCH_LANDSCAPE),
                evidence=[evidence],
            ),
            LiteratureReviewEvidenceBundle(
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                evidence=[evidence],
            ),
        ],
    )

    synthesis = LiteratureReviewSynthesis(
        query=aggregation.query,
        paper_ids=aggregation.paper_ids,
        findings=[
            LiteratureReviewSynthesisFinding(
                finding_id="SF1",
                section_type=(LiteratureReviewSectionType.GENERATION_STRATEGIES),
                statement="Finding.",
                paper_ids=["03_mutap"],
                evidence_ids=["E1"],
                support_count=1,
                is_cross_paper=False,
            )
        ],
    )

    result = LiteratureReviewGroundingValidator().validate(
        aggregation,
        synthesis,
    )

    assert result.valid is True
