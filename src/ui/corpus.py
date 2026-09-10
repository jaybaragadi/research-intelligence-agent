from dataclasses import dataclass


@dataclass(frozen=True)
class CorpusPaper:
    paper_id: str
    title: str
    year: int


CORPUS_PAPERS = [
    CorpusPaper(
        paper_id="01_testpilot",
        title=(
            "An Empirical Evaluation of Using Large Language Models "
            "for Automated Unit Test Generation"
        ),
        year=2023,
    ),
    CorpusPaper(
        paper_id="02_chattester",
        title=(
            "No More Manual Tests? Evaluating and Improving ChatGPT "
            "for Unit Test Generation"
        ),
        year=2024,
    ),
    CorpusPaper(
        paper_id="03_mutap",
        title=(
            "Effective Test Generation Using Pre-trained Large "
            "Language Models and Mutation Testing"
        ),
        year=2023,
    ),
    CorpusPaper(
        paper_id="04_symprompt",
        title=(
            "Code-Aware Prompting: A Study of Coverage-Guided "
            "Test Generation in Regression Setting using LLM"
        ),
        year=2024,
    ),
    CorpusPaper(
        paper_id="05_coverup",
        title=(
            "CoverUp: Effective High Coverage Test Generation "
            "for Python"
        ),
        year=2025,
    ),
    CorpusPaper(
        paper_id="06_chatunitest",
        title="ChatUniTest: A Framework for LLM-Based Test Generation",
        year=2024,
    ),
    CorpusPaper(
        paper_id="07_codamosa",
        title=(
            "CODAMOSA: Escaping Coverage Plateaus in Test Generation "
            "with Pre-trained Large Language Models"
        ),
        year=2023,
    ),
    CorpusPaper(
        paper_id="08_telpa",
        title=(
            "Advancing Code Coverage: Incorporating Program Analysis "
            "with Large Language Models"
        ),
        year=2025,
    ),
    CorpusPaper(
        paper_id="09_hits",
        title=(
            "HITS: High-coverage LLM-based Unit Test Generation "
            "via Method Slicing"
        ),
        year=2024,
    ),
    CorpusPaper(
        paper_id="10_coding_before_testing",
        title=(
            "On the Risk of Coding Before Testing: "
            "An Empirical Study on LLM-Based Test Generation Workflow"
        ),
        year=2026,
    ),
]


def get_paper_ids() -> list[str]:
    return [
        paper.paper_id
        for paper in CORPUS_PAPERS
    ]


def get_paper_by_id(
    paper_id: str,
) -> CorpusPaper | None:

    for paper in CORPUS_PAPERS:

        if paper.paper_id == paper_id:
            return paper

    return None