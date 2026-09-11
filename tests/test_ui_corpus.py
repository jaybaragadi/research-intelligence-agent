from src.ui.corpus import (
    CORPUS_PAPERS,
    get_paper_by_id,
    get_paper_ids,
)


def test_corpus_contains_ten_papers():

    assert len(CORPUS_PAPERS) == 10


def test_paper_ids_are_unique():

    paper_ids = get_paper_ids()

    assert len(paper_ids) == len(set(paper_ids))


def test_expected_paper_ids_exist():

    assert get_paper_ids() == [
        "01_testpilot",
        "02_chattester",
        "03_mutap",
        "04_symprompt",
        "05_coverup",
        "06_chatunitest",
        "07_codamosa",
        "08_telpa",
        "09_hits",
        "10_coding_before_testing",
    ]


def test_get_paper_by_id():

    paper = get_paper_by_id("03_mutap")

    assert paper is not None

    assert paper.paper_id == "03_mutap"


def test_unknown_paper_returns_none():

    assert get_paper_by_id("unknown") is None
