from src.ingestion.paper_discovery import discover_pdfs


def test_discover_pdfs(tmp_path):
    pdf1 = tmp_path / "paper2.pdf"
    pdf2 = tmp_path / "paper1.pdf"
    txt = tmp_path / "notes.txt"

    pdf1.write_bytes(b"fake")
    pdf2.write_bytes(b"fake")
    txt.write_text("ignore me")

    results = discover_pdfs(tmp_path)

    assert len(results) == 2

    assert results[0].name == "paper1.pdf"
    assert results[1].name == "paper2.pdf"