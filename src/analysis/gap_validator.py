from src.analysis.gap_models import (
    GapCandidate,
    GapType,
    GapValidationIssue,
    GapValidationResult,
)


class GapValidator:
    """
    Validate research-gap candidates before they
    are exposed as final analysis results.

    Validation is structural and provenance-oriented.

    It verifies that candidates are supported by the
    evidence available to the analysis pipeline.

    It does NOT prove that a research gap exists across
    all scientific literature.
    """

    def validate(
        self,
        candidates: list[GapCandidate],
        available_evidence_ids: set[str],
    ) -> GapValidationResult:
        """
        Validate all candidate gaps.

        Checks include:

        - unique gap IDs
        - required evidence
        - known evidence references
        - required paper references
        - valid explicit-gap structure
        - valid corpus-imbalance structure
        """

        issues: list[GapValidationIssue] = []

        seen_gap_ids: set[str] = set()

        valid_gap_count = 0

        for candidate in candidates:

            candidate_issues = self._validate_candidate(
                candidate=candidate,
                available_evidence_ids=(available_evidence_ids),
            )

            if candidate.gap_id in seen_gap_ids:

                candidate_issues.append(
                    GapValidationIssue(
                        issue_type=("duplicate_gap_id"),
                        message=("Gap ID must be unique: " f"{candidate.gap_id}"),
                        gap_id=(candidate.gap_id),
                    )
                )

            else:
                seen_gap_ids.add(candidate.gap_id)

            if not candidate_issues:
                valid_gap_count += 1

            issues.extend(candidate_issues)

        return GapValidationResult(
            is_valid=(len(issues) == 0),
            validated_gap_count=(valid_gap_count),
            issue_count=len(issues),
            issues=issues,
        )

    def _validate_candidate(
        self,
        candidate: GapCandidate,
        available_evidence_ids: set[str],
    ) -> list[GapValidationIssue]:
        """
        Validate one candidate independently.
        """

        issues: list[GapValidationIssue] = []

        if not candidate.gap_id.strip():

            issues.append(
                GapValidationIssue(
                    issue_type=("missing_gap_id"),
                    message=("Gap candidate is missing " "a gap ID."),
                )
            )

        if not candidate.title.strip():

            issues.append(
                GapValidationIssue(
                    issue_type=("missing_title"),
                    message=("Gap candidate is missing " "a title."),
                    gap_id=(candidate.gap_id),
                )
            )

        if not candidate.description.strip():

            issues.append(
                GapValidationIssue(
                    issue_type=("missing_description"),
                    message=("Gap candidate is missing " "a description."),
                    gap_id=(candidate.gap_id),
                )
            )

        if not candidate.reason.strip():

            issues.append(
                GapValidationIssue(
                    issue_type=("missing_reason"),
                    message=("Gap candidate is missing " "a reason."),
                    gap_id=(candidate.gap_id),
                )
            )

        issues.extend(
            self._validate_evidence(
                candidate=candidate,
                available_evidence_ids=(available_evidence_ids),
            )
        )

        if candidate.gap_type == GapType.EXPLICIT:

            issues.extend(self._validate_explicit(candidate))

        elif candidate.gap_type == GapType.CORPUS_IMBALANCE:

            issues.extend(self._validate_imbalance(candidate))

        elif candidate.gap_type == GapType.INSUFFICIENT_EVIDENCE:

            issues.extend(self._validate_insufficient_evidence(candidate))

        return issues

    def _validate_evidence(
        self,
        candidate: GapCandidate,
        available_evidence_ids: set[str],
    ) -> list[GapValidationIssue]:
        """
        Ensure evidence references exist and are
        not duplicated within the candidate.
        """

        issues: list[GapValidationIssue] = []

        seen: set[str] = set()

        for evidence_id in candidate.evidence_ids:

            if evidence_id in seen:

                issues.append(
                    GapValidationIssue(
                        issue_type=("duplicate_evidence_id"),
                        message=(
                            "Candidate contains duplicate "
                            "evidence reference: "
                            f"{evidence_id}"
                        ),
                        gap_id=(candidate.gap_id),
                        evidence_id=(evidence_id),
                    )
                )

                continue

            seen.add(evidence_id)

            if evidence_id not in available_evidence_ids:

                issues.append(
                    GapValidationIssue(
                        issue_type=("unknown_evidence_id"),
                        message=(
                            "Candidate references evidence "
                            "that is not available to the "
                            "analysis: "
                            f"{evidence_id}"
                        ),
                        gap_id=(candidate.gap_id),
                        evidence_id=(evidence_id),
                    )
                )

        return issues

    def _validate_explicit(
        self,
        candidate: GapCandidate,
    ) -> list[GapValidationIssue]:
        """
        Explicit candidates must contain direct
        supporting evidence and identify a paper.
        """

        issues: list[GapValidationIssue] = []

        if not candidate.evidence_ids:

            issues.append(
                GapValidationIssue(
                    issue_type=("explicit_gap_without_evidence"),
                    message=(
                        "Explicit gap candidates require "
                        "at least one evidence reference."
                    ),
                    gap_id=(candidate.gap_id),
                )
            )

        if not candidate.paper_ids:

            issues.append(
                GapValidationIssue(
                    issue_type=("explicit_gap_without_paper"),
                    message=(
                        "Explicit gap candidates require " "at least one source paper."
                    ),
                    gap_id=(candidate.gap_id),
                )
            )

        return issues

    def _validate_imbalance(
        self,
        candidate: GapCandidate,
    ) -> list[GapValidationIssue]:
        """
        Corpus-imbalance candidates require evidence
        from two distinct analytical dimensions.

        This prevents a single missing or sparse
        dimension from being declared a gap by itself.
        """

        issues: list[GapValidationIssue] = []

        unique_dimensions = list(dict.fromkeys(candidate.dimensions))

        if len(unique_dimensions) < 2:

            issues.append(
                GapValidationIssue(
                    issue_type=("imbalance_requires_two_dimensions"),
                    message=(
                        "Corpus-imbalance candidates "
                        "require at least two distinct "
                        "dimensions."
                    ),
                    gap_id=(candidate.gap_id),
                )
            )

        if not candidate.evidence_ids:

            issues.append(
                GapValidationIssue(
                    issue_type=("imbalance_without_evidence"),
                    message=(
                        "Corpus-imbalance candidates " "require supporting evidence."
                    ),
                    gap_id=(candidate.gap_id),
                )
            )

        if not candidate.paper_ids:

            issues.append(
                GapValidationIssue(
                    issue_type=("imbalance_without_papers"),
                    message=(
                        "Corpus-imbalance candidates " "require supporting papers."
                    ),
                    gap_id=(candidate.gap_id),
                )
            )

        return issues

    def _validate_insufficient_evidence(
        self,
        candidate: GapCandidate,
    ) -> list[GapValidationIssue]:
        """
        INSUFFICIENT_EVIDENCE is intentionally
        different from a supported research gap.

        Such candidates should not pretend to have
        positive evidence proving a gap.
        """

        issues: list[GapValidationIssue] = []

        if candidate.evidence_ids:

            issues.append(
                GapValidationIssue(
                    issue_type=("insufficient_evidence_has_support"),
                    message=(
                        "An insufficient-evidence result "
                        "must not contain evidence IDs "
                        "presented as positive support "
                        "for a research gap."
                    ),
                    gap_id=(candidate.gap_id),
                )
            )

        return issues
