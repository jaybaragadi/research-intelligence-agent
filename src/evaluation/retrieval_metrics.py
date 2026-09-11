from dataclasses import dataclass

from src.evaluation.models import (
    RetrievalEvaluationResult,
)


@dataclass
class RetrievalAggregateMetrics:
    case_count: int

    hit_at_1: float
    hit_at_3: float
    hit_at_5: float

    mean_reciprocal_rank: float

    mean_recall_at_3: float
    mean_recall_at_5: float
    mean_recall_at_10: float


def calculate_retrieval_metrics(
    results: list[RetrievalEvaluationResult],
) -> RetrievalAggregateMetrics:

    if not results:

        return RetrievalAggregateMetrics(
            case_count=0,
            hit_at_1=0.0,
            hit_at_3=0.0,
            hit_at_5=0.0,
            mean_reciprocal_rank=0.0,
            mean_recall_at_3=0.0,
            mean_recall_at_5=0.0,
            mean_recall_at_10=0.0,
        )

    count = len(results)

    return RetrievalAggregateMetrics(
        case_count=count,
        hit_at_1=sum(result.hit_at_1 for result in results) / count,
        hit_at_3=sum(result.hit_at_3 for result in results) / count,
        hit_at_5=sum(result.hit_at_5 for result in results) / count,
        mean_reciprocal_rank=sum(result.reciprocal_rank for result in results) / count,
        mean_recall_at_3=sum(result.recall_at_3 for result in results) / count,
        mean_recall_at_5=sum(result.recall_at_5 for result in results) / count,
        mean_recall_at_10=sum(result.recall_at_10 for result in results) / count,
    )
