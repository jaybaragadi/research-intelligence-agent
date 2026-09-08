from src.retrieval.retriever import (
    SemanticRetriever,
)


def create_retriever_without_init(
) -> SemanticRetriever:
    """
    Create the retriever without loading the real
    embedding model or FAISS store.
    """

    return SemanticRetriever.__new__(
        SemanticRetriever
    )


def test_references_receive_no_priority():

    retriever = (
        create_retriever_without_init()
    )

    bonus = (
        retriever._section_bonus(
            "references"
        )
    )

    assert bonus == 0.0


def test_methodology_has_positive_bonus():

    retriever = (
        create_retriever_without_init()
    )

    bonus = (
        retriever._section_bonus(
            "methodology"
        )
    )

    assert bonus > 0


def test_limitation_query_boosts_limitations():

    retriever = (
        create_retriever_without_init()
    )

    bonus = (
        retriever._query_section_bonus(
            (
                "What limitations are "
                "reported?"
            ),
            "limitations",
        )
    )

    assert bonus > 0


def test_limitation_query_does_not_boost_methodology():

    retriever = (
        create_retriever_without_init()
    )

    bonus = (
        retriever._query_section_bonus(
            (
                "What limitations are "
                "reported?"
            ),
            "methodology",
        )
    )

    assert bonus == 0


def test_coverage_query_boosts_evaluation():

    retriever = (
        create_retriever_without_init()
    )

    bonus = (
        retriever._query_section_bonus(
            (
                "How do techniques improve "
                "code coverage?"
            ),
            "evaluation",
        )
    )

    assert bonus > 0


def test_lexical_score_detects_overlap():

    retriever = (
        create_retriever_without_init()
    )

    score = (
        retriever._lexical_score(
            (
                "iterative feedback "
                "generated tests"
            ),
            (
                "The method uses an iterative "
                "feedback process to improve "
                "generated tests."
            ),
        )
    )

    assert score > 0.5


def test_lexical_score_is_zero_without_overlap():

    retriever = (
        create_retriever_without_init()
    )

    score = (
        retriever._lexical_score(
            "mutation testing",
            "neural network image classification",
        )
    )

    assert score == 0.0


def test_reference_detector_identifies_bibliography_text():

    retriever = (
        create_retriever_without_init()
    )

    text = """
    Smith et al. 2023. Software Testing.
    arXiv:2301.00001.
    https://doi.org/10.1000/test.
    Jones et al. 2022.
    Proc. ACM Software Engineering.
    IEEE Computer Society.
    """

    assert (
        retriever._looks_like_reference_text(
            text
        )
        is True
    )


def test_reference_detector_keeps_normal_research_text():

    retriever = (
        create_retriever_without_init()
    )

    text = (
        "The proposed method repeatedly generates "
        "tests, executes them, and provides feedback "
        "to the language model until coverage improves."
    )

    assert (
        retriever._looks_like_reference_text(
            text
        )
        is False
    )


def test_hybrid_score_rewards_lexical_alignment():

    retriever = (
        create_retriever_without_init()
    )

    aligned_score, _ = (
        retriever._hybrid_score(
            query=(
                "iterative feedback generated tests"
            ),
            text=(
                "The iterative feedback process "
                "improves generated tests."
            ),
            raw_score=0.60,
            section="methodology",
        )
    )

    weak_score, _ = (
        retriever._hybrid_score(
            query=(
                "iterative feedback generated tests"
            ),
            text=(
                "This study evaluates unit test "
                "generation with language models."
            ),
            raw_score=0.60,
            section="methodology",
        )
    )

    assert (
        aligned_score
        > weak_score
    )


def test_token_normalization():

    retriever = (
        create_retriever_without_init()
    )

    assert (
        retriever._normalize_token(
            "tests"
        )
        == "test"
    )

    assert (
        retriever._normalize_token(
            "generated"
        )
        == "generate"
    )

    assert (
        retriever._normalize_token(
            "limitations"
        )
        == "limitation"
    )


def test_normalized_lexical_score_matches_variants():

    retriever = (
        create_retriever_without_init()
    )

    score = (
        retriever._lexical_score(
            (
                "improve generated tests"
            ),
            (
                "The approach improves "
                "test generation."
            ),
        )
    )

    assert score > 0.5


def test_concept_alignment_rewards_direct_evidence():

    retriever = (
        create_retriever_without_init()
    )

    direct_bonus = (
        retriever._concept_alignment_bonus(
            (
                "iterative feedback improve "
                "generated tests"
            ),
            (
                "The iterative feedback process "
                "improves generated tests."
            ),
        )
    )

    weak_bonus = (
        retriever._concept_alignment_bonus(
            (
                "iterative feedback improve "
                "generated tests"
            ),
            (
                "The study evaluates test "
                "generation techniques."
            ),
        )
    )

    assert (
        direct_bonus
        > weak_bonus
    )