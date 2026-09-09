from src.analysis.comparison_findings import (
    ComparisonFindingBuilder,
)

from src.analysis.comparison_models import (
    ComparisonCell,
    ComparisonRow,
)


def test_finding_created_for_shared_dimension():

    rows = [
        ComparisonRow(
            dimension="feedback_signal",

            cells=[
                ComparisonCell(
                    paper_id="03_mutap",
                    dimension="feedback_signal",
                    summary="Mutation feedback",
                    evidence_ids=["m1"],
                ),

                ComparisonCell(
                    paper_id="05_coverup",
                    dimension="feedback_signal",
                    summary="Coverage feedback",
                    evidence_ids=["c1"],
                ),
            ],
        )
    ]

    findings = (
        ComparisonFindingBuilder()
        .build(
            rows
        )
    )

    assert len(
        findings
    ) == 1

    assert (
        findings[0].finding_type
        == "shared_dimension"
    )


def test_no_finding_for_single_populated_paper():

    rows = [
        ComparisonRow(
            dimension="limitations",

            cells=[
                ComparisonCell(
                    paper_id="03_mutap",
                    dimension="limitations",
                    summary="Limitation",
                    evidence_ids=["m1"],
                ),

                ComparisonCell(
                    paper_id="05_coverup",
                    dimension="limitations",
                    summary=None,
                    evidence_ids=[],
                ),
            ],
        )
    ]

    findings = (
        ComparisonFindingBuilder()
        .build(
            rows
        )
    )

    assert findings == []


def test_finding_preserves_evidence_ids():

    rows = [
        ComparisonRow(
            dimension="feedback_signal",

            cells=[
                ComparisonCell(
                    paper_id="03_mutap",
                    dimension="feedback_signal",
                    summary="A",
                    evidence_ids=[
                        "m1",
                        "m2",
                    ],
                ),

                ComparisonCell(
                    paper_id="05_coverup",
                    dimension="feedback_signal",
                    summary="B",
                    evidence_ids=[
                        "c1"
                    ],
                ),
            ],
        )
    ]

    finding = (
        ComparisonFindingBuilder()
        .build(
            rows
        )[0]
    )

    assert finding.evidence_ids == [
        "m1",
        "m2",
        "c1",
    ]