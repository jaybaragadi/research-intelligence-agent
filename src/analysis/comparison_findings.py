from src.analysis.comparison_models import (
    ComparativeFinding,
    ComparisonRow,
)


class ComparisonFindingBuilder:
    """
    Build deterministic cross-paper observations
    from the populated comparison matrix.

    Phase 9 findings describe evidence presence
    and contrast structure.

    They do not invent domain conclusions.
    """

    def build(
        self,
        rows: list[
            ComparisonRow
        ],
    ) -> list[
        ComparativeFinding
    ]:

        findings: list[
            ComparativeFinding
        ] = []

        for row in rows:

            populated = [
                cell

                for cell in row.cells

                if cell.summary
            ]

            if len(populated) < 2:
                continue

            evidence_ids = [
                evidence_id

                for cell in populated

                for evidence_id
                in cell.evidence_ids
            ]

            paper_ids = [
                cell.paper_id
                for cell in populated
            ]

            finding_id = (
                f"F{len(findings) + 1}"
            )

            findings.append(
                ComparativeFinding(
                    finding_id=(
                        finding_id
                    ),

                    finding_type=(
                        "shared_dimension"
                    ),

                    text=(
                        "The compared papers "
                        f"contain evidence for the "
                        f"'{row.dimension}' "
                        "dimension."
                    ),

                    paper_ids=(
                        paper_ids
                    ),

                    evidence_ids=(
                        list(
                            dict.fromkeys(
                                evidence_ids
                            )
                        )
                    ),
                )
            )

        return findings