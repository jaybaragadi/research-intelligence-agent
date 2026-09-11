import re

SENTENCE_BOUNDARY_PATTERN = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")


def split_sentences(
    text: str,
) -> list[str]:
    """
    Split academic text into sentence-like units.

    This intentionally remains lightweight so that the project
    does not depend on an external NLP model just for chunking.
    """

    if not text:
        return []

    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    sentences = SENTENCE_BOUNDARY_PATTERN.split(text)

    return [sentence.strip() for sentence in sentences if sentence.strip()]
