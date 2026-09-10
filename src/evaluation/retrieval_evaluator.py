from src.evaluation.models import (
    RetrievalBenchmarkCase,
    RetrievalEvaluationResult,
)

from src.tools.search_papers import (
    SearchPapersTool,
)


class RetrievalEvaluator:

    def __init__(
        self,
        search_tool: SearchPapersTool | None = None,
    ) -> None:

        self.search_tool = (
            search_tool
            if search_tool is not None
            else SearchPapersTool()
        )

    def evaluate_case(
        self,
        case: RetrievalBenchmarkCase,
        top_k: int = 10,
    ) -> RetrievalEvaluationResult:

        response = self.search_tool.search(
            query=case.query,
            top_k=top_k,
        )

        retrieved_papers = [
            result.paper_id
            for result in response.results
        ]

        unique_retrieved_papers = (
            self._unique_in_order(
                retrieved_papers
            )
        )

        expected = set(
            case.expected_papers
        )

        matched = [
            paper_id
            for paper_id
            in unique_retrieved_papers
            if paper_id in expected
        ]

        missing = [
            paper_id
            for paper_id
            in case.expected_papers
            if paper_id not in matched
        ]

        reciprocal_rank = (
            self._reciprocal_rank(
                retrieved_papers,
                expected,
            )
        )

        return RetrievalEvaluationResult(
            question_id=case.question_id,
            query=case.query,
            expected_papers=case.expected_papers,

            retrieved_papers=retrieved_papers,
            unique_retrieved_papers=(
                unique_retrieved_papers
            ),

            hit_at_1=self._hit_at_k(
                retrieved_papers,
                expected,
                1,
            ),

            hit_at_3=self._hit_at_k(
                retrieved_papers,
                expected,
                3,
            ),

            hit_at_5=self._hit_at_k(
                retrieved_papers,
                expected,
                5,
            ),

            reciprocal_rank=(
                reciprocal_rank
            ),

            recall_at_3=self._recall_at_k(
                retrieved_papers,
                expected,
                3,
            ),

            recall_at_5=self._recall_at_k(
                retrieved_papers,
                expected,
                5,
            ),

            recall_at_10=self._recall_at_k(
                retrieved_papers,
                expected,
                10,
            ),

            matched_papers=matched,
            missing_expected_papers=missing,
        )

    def _unique_in_order(
        self,
        paper_ids: list[str],
    ) -> list[str]:

        seen = set()
        unique = []

        for paper_id in paper_ids:

            if paper_id not in seen:

                unique.append(
                    paper_id
                )

                seen.add(
                    paper_id
                )

        return unique

    def _hit_at_k(
        self,
        retrieved_papers: list[str],
        expected_papers: set[str],
        k: int,
    ) -> bool:

        return any(
            paper_id in expected_papers
            for paper_id
            in retrieved_papers[:k]
        )

    def _reciprocal_rank(
        self,
        retrieved_papers: list[str],
        expected_papers: set[str],
    ) -> float:

        for index, paper_id in enumerate(
            retrieved_papers,
            start=1,
        ):

            if paper_id in expected_papers:

                return 1.0 / index

        return 0.0

    def _recall_at_k(
        self,
        retrieved_papers: list[str],
        expected_papers: set[str],
        k: int,
    ) -> float:

        if not expected_papers:

            return 0.0

        retrieved_at_k = set(
            retrieved_papers[:k]
        )

        matched = (
            retrieved_at_k
            & expected_papers
        )

        return (
            len(matched)
            / len(expected_papers)
        )