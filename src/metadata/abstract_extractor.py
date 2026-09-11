import re

from src.models import ExtractedPaper

ABSTRACT_START_PATTERN = re.compile(
    r"\babstract\b" r"\s*[:.\-—–]?\s*",
    flags=re.IGNORECASE,
)


ABSTRACT_END_PATTERNS = [
    re.compile(
        r"\b(?:1|I)[.\s]+introduction\b",
        flags=re.IGNORECASE,
    ),
    re.compile(
        r"\bintroduction\b",
        flags=re.IGNORECASE,
    ),
    re.compile(
        r"\bkeywords?\b",
        flags=re.IGNORECASE,
    ),
    re.compile(
        r"\bindex\s+terms?\b",
        flags=re.IGNORECASE,
    ),
    re.compile(
        r"\bCCS\s+concepts?\b",
        flags=re.IGNORECASE,
    ),
    re.compile(
        r"\bACM\s+reference\s+format\b",
        flags=re.IGNORECASE,
    ),
    re.compile(
        r"\bcategories\s+and\s+subject\s+descriptors\b",
        flags=re.IGNORECASE,
    ),
]


def normalize_abstract(
    text: str,
) -> str:
    """Normalize whitespace in an extracted abstract."""

    return re.sub(
        r"\s+",
        " ",
        text,
    ).strip()


def extract_from_abstract_heading(
    text: str,
) -> str | None:
    """
    Extract text beginning after an explicit Abstract heading.
    """

    start_match = ABSTRACT_START_PATTERN.search(text)

    if not start_match:
        return None

    remaining = text[start_match.end() :]

    end_positions: list[int] = []

    for pattern in ABSTRACT_END_PATTERNS:

        match = pattern.search(remaining)

        if match:
            end_positions.append(match.start())

    if end_positions:

        candidate = remaining[: min(end_positions)]

    else:

        candidate = remaining[:3500]

    candidate = normalize_abstract(candidate)

    if not (80 <= len(candidate) <= 3500):
        return None

    return candidate


def extract_front_matter_fallback(
    text: str,
) -> str | None:
    """
    Last-resort extraction for publisher PDFs where the word
    'Abstract' was lost or merged during PDF extraction.

    The fallback only runs when an Introduction heading exists.
    """

    introduction_patterns = [
        re.compile(
            r"\b1\.?\s+introduction\b",
            flags=re.IGNORECASE,
        ),
        re.compile(
            r"\bI\.?\s+introduction\b",
            flags=re.IGNORECASE,
        ),
        re.compile(
            r"\bintroduction\b",
            flags=re.IGNORECASE,
        ),
    ]

    intro_position = None

    for pattern in introduction_patterns:

        match = pattern.search(text)

        if match:
            intro_position = match.start()
            break

    if intro_position is None:
        return None

    front_matter = text[:intro_position]

    # We cannot safely determine the exact abstract boundary
    # without an Abstract label, so only use the final substantial
    # paragraph-like portion of the front matter.
    sentences = re.split(
        r"(?<=[.!?])\s+",
        front_matter,
    )

    substantial: list[str] = []

    character_count = 0

    for sentence in reversed(sentences):

        sentence = sentence.strip()

        if len(sentence) < 30:
            continue

        substantial.insert(
            0,
            sentence,
        )

        character_count += len(sentence)

        if character_count >= 500:
            break

    candidate = normalize_abstract(" ".join(substantial))

    if not (150 <= len(candidate) <= 2000):
        return None

    return candidate


def extract_abstract(
    paper: ExtractedPaper,
) -> str | None:
    """
    Extract a paper abstract from its opening pages.
    """

    opening_pages = paper.pages[:4]

    if not opening_pages:
        return None

    text = "\n".join(page.text for page in opening_pages)

    abstract = extract_from_abstract_heading(text)

    if abstract:
        return abstract

    return extract_front_matter_fallback(text)
