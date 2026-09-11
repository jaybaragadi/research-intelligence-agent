from src.generation.deterministic_generator import (
    DeterministicGroundedGenerator,
)
from src.generation.evidence_package import (
    EvidencePackageBuilder,
)
from src.generation.generator import (
    AnswerGenerator,
)
from src.generation.grounding_validator import (
    GroundingValidator,
)
from src.generation.models import (
    GroundedAnswer,
)
from src.generation.query_focus import (
    build_comparison_focus_query,
)
from src.tools.compare_papers import (
    ComparePapersTool,
)
from src.tools.search_papers import (
    SearchPapersTool,
)


class GroundedAnswerService:
    """
    High-level Phase 8 service for producing
    evidence-grounded answers.

    Retrieval remains deterministic.

    Generation is provider-independent.

    Validation occurs before a grounded answer
    is returned.
    """

    def __init__(
        self,
        search_tool: SearchPapersTool | None = None,
        compare_tool: ComparePapersTool | None = None,
        package_builder: EvidencePackageBuilder | None = None,
        generator: AnswerGenerator | None = None,
        validator: GroundingValidator | None = None,
    ) -> None:

        self.search_tool = (
            search_tool if search_tool is not None else SearchPapersTool()
        )

        self.compare_tool = (
            compare_tool if compare_tool is not None else ComparePapersTool()
        )

        self.package_builder = (
            package_builder if package_builder is not None else EvidencePackageBuilder()
        )

        self.generator = (
            generator if generator is not None else DeterministicGroundedGenerator()
        )

        self.validator = validator if validator is not None else GroundingValidator()

    def _finalize(
        self,
        package,
    ) -> GroundedAnswer:
        """
        Generate and validate one answer.
        """

        draft = self.generator.generate(package)

        validation = self.validator.validate(
            draft=draft,
            package=package,
        )

        return GroundedAnswer(
            query=(package.query),
            answer_text=(draft.answer_text),
            claims=(draft.claims),
            evidence=(package.evidence),
            validation=(validation),
        )

    def answer_search(
        self,
        query: str,
        top_k: int = 5,
    ) -> GroundedAnswer:
        """
        Answer a general research question from
        retrieved validated evidence.
        """

        response = self.search_tool.search(
            query=query,
            top_k=top_k,
        )

        package = self.package_builder.from_search(response)

        return self._finalize(package)

    def answer_comparison(
        self,
        paper_ids: list[str],
        query: str,
        evidence_per_paper: int = 3,
    ) -> GroundedAnswer:
        """
        Answer a comparison question using
        independently retrieved evidence for
        every requested paper.

        The user-facing query is preserved, while
        retrieval uses a focused version with
        comparison commands and paper names removed.
        """

        retrieval_query = build_comparison_focus_query(
            query=query,
            paper_ids=paper_ids,
        )

        response = self.compare_tool.compare(
            paper_ids=paper_ids,
            query=retrieval_query,
            evidence_per_paper=(evidence_per_paper),
        )

        package = self.package_builder.from_comparison(response)

        # Restore the original user question.
        # The focused query is only an internal
        # retrieval optimization.
        package.query = query

        return self._finalize(package)
