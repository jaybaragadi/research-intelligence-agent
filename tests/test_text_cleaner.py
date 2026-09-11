from src.ingestion.text_cleaner import clean_text


def test_clean_text_removes_extra_spaces():
    text = "Large    language    models"

    result = clean_text(text)

    assert result == "Large language models"


def test_clean_text_repairs_hyphenated_line_break():
    text = "auto-\nmated testing"

    result = clean_text(text)

    assert result == "automated testing"


def test_clean_text_joins_single_line_break():
    text = "Large language models\nfor software testing"

    result = clean_text(text)

    assert result == ("Large language models for software testing")


def test_clean_text_preserves_paragraph_break():
    text = "First paragraph.\n\n" "Second paragraph."

    result = clean_text(text)

    assert "\n\n" in result
