import streamlit as st

from src.ui.corpus import (
    CORPUS_PAPERS,
)
from src.ui.presentation import (
    literature_review_filename,
    review_validation_status,
)
from src.ui.services import (
    get_literature_review_renderer,
    get_literature_review_service,
)

DEFAULT_REVIEW_QUERY = (
    "How are Large Language Models and Generative AI "
    "being used to improve software testing and "
    "quality assurance?"
)


DEFAULT_REVIEW_TITLE = "Large Language Models for Automated " "Software Test Generation"


def _paper_label(
    paper_id: str,
) -> str:

    for paper in CORPUS_PAPERS:

        if paper.paper_id == paper_id:

            return f"{paper.paper_id} — " f"{paper.title}"

    return paper_id


def _render_review_summary(
    review,
) -> None:

    st.subheader("Review Summary")

    validation_status = review_validation_status(review.validation)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Indexed Papers",
            len(review.paper_ids),
        )

    with col2:

        st.metric(
            "Review Sections",
            len(review.sections),
        )

    with col3:

        st.metric(
            "Grounding",
            validation_status,
        )

    st.markdown("**Research Question**")

    st.write(review.query)

    st.markdown("**Corpus**")

    st.caption(", ".join(review.paper_ids))


def _render_review_sections(
    review,
) -> None:

    st.subheader("Literature Review")

    for section in review.sections:

        st.markdown(f"## {section.title}")

        if section.objective:

            st.caption(f"Section objective: " f"{section.objective}")

        if section.narrative:

            st.write(section.narrative)

        else:

            st.info("No narrative was generated " "for this section.")

        if section.findings:

            with st.expander("Structured Findings"):

                for finding in section.findings:

                    st.markdown(f"**{finding.finding_id}**")

                    st.write(finding.statement)

                    if finding.paper_ids:

                        st.caption("Papers: " + ", ".join(finding.paper_ids))

                    if finding.evidence_ids:

                        st.caption("Evidence: " + ", ".join(finding.evidence_ids))

        if section.evidence:

            with st.expander(f"Supporting Evidence " f"({len(section.evidence)})"):

                for evidence in section.evidence:

                    st.markdown(f"**{evidence.evidence_id}**")

                    st.caption(f"Paper: {evidence.paper_id}")

                    st.caption(f"Page: {evidence.page_number}")

                    if evidence.section:

                        st.caption(f"Section: {evidence.section}")

                    st.write(evidence.text)

                    st.caption(evidence.citation_text)

                    st.divider()


def _render_citations(
    review,
) -> None:

    st.subheader("Citation Index")

    if not review.citations:

        st.info("No citation entries were generated.")

        return

    for number, citation in enumerate(
        review.citations,
        start=1,
    ):

        st.markdown(f"{number}. {citation}")


def _render_validation(
    review,
) -> None:

    st.subheader("Grounding Validation")

    validation = review.validation

    if validation is None:

        st.warning("No grounding validation result " "was attached to this review.")

        return

    if validation.valid:

        st.success("Grounding validation passed.")

    else:

        st.error("Grounding validation failed.")

    st.metric(
        "Validation Issues",
        len(validation.issues),
    )

    for issue in validation.issues:

        code = (
            issue.code.value
            if hasattr(
                issue.code,
                "value",
            )
            else str(issue.code)
        )

        st.warning(f"{code}: {issue.message}")


def render_literature_review_page() -> None:

    st.title("Literature Review")

    st.write("""
        Generate an evidence-grounded literature review
        across selected papers from the indexed corpus.
        """)

    st.info("""
        The review is produced through the existing
        Phase 11 pipeline: comparative analysis,
        research-gap analysis, evidence aggregation,
        cross-paper synthesis, grounding validation,
        and deterministic generation.
        """)

    paper_ids = [paper.paper_id for paper in CORPUS_PAPERS]

    selected_papers = st.multiselect(
        "Select papers for the literature review",
        options=paper_ids,
        default=paper_ids,
        format_func=_paper_label,
    )

    title = st.text_input(
        "Review Title",
        value=DEFAULT_REVIEW_TITLE,
    )

    query = st.text_area(
        "Research Question",
        value=DEFAULT_REVIEW_QUERY,
        height=130,
    )

    evidence_per_paper = st.slider(
        "Evidence passages per paper",
        min_value=1,
        max_value=12,
        value=8,
    )

    generate = st.button(
        "Generate Literature Review",
        type="primary",
    )

    if not generate:
        return

    cleaned_title = title.strip()

    cleaned_query = query.strip()

    if len(selected_papers) < 2:

        st.warning("Select at least two papers.")

        return

    if not cleaned_title:

        st.warning("Enter a literature-review title.")

        return

    if not cleaned_query:

        st.warning("Enter a research question.")

        return

    try:

        with st.spinner("Generating evidence-grounded literature review..."):

            service = get_literature_review_service()

            review = service.generate(
                query=cleaned_query,
                paper_ids=selected_papers,
                title=cleaned_title,
                evidence_per_paper=(evidence_per_paper),
            )

            renderer = get_literature_review_renderer()

            markdown_report = renderer.render(review)

    except Exception as exc:

        st.error("The literature review could not be generated.")

        st.exception(exc)

        return

    st.divider()

    _render_review_summary(review)

    st.divider()

    _render_review_sections(review)

    st.divider()

    _render_citations(review)

    st.divider()

    st.subheader("Scope Note")

    st.warning(review.corpus_scope_note)

    st.divider()

    _render_validation(review)

    st.divider()

    st.subheader("Download Report")

    filename = literature_review_filename(review.title)

    st.download_button(
        label="Download Markdown Literature Review",
        data=markdown_report,
        file_name=filename,
        mime="text/markdown",
    )
