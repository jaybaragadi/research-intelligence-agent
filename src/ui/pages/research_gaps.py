import streamlit as st

from src.ui.corpus import (
    CORPUS_PAPERS,
)

from src.ui.presentation import (
    coverage_label,
    dimension_label,
    gap_confidence_label,
    gap_type_label,
    join_evidence_ids,
    signal_type_label,
)

from src.ui.services import (
    get_research_gap_analysis_service,
)


DEFAULT_GAP_QUERY = (
    "What limitations, unresolved problems, "
    "underexplored areas, and research gaps are "
    "reported across LLM-based automated software "
    "test generation research?"
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


def _render_validation(
    result,
) -> None:

    validation = result.validation

    if validation is None:

        st.warning(
            "No gap validation result was returned."
        )

        return

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Validation",
            (
                "Valid"
                if validation.is_valid
                else "Invalid"
            ),
        )

    with col2:

        st.metric(
            "Validated Candidates",
            validation.validated_gap_count,
        )

    with col3:

        st.metric(
            "Validation Issues",
            validation.issue_count,
        )

    if validation.issues:

        st.subheader(
            "Validation Issues"
        )

        for issue in validation.issues:

            st.warning(
                f"{issue.issue_type}: "
                f"{issue.message}"
            )


def _render_dimension_coverage(
    result,
) -> None:

    st.subheader(
        "Corpus Evidence Coverage"
    )

    st.write(
        """
        Coverage represents where validated evidence
        was found across the selected indexed papers.
        It does not measure scientific importance.
        """
    )

    corpus_size = len(
        result.corpus_papers
    )

    for coverage in result.dimension_coverage:

        with st.container(
            border=True
        ):

            label = coverage_label(
                coverage.dimension,
                coverage.paper_count,
                corpus_size,
            )

            st.markdown(
                f"**{label}**"
            )
            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Papers with Evidence",
                    coverage.paper_count,
                )

            with col2:

                st.metric(
                    "Evidence Passages",
                    coverage.evidence_count,
                )

            if coverage.paper_ids:

                st.caption(
                    "Papers: "
                    + ", ".join(
                        coverage.paper_ids
                    )
                )

            if coverage.evidence_ids:

                with st.expander(
                    "Evidence IDs"
                ):

                    st.write(
                        join_evidence_ids(
                            coverage.evidence_ids
                        )
                    )


def _render_explicit_signals(
    result,
) -> None:

    st.subheader(
        "Explicit Gap Signals"
    )

    signal_count = sum(
        len(
            item.signals
        )
        for item in result.paper_signals
    )

    if signal_count == 0:

        st.info(
            """
            No explicit limitation, future-work,
            or unresolved-problem signals were
            identified in this run.
            """
        )

        return

    for paper in result.paper_signals:

        if not paper.signals:
            continue

        st.markdown(
            f"### {_paper_label(paper.paper_id)}"
        )

        for signal in paper.signals:

            with st.container(
                border=True
            ):

                st.markdown(
                    "**"
                    + signal_type_label(
                        signal.signal_type
                    )
                    + "**"
                )

                st.write(
                    signal.text
                )

                st.caption(
                    f"Evidence: {signal.evidence_id}"
                )

                st.caption(
                    f"Page: {signal.page_number}"
                )

                if signal.section:

                    st.caption(
                        f"Section: {signal.section}"
                    )

                st.caption(
                    signal.citation_text
                )


def _render_candidates(
    result,
) -> None:

    st.subheader(
        "Research Gap Candidates"
    )

    if not result.candidates:

        st.info(
            """
            No validated gap candidates were produced
            for this selected corpus and query.
            """
        )

        return

    for candidate in result.candidates:

        with st.container(
            border=True
        ):

            st.markdown(
                f"### {candidate.gap_id} — "
                f"{candidate.title}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    "**Type:** "
                    + gap_type_label(
                        candidate.gap_type
                    )
                )

            with col2:

                st.markdown(
                    "**Confidence:** "
                    + gap_confidence_label(
                        candidate.confidence
                    )
                )

            st.write(
                candidate.description
            )

            if candidate.reason:

                st.markdown(
                    f"**Reason:** {candidate.reason}"
                )

            if candidate.paper_ids:

                st.markdown(
                    "**Papers:** "
                    + ", ".join(
                        candidate.paper_ids
                    )
                )

            if candidate.dimensions:

                st.markdown(
                    "**Dimensions:** "
                    + ", ".join(
                        dimension_label(
                            dimension
                        )
                        for dimension
                        in candidate.dimensions
                    )
                )

            if candidate.evidence_ids:

                st.caption(
                    "Evidence: "
                    + join_evidence_ids(
                        candidate.evidence_ids
                    )
                )


def render_research_gaps_page() -> None:

    st.title(
        "Research Gap Analysis"
    )

    st.write(
        """
        Analyze explicit research limitations and
        corpus-level evidence imbalances across the
        indexed software-testing literature.
        """
    )

    st.warning(
        """
        Important: missing retrieved evidence is not
        treated as proof that research does not exist.
        Gap statements remain scoped to the selected
        indexed corpus.
        """
    )

    paper_ids = [
        paper.paper_id
        for paper in CORPUS_PAPERS
    ]

    selected_papers = st.multiselect(
        "Select papers for gap analysis",
        options=paper_ids,
        default=paper_ids,
        format_func=_paper_label,
    )

    query = st.text_area(
        "Gap Analysis Question",
        value=DEFAULT_GAP_QUERY,
        height=130,
    )

    evidence_per_paper = st.slider(
        "Comparative evidence passages per paper",
        min_value=1,
        max_value=12,
        value=8,
    )

    analyze = st.button(
        "Analyze Research Gaps",
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
            "Enter a research-gap question."
        )

        return

    try:

        with st.spinner(
            "Analyzing evidence-grounded research gaps..."
        ):

            service = (
                get_research_gap_analysis_service()
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
            "Research-gap analysis could not be completed."
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
        "**Indexed papers analyzed:** "
        f"{len(result.corpus_papers)}"
    )

    st.caption(
        ", ".join(
            result.corpus_papers
        )
    )

    st.divider()

    _render_validation(
        result
    )

    st.divider()

    _render_dimension_coverage(
        result
    )

    st.divider()

    _render_explicit_signals(
        result
    )

    st.divider()

    _render_candidates(
        result
    )

    st.caption(
        """
        Interpretation rule: absence of retrieved
        evidence is not equivalent to absence of
        research. Results describe only evidence
        found in the selected indexed corpus.
        """
    )