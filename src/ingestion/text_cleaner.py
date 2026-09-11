import re


def clean_text(text: str) -> str:
    """
    Clean text extracted from PDF pages.

    The goal is conservative cleaning:
    preserve academic content while removing obvious
    extraction noise.
    """

    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Join words broken by line-wrap hyphenation.
    # Example:
    # "auto-\nmated" -> "automated"
    text = re.sub(
        r"(?<=\w)-\n(?=\w)",
        "",
        text,
    )

    # Replace single newlines inside paragraphs with spaces.
    # Preserve paragraph boundaries represented by blank lines.
    text = re.sub(
        r"(?<!\n)\n(?!\n)",
        " ",
        text,
    )

    # Collapse excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()
