from src.models import PaperChunk, PaperMetadata


def test_paper_metadata_creation():
    paper = PaperMetadata(
        paper_id="testpilot",
        title="An Empirical Evaluation of Using Large Language Models for Automated Unit Test Generation",
        authors=[
            "Max Schäfer",
            "Sarah Nadi",
        ],
        year=2023,
    )

    assert paper.paper_id == "testpilot"
    assert paper.year == 2023
    assert len(paper.authors) == 2


def test_paper_chunk_creation():
    chunk = PaperChunk(
        chunk_id="testpilot_chunk_001",
        paper_id="testpilot",
        text="This is an example research-paper chunk.",
        page_number=1,
        chunk_index=0,
    )

    assert chunk.paper_id == "testpilot"
    assert chunk.page_number == 1