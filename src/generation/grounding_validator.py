from src.generation.models import (
    EvidencePackage,
    GeneratedDraft,
    GroundingIssue,
    GroundingValidationResult,
)


class GroundingValidator:
    """
    Validate generated claims against the
    evidence package supplied to the generator.

    Phase 8 validates provenance relationships.

    Full semantic claim-entailment evaluation
    will be introduced later during evaluation.
    """

    def validate(
        self,
        draft: GeneratedDraft,
        package: EvidencePackage,
    ) -> GroundingValidationResult:

        issues: list[GroundingIssue] = []

        available_ids = {evidence.evidence_id for evidence in package.evidence}

        seen_claim_ids: set[str] = set()

        validated_claim_count = 0

        for claim in draft.claims:

            if claim.claim_id in (seen_claim_ids):

                issues.append(
                    GroundingIssue(
                        issue_type=("duplicate_claim_id"),
                        message=("Claim ID is duplicated."),
                        claim_id=(claim.claim_id),
                    )
                )

            seen_claim_ids.add(claim.claim_id)

            if not claim.text.strip():

                issues.append(
                    GroundingIssue(
                        issue_type=("empty_claim"),
                        message=("Claim text is empty."),
                        claim_id=(claim.claim_id),
                    )
                )

            if not claim.evidence_ids:

                issues.append(
                    GroundingIssue(
                        issue_type=("missing_evidence"),
                        message=("Claim has no supporting " "evidence IDs."),
                        claim_id=(claim.claim_id),
                    )
                )

                continue

            claim_valid = True

            for evidence_id in claim.evidence_ids:

                if evidence_id not in (available_ids):

                    claim_valid = False

                    issues.append(
                        GroundingIssue(
                            issue_type=("unknown_evidence"),
                            message=(
                                "Claim references "
                                "evidence that was not "
                                "present in the validated "
                                "evidence package."
                            ),
                            claim_id=(claim.claim_id),
                            evidence_id=(evidence_id),
                        )
                    )

            if claim_valid and claim.text.strip() and claim.evidence_ids:

                validated_claim_count += 1

        return GroundingValidationResult(
            is_valid=(len(issues) == 0),
            validated_claim_count=(validated_claim_count),
            issue_count=(len(issues)),
            issues=issues,
        )
