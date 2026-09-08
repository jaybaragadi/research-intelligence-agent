from src.chunking.section_mapper import (
    section_for_page,
)

from src.chunking.sentence_splitter import (
    split_sentences,
)

from src.models import (
    ExtractedPaper,
    PaperChunk,
    PaperProfile,
)


def build_chunk_id(
    paper_id: str,
    chunk_index: int,
) -> str:
    """
    Create a stable chunk identifier.

    Example:
        01_testpilot_chunk_0000
        01_testpilot_chunk_0001
    """

    return (
        f"{paper_id}_chunk_"
        f"{chunk_index:04d}"
    )


def split_long_text(
    text: str,
    max_size: int,
) -> list[str]:
    """
    Split an unusually long sentence-like unit into
    smaller pieces.

    This is primarily a fallback for PDF extraction
    artifacts such as:

    - flattened tables
    - long captions
    - reference blocks
    - text where punctuation was lost during extraction

    Splitting is performed on word boundaries so that
    no returned part exceeds max_size whenever possible.
    """

    if not text:
        return []

    if len(text) <= max_size:
        return [text]

    words = text.split()

    parts: list[str] = []

    current_words: list[str] = []
    current_length = 0

    for word in words:

        # Extremely unusual case where one extracted
        # token itself is larger than max_size.
        if len(word) > max_size:

            if current_words:

                parts.append(
                    " ".join(
                        current_words
                    )
                )

                current_words = []
                current_length = 0

            start = 0

            while start < len(word):

                parts.append(
                    word[
                        start:
                        start + max_size
                    ]
                )

                start += max_size

            continue

        separator_length = (
            1
            if current_words
            else 0
        )

        projected_length = (
            current_length
            + separator_length
            + len(word)
        )

        if (
            current_words
            and projected_length > max_size
        ):

            parts.append(
                " ".join(
                    current_words
                )
            )

            current_words = [
                word
            ]

            current_length = len(
                word
            )

        else:

            current_words.append(
                word
            )

            current_length = (
                projected_length
            )

    if current_words:

        parts.append(
            " ".join(
                current_words
            )
        )

    return parts


def build_overlap(
    previous_units: list[str],
    chunk_overlap: int,
) -> list[str]:
    """
    Preserve a small amount of text from the previous
    chunk.

    Whole sentence-like units are preferred so that the
    overlap remains readable and semantically meaningful.
    """

    if chunk_overlap <= 0:
        return []

    overlap_units: list[str] = []
    overlap_length = 0

    for unit in reversed(
        previous_units
    ):

        separator_length = (
            1
            if overlap_units
            else 0
        )

        projected_length = (
            overlap_length
            + separator_length
            + len(unit)
        )

        if projected_length > chunk_overlap:
            break

        overlap_units.insert(
            0,
            unit,
        )

        overlap_length = (
            projected_length
        )

    return overlap_units


def create_page_chunks(
    paper: ExtractedPaper,
    profile: PaperProfile,
    chunk_size: int,
    chunk_overlap: int,
) -> list[PaperChunk]:
    """
    Build sentence-aware chunks while preserving
    research-paper provenance.

    Important design rules:

    1. Chunks never cross PDF page boundaries.
    2. Section metadata is attached when available.
    3. Sentence boundaries are preferred.
    4. Very long extracted sentences are split safely.
    5. Small overlap is carried between chunks from
       the same page.
    """

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be positive"
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative"
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller "
            "than chunk_size"
        )

    chunks: list[PaperChunk] = []

    chunk_index = 0

    for page in paper.pages:

        sentences = split_sentences(
            page.text
        )

        if not sentences:
            continue

        section = section_for_page(
            page.page_number,
            profile,
        )

        # Convert very long extracted sentence-like
        # units into safe-sized units first.
        page_units: list[str] = []

        for sentence in sentences:

            sentence_parts = split_long_text(
                sentence,
                chunk_size,
            )

            page_units.extend(
                sentence_parts
            )

        current_units: list[str] = []

        for unit in page_units:

            current_text = " ".join(
                current_units
            )

            projected_length = (
                len(current_text)
                + (
                    1
                    if current_units
                    else 0
                )
                + len(unit)
            )

            # Current chunk is full enough.
            if (
                current_units
                and projected_length > chunk_size
            ):

                chunk_text = " ".join(
                    current_units
                )

                chunks.append(
                    PaperChunk(
                        chunk_id=build_chunk_id(
                            paper.paper_id,
                            chunk_index,
                        ),
                        paper_id=paper.paper_id,
                        text=chunk_text,
                        page_number=(
                            page.page_number
                        ),
                        section=section,
                        chunk_index=chunk_index,
                        character_count=len(
                            chunk_text
                        ),
                    )
                )

                chunk_index += 1

                # Carry controlled overlap into the
                # next chunk.
                current_units = build_overlap(
                    previous_units=(
                        current_units
                    ),
                    chunk_overlap=(
                        chunk_overlap
                    ),
                )

                current_text = " ".join(
                    current_units
                )

                # Important safety check:
                # overlap + new unit must still fit.
                projected_length = (
                    len(current_text)
                    + (
                        1
                        if current_units
                        else 0
                    )
                    + len(unit)
                )

                # If the overlap would make the new
                # chunk exceed chunk_size, drop overlap.
                if projected_length > chunk_size:

                    current_units = []

            current_units.append(
                unit
            )

        # Flush the remaining content for this page.
        if current_units:

            chunk_text = " ".join(
                current_units
            )

            chunks.append(
                PaperChunk(
                    chunk_id=build_chunk_id(
                        paper.paper_id,
                        chunk_index,
                    ),
                    paper_id=paper.paper_id,
                    text=chunk_text,
                    page_number=(
                        page.page_number
                    ),
                    section=section,
                    chunk_index=chunk_index,
                    character_count=len(
                        chunk_text
                    ),
                )
            )

            chunk_index += 1

    return chunks