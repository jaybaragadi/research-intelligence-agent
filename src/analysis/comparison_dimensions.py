from dataclasses import dataclass


@dataclass(frozen=True)
class ComparisonDimension:
    """
    Definition of one analytical comparison dimension.

    Keywords are deterministic signals used to classify
    validated evidence passages.

    These definitions describe analytical categories.
    They do not make claims about any specific paper.
    """

    name: str
    description: str
    keywords: tuple[str, ...]


COMPARISON_DIMENSIONS = (
    ComparisonDimension(
        name="generation_strategy",
        description=("How the proposed approach generates or " "constructs tests."),
        keywords=(
            "prompt",
            "prompts",
            "augmenting prompts",
            "generate tests",
            "generating tests",
            "test generation",
            "code context",
            "surviving mutants",
        ),
    ),
    ComparisonDimension(
        name="feedback_signal",
        description=(
            "Information fed back into the generation "
            "process to guide subsequent tests."
        ),
        keywords=(
            "feedback",
            "coverage feedback",
            "surviving mutants",
            "counter-example",
            "counterexample",
            "compilation feedback",
            "execution feedback",
            "augmenting prompts",
        ),
    ),
    ComparisonDimension(
        name="iteration_strategy",
        description=(
            "How generated tests are repeatedly refined "
            "using results from previous attempts."
        ),
        keywords=(
            "iterative",
            "iteratively",
            "refine",
            "refiner",
            "regenerate",
            "retry",
            "continues the dialogue",
            "continue the dialogue",
            "feedback loop",
            "subsequent",
        ),
    ),
    ComparisonDimension(
        name="quality_objective",
        description=(
            "What notion of test quality the approach " "attempts to improve."
        ),
        keywords=(
            "coverage",
            "branch coverage",
            "line coverage",
            "mutation score",
            "bug detection",
            "fault detection",
            "revealing bugs",
            "detect bugs",
            "effectiveness",
            "quality",
        ),
    ),
    ComparisonDimension(
        name="evaluation_method",
        description=("How the paper evaluates the proposed " "test-generation method."),
        keywords=(
            "evaluate",
            "evaluation",
            "experiment",
            "benchmark",
            "benchmarks",
            "dataset",
            "study",
            "research question",
            "baseline",
        ),
    ),
    ComparisonDimension(
        name="limitations",
        description=(
            "Reported weaknesses, constraints, risks, "
            "or limitations of the proposed method "
            "or study."
        ),
        keywords=(
            "limitation",
            "limitations",
            "threat to validity",
            "threats to validity",
            "weakness",
            "drawback",
            "challenge",
            "risk",
            "future work",
        ),
    ),
)
