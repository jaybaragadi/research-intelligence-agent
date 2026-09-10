import streamlit as st

from src.ui.corpus import (
    CORPUS_PAPERS,
)

from src.ui.presentation import (
    result_section_label,
    search_result_title,
    search_score_label,
)

from src.ui.services import (
    get_search_papers_tool,
)


DEFAULT_SEARCH_QUERY = (
    "How are Large Language Models used "
    "for automated software test generation?"
)


def _paper_label(
    paper_id: str,
) -> str:

    for paper in CORPUS_PAPERS:

        if paper.paper_id == paper_id:

            return (
                f"{paper.paper_id} — "
                f"{paper.title}"
            )

    return paper_id


def _render_result(
    result,
) -> None:

    title = search_result_title(
        rank=result.rank,
        paper_id=result.paper_id,
        page_number=result.page_number,
    )

    with st.container(
        border=True
    ):

        st.markdown(
            f"### {title}"
        )

        st.caption(
            f"Chunk: {result.chunk_id}"
        )

        st.markdown(
            "**Section:** "
            + result_section_label(
                result.section
            )
        )

        score_col1, score_col2, score_col3 = (
            st.columns(3)
        )

        with score_col1:

            st.metric(
                "Combined Score",
                search_score_label(
                    result.score
                ),
            )

        with score_col2:

            st.metric(
                "Semantic Score",
                search_score_label(
                    result.raw_score
                ),
            )

        with score_col3:

            st.metric(
                "Lexical Score",
                search_score_label(
                    result.lexical_score
                ),
            )

        st.markdown(
            "**Evidence Text**"
        )

        st.write(
            result.text
        )


def render_paper_search_page() -> None:

    st.title(
        "Paper Search"
    )

    st.write(
        """
        Search the indexed research corpus using
        semantic and lexical retrieval.
        """
    )

    st.info(
        """
        Results are returned from the existing
        research retrieval layer and preserve
        paper, page, section, and chunk provenance.
        """
    )

    query = st.text_area(
        "Search Query",
        value=DEFAULT_SEARCH_QUERY,
        height=120,
    )

    paper_ids = [
        paper.paper_id
        for paper in CORPUS_PAPERS
    ]

    selected_papers = st.multiselect(
        "Limit search to specific papers",
        options=paper_ids,
        default=[],
        format_func=_paper_label,
    )

    col1, col2 = st.columns(2)

    with col1:

        top_k = st.slider(
            "Maximum results",
            min_value=1,
            max_value=20,
            value=8,
        )

    with col2:

        max_per_paper = st.slider(
            "Maximum results per paper",
            min_value=1,
            max_value=10,
            value=3,
        )

    search = st.button(
        "Search Research Evidence",
        type="primary",
    )

    if not search:
        return

    cleaned_query = query.strip()

    if not cleaned_query:

        st.warning(
            "Enter a search query."
        )

        return

    allowed_paper_ids = (
        set(selected_papers)
        if selected_papers
        else None
    )

    try:

        with st.spinner(
            "Searching indexed research evidence..."
        ):

            tool = (
                get_search_papers_tool()
            )

            response = tool.search(
                query=cleaned_query,
                top_k=top_k,
                allowed_paper_ids=(
                    allowed_paper_ids
                ),
                max_per_paper=(
                    max_per_paper
                ),
            )

    except Exception as exc:

        st.error(
            "Research evidence search could not be completed."
        )

        st.exception(
            exc
        )

        return

    st.divider()

    st.subheader(
        "Search Results"
    )

    st.markdown(
        f"**Query:** {response.query}"
    )

    st.metric(
        "Results Returned",
        response.result_count,
    )

    if response.result_count == 0:

        st.info(
            """
            No matching evidence was retrieved.
            This does not mean the topic does not
            exist in the broader literature.
            """
        )

        return

    for result in response.results:

        _render_result(
            result
        )

    st.caption(
        """
        Search results represent evidence retrieved
        from the indexed corpus only. Retrieval
        ranking should not be interpreted as
        scientific importance.
        """
    )