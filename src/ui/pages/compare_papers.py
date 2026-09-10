import streamlit as st

from src.ui.corpus import (
    CORPUS_PAPERS,
)

from src.ui.presentation import (
    comparison_cell_status,
    dimension_label,
    join_evidence_ids,
)

from src.ui.services import (
    get_comparative_analysis_service,
)


DEFAULT_COMPARISON_QUERY = (
    "How do these approaches differ in their "
    "test generation strategy, feedback mechanisms, "
    "iteration strategy, evaluation methods, "
    "quality objectives, and limitations?"
)


def _paper_option_label(
    paper_id: str,
) -> str:

    for paper in CORPUS_PAPERS:

        if paper.paper_id == paper_id:

            return (
                f"{paper.paper_id} — "
                f"{paper.title}"
            )

    return paper_id


def _render_comparison_matrix(
    result,
) -> None:

    st.subheader(
        "Comparison Matrix"
    )

    for row in result.matrix:

        st.markdown(
            f"### {dimension_label(row.dimension)}"
        )

        for cell in row.cells:

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**{_paper_option_label(cell.paper_id)}**"
                )

                st.write(
                    comparison_cell_status(
                        cell.summary
                    )
                )

                if cell.evidence_ids:

                    st.caption(
                        "Evidence: "
                        + join_evidence_ids(
                            cell.evidence_ids
                        )
                    )


def _render_findings(
    result,
) -> None:

    st.subheader(
        "Cross-Paper Findings"
    )

    if not result.findings:

        st.info(
            "No shared analytical dimensions "
            "were identified from the validated evidence."
        )

        return

    for finding in result.findings:

        with st.container(
            border=True
        ):

            st.markdown(
                f"**{finding.finding_id}**"
            )

            st.write(
                finding.text
            )

            st.markdown(
                "**Papers:** "
                + ", ".join(
                    finding.paper_ids
                )
            )

            st.caption(
                "Evidence: "
                + join_evidence_ids(
                    finding.evidence_ids
                )
            )


def render_compare_papers_page() -> None:

    st.title(
        "Compare Research Papers"
    )

    st.write(
        """
        Compare two or more papers using the structured
        evidence-grounded comparative analysis developed
        in Phase 9.
        """
    )

    st.info(
        """
        The system compares validated evidence across
        research dimensions such as generation strategy,
        feedback, iteration, quality objectives,
        evaluation methods, and limitations.
        """
    )

    paper_ids = [
        paper.paper_id
        for paper in CORPUS_PAPERS
    ]

    selected_papers = st.multiselect(
        "Select papers to compare",
        options=paper_ids,
        default=[
            "03_mutap",
            "05_coverup",
        ],
        format_func=_paper_option_label,
    )

    query = st.text_area(
        "Comparison Question",
        value=DEFAULT_COMPARISON_QUERY,
        height=130,
    )

    evidence_per_paper = st.slider(
        "Evidence passages per paper",
        min_value=1,
        max_value=10,
        value=6,
    )

    analyze = st.button(
        "Compare Selected Papers",
        type="primary",
    )

    if not analyze:
        return

    if len(selected_papers) < 2:

        st.warning(
            "Select at least two papers."
        )

        return

    cleaned_query = query.strip()

    if not cleaned_query:

        st.warning(
            "Enter a comparison question."
        )

        return

    try:

        with st.spinner(
            "Retrieving and comparing research evidence..."
        ):

            service = (
                get_comparative_analysis_service()
            )

            result = service.analyze(
                paper_ids=selected_papers,
                query=cleaned_query,
                evidence_per_paper=(
                    evidence_per_paper
                ),
            )

    except Exception as exc:

        st.error(
            "The comparative analysis could not be completed."
        )

        st.exception(
            exc
        )

        return

    st.divider()

    st.subheader(
        "Analysis Scope"
    )

    st.write(
        result.query
    )

    st.markdown(
        "**Compared papers:** "
        + ", ".join(
            result.requested_papers
        )
    )

    st.divider()

    _render_comparison_matrix(
        result
    )

    st.divider()

    _render_findings(
        result
    )

    st.caption(
        """
        Scope: Comparison findings describe evidence
        identified in the indexed corpus. Empty cells
        mean that matching validated evidence was not
        identified for that paper/dimension in this
        analysis; they do not prove that the paper or
        broader literature contains no such information.
        """
    )