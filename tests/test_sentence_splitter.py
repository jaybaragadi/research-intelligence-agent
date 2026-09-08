from src.chunking.sentence_splitter import (
    split_sentences,
)


def test_split_sentences_basic():

    text = (
        "Large language models generate tests. "
        "Coverage is then measured. "
        "Results are compared."
    )

    sentences = split_sentences(
        text
    )

    assert len(sentences) == 3

    assert sentences[0] == (
        "Large language models generate tests."
    )


def test_split_sentences_empty_text():

    assert split_sentences("") == []


def test_split_sentences_normalizes_whitespace():

    text = (
        "Large language models   generate tests.   "
        "Coverage improves."
    )

    sentences = split_sentences(
        text
    )

    assert len(sentences) == 2

    assert (
        "  "
        not in sentences[0]
    )