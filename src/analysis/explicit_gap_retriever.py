from src.generation.evidence_package import (
    EvidencePackageBuilder,
)

from src.generation.models import (
    GroundingEvidence,
)

from src.tools.search_papers import (
    SearchPapersTool,
)


EXPLICIT_GAP_QUERIES = (
    (
        "limitations threats to validity "
        "weaknesses constraints drawbacks"
    ),
    (
        "future work future research "
        "future directions further investigation"
    ),
    (
        "open problem unresolved challenge "
        "underexplored not addressed "
        "not investigated"
    ),
)


class ExplicitGapEvidenceRetriever:
    """
    Retrieve evidence specifically for explicit
    research-gap signals.

    Retrieval is performed independently inside
    every requested paper.

    This prevents globally high-ranking papers
    from crowding out limitation, future-work,
    or unresolved-problem evidence from another
    paper.

    Returned evidence is validated again through
    EvidencePackageBuilder before downstream
    signal extraction.
    """

    def __init__(
        self,
        search_tool: SearchPapersTool | None = None,
        package_builder: (
            EvidencePackageBuilder | None
        ) = None,
    ) -> None:

        self.search_tool = (
            search_tool
            if search_tool is not None
            else SearchPapersTool()
        )

        self.package_builder = (
            package_builder
            if package_builder is not None
            else EvidencePackageBuilder()
        )

    def retrieve(
        self,
        paper_ids: list[str],
        evidence_per_query: int = 4,
    ) -> list[GroundingEvidence]:
        """
        Retrieve gap-focused evidence from every
        requested paper.

        Three focused searches are performed:

        1. limitations / threats;
        2. future work;
        3. unresolved / underexplored problems.

        Evidence is deduplicated by evidence ID
        because one chunk can rank for several
        focus queries.
        """

        if evidence_per_query <= 0:

            raise ValueError(
                "evidence_per_query must be positive"
            )

        cleaned_papers = (
            self._clean_paper_ids(
                paper_ids
            )
        )

        if not cleaned_papers:
            return []

        collected: list[
            GroundingEvidence
        ] = []

        seen_evidence_ids: set[str] = set()

        for paper_id in cleaned_papers:

            for query in (
                EXPLICIT_GAP_QUERIES
            ):

                response = (
                    self.search_tool.search(
                        query=query,

                        top_k=(
                            evidence_per_query
                        ),

                        allowed_paper_ids={
                            paper_id
                        },

                        max_per_paper=(
                            evidence_per_query
                        ),
                    )
                )

                package = (
                    self.package_builder
                    .from_search(
                        response
                    )
                )

                for evidence in (
                    package.evidence
                ):

                    if (
                        evidence.evidence_id
                        in seen_evidence_ids
                    ):
                        continue

                    seen_evidence_ids.add(
                        evidence.evidence_id
                    )

                    collected.append(
                        GroundingEvidence(
                            evidence_id=(
                                evidence.evidence_id
                            ),

                            label=(
                                f"E{len(collected) + 1}"
                            ),

                            paper_id=(
                                evidence.paper_id
                            ),

                            page_number=(
                                evidence.page_number
                            ),

                            section=(
                                evidence.section
                            ),

                            text=(
                                evidence.text
                            ),

                            citation_text=(
                                evidence.citation_text
                            ),
                        )
                    )

        return collected

    def _clean_paper_ids(
        self,
        paper_ids: list[str],
    ) -> list[str]:
        """
        Remove blank and duplicate paper IDs
        while preserving requested order.
        """

        seen: set[str] = set()

        cleaned: list[str] = []

        for paper_id in paper_ids:

            value = paper_id.strip()

            if (
                not value
                or value in seen
            ):
                continue

            seen.add(
                value
            )

            cleaned.append(
                value
            )

        return cleaned