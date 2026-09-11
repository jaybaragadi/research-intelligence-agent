from src.generation.models import (
    EvidencePackage,
    GroundingEvidence,
)
from src.tools.citation_tool import (
    CitationTool,
)
from src.tools.compare_papers import (
    PaperComparisonResponse,
)
from src.tools.evidence_tool import (
    EvidenceTool,
)
from src.tools.search_papers import (
    PaperSearchResponse,
)


class EvidencePackageBuilder:
    """
    Convert retrieval results into validated
    evidence packages for answer generation.

    Retrieval results themselves are not
    trusted as final citation metadata.

    Every chunk ID is resolved again through
    EvidenceTool and CitationTool.
    """

    def __init__(
        self,
        evidence_tool: EvidenceTool | None = None,
        citation_tool: CitationTool | None = None,
    ) -> None:

        self.evidence_tool = (
            evidence_tool if evidence_tool is not None else EvidenceTool()
        )

        self.citation_tool = (
            citation_tool
            if citation_tool is not None
            else CitationTool(evidence_tool=(self.evidence_tool))
        )

    def _build_item(
        self,
        evidence_id: str,
        label: str,
    ) -> GroundingEvidence:
        """
        Resolve one evidence identifier and
        attach its validated citation.
        """

        evidence = self.evidence_tool.get(evidence_id)

        citation = self.citation_tool.cite(evidence_id)

        return GroundingEvidence(
            evidence_id=(evidence.evidence_id),
            label=label,
            paper_id=(evidence.paper_id),
            page_number=(evidence.page_number),
            section=(evidence.section),
            text=(evidence.text),
            citation_text=(citation.citation_text),
        )

    def from_search(
        self,
        response: PaperSearchResponse,
    ) -> EvidencePackage:
        """
        Build a validated evidence package
        from search results.
        """

        items: list[GroundingEvidence] = []

        seen: set[str] = set()

        for result in response.results:

            evidence_id = result.chunk_id

            if evidence_id in seen:
                continue

            seen.add(evidence_id)

            label = f"E{len(items) + 1}"

            items.append(
                self._build_item(
                    evidence_id=(evidence_id),
                    label=label,
                )
            )

        return EvidencePackage(
            query=(response.query),
            evidence=items,
        )

    def from_comparison(
        self,
        response: PaperComparisonResponse,
    ) -> EvidencePackage:
        """
        Build one validated evidence package
        from paper-grouped comparison results.

        Requested-paper order and evidence
        order are preserved.
        """

        items: list[GroundingEvidence] = []

        seen: set[str] = set()

        for comparison in response.comparisons:

            for result in comparison.evidence:

                evidence_id = result.chunk_id

                if evidence_id in seen:
                    continue

                seen.add(evidence_id)

                label = f"E{len(items) + 1}"

                items.append(
                    self._build_item(
                        evidence_id=(evidence_id),
                        label=label,
                    )
                )

        return EvidencePackage(
            query=(response.query),
            evidence=items,
        )
