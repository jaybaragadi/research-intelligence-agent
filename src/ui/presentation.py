def evidence_title(
    evidence_id: str,
    paper_id: str,
    page_number: int,
) -> str:

    return f"{evidence_id} | " f"{paper_id} | " f"Page {page_number}"


def evidence_section(
    section: str | None,
) -> str:

    if section:
        return section

    return "Unspecified"


def grounding_status(
    is_valid: bool,
) -> str:

    return "Yes" if is_valid else "No"


def dimension_label(
    dimension: str,
) -> str:

    labels = {
        "generation_strategy": "Generation Strategy",
        "feedback_signal": "Feedback Signal",
        "iteration_strategy": "Iteration Strategy",
        "quality_objective": "Quality Objective",
        "evaluation_method": "Evaluation Method",
        "limitations": "Limitations",
    }

    return labels.get(
        dimension,
        dimension.replace(
            "_",
            " ",
        ).title(),
    )


def comparison_cell_status(
    summary: str | None,
) -> str:

    if summary:
        return summary

    return "No matching validated evidence " "was identified for this dimension."


def join_evidence_ids(
    evidence_ids: list[str],
) -> str:

    if not evidence_ids:
        return "None"

    return ", ".join(evidence_ids)


def gap_type_label(
    gap_type,
) -> str:

    value = gap_type.value if hasattr(gap_type, "value") else str(gap_type)

    labels = {
        "explicit": "Explicit Gap",
        "corpus_imbalance": "Corpus Imbalance",
        "insufficient_evidence": "Insufficient Evidence",
    }

    return labels.get(
        value,
        value.replace(
            "_",
            " ",
        ).title(),
    )


def gap_confidence_label(
    confidence,
) -> str:

    value = confidence.value if hasattr(confidence, "value") else str(confidence)

    return value.title()


def signal_type_label(
    signal_type,
) -> str:

    value = signal_type.value if hasattr(signal_type, "value") else str(signal_type)

    return value.replace(
        "_",
        " ",
    ).title()


def coverage_label(
    dimension: str,
    paper_count: int,
    corpus_size: int,
) -> str:

    return f"{dimension_label(dimension)}: " f"{paper_count}/{corpus_size} papers"


def review_section_label(
    section_type,
) -> str:

    value = section_type.value if hasattr(section_type, "value") else str(section_type)

    return value.replace(
        "_",
        " ",
    ).title()


def literature_review_filename(
    title: str,
) -> str:

    cleaned = "".join(
        character.lower() if character.isalnum() else "_" for character in title.strip()
    )

    cleaned = "_".join(part for part in cleaned.split("_") if part)

    if not cleaned:
        cleaned = "literature_review"

    return cleaned + ".md"


def review_validation_status(
    validation,
) -> str:

    if validation is None:
        return "Not Available"

    return "Valid" if validation.valid else "Invalid"


def search_result_title(
    rank: int,
    paper_id: str,
    page_number: int,
) -> str:

    return f"#{rank} | " f"{paper_id} | " f"Page {page_number}"


def search_score_label(
    score: float,
) -> str:

    return f"{score:.4f}"


def result_section_label(
    section: str | None,
) -> str:

    if section:
        return section

    return "Unspecified"


def page_intro(
    title: str,
    description: str,
) -> tuple[str, str]:

    return (
        title.strip(),
        description.strip(),
    )
