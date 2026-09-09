import re


COMPARE_PREFIXES = (
    "compare",
    "comparison",
    "contrast",
)


def build_comparison_focus_query(
    query: str,
    paper_ids: list[str],
) -> str:
    """
    Remove comparison instructions and requested
    paper names from the retrieval query.

    Paper scoping is already handled by
    ComparePapersTool, so names such as MuTAP
    and CoverUp should not influence semantic
    ranking inside those papers.
    """

    focused = query.strip().lower()

    for prefix in COMPARE_PREFIXES:

        focused = re.sub(
            rf"\b{re.escape(prefix)}\b",
            " ",
            focused,
        )

    # Remove human-readable forms derived from
    # canonical corpus IDs.
    #
    # 03_mutap -> mutap
    # 05_coverup -> coverup
    # 10_coding_before_testing
    #     -> coding before testing
    for paper_id in paper_ids:

        name = re.sub(
            r"^\d{2}_",
            "",
            paper_id.lower(),
        )

        alias = name.replace(
            "_",
            " ",
        )

        focused = re.sub(
            rf"\b{re.escape(alias)}\b",
            " ",
            focused,
        )

        # Also handle compact forms such as
        # CoverUp / ChatUniTest after lowercase
        # normalization.
        compact = alias.replace(
            " ",
            "",
        )

        focused = re.sub(
            rf"\b{re.escape(compact)}\b",
            " ",
            focused,
        )

    # Remove command/connective language that
    # contributes little to evidence retrieval.
    focused = re.sub(
        r"\b("
        r"how|do|does|did|and|versus|vs|"
        r"between|for|the|a|an"
        r")\b",
        " ",
        focused,
    )

    focused = re.sub(
        r"\s+",
        " ",
        focused,
    ).strip()

    # Never accidentally issue an empty search.
    return (
        focused
        if focused
        else query.strip()
    )