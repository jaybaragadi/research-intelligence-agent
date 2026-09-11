import streamlit as st

from src.ui.presentation import (
    evidence_section,
    evidence_title,
    grounding_status,
)
from src.ui.services import (
    get_grounded_answer_service,
)

DEFAULT_QUESTION = (
    "How are Large Language Models being used "
    "to improve automated software test generation?"
)


def _render_grounding_status(answer) -> None:

    validation = answer.validation

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Grounding Valid",
            grounding_status(validation.is_valid),
        )

    with col2:
        st.metric(
            "Validated Claims",
            validation.validated_claim_count,
        )

    with col3:
        st.metric(
            "Grounding Issues",
            validation.issue_count,
        )


def _render_claims(answer) -> None:

    st.subheader("Grounded Claims")

    if not answer.claims:

        st.info("No grounded claims were generated.")

        return

    for claim in answer.claims:

        with st.container(border=True):

            st.markdown(f"**{claim.claim_id}**")

            st.write(claim.text)

            if claim.evidence_ids:

                st.caption("Evidence: " + ", ".join(claim.evidence_ids))


def _render_evidence(answer) -> None:

    st.subheader("Supporting Evidence")

    if not answer.evidence:

        st.info("No supporting evidence was retrieved.")

        return

    for evidence in answer.evidence:

        section = evidence_section(evidence.section)

        title = evidence_title(
            evidence_id=evidence.evidence_id,
            paper_id=evidence.paper_id,
            page_number=evidence.page_number,
        )

        with st.expander(title):

            st.markdown(f"**Section:** {section}")

            st.write(evidence.text)

            st.caption(evidence.citation_text)


def _render_validation_issues(
    answer,
) -> None:

    validation = answer.validation

    if not validation.issues:
        return

    st.subheader("Grounding Validation Issues")

    for issue in validation.issues:

        st.warning(f"{issue.issue_type}: " f"{issue.message}")


def render_research_qa_page() -> None:

    st.title("Research Q&A")

    st.write("""
        Ask a research question about the indexed
        software-testing literature. Answers are
        generated only from retrieved evidence in
        the current corpus.
        """)

    st.info("""
        Evidence grounding is preserved from the
        backend. Each answer can be traced to the
        supporting paper, page, section, and chunk.
        """)

    query = st.text_area(
        "Research Question",
        value=DEFAULT_QUESTION,
        height=120,
    )

    top_k = st.slider(
        "Evidence passages to retrieve",
        min_value=1,
        max_value=10,
        value=5,
    )

    ask = st.button(
        "Analyze Research Question",
        type="primary",
    )

    if not ask:
        return

    cleaned_query = query.strip()

    if not cleaned_query:

        st.warning("Enter a research question.")

        return

    try:

        with st.spinner("Retrieving and validating evidence..."):

            service = get_grounded_answer_service()

            answer = service.answer_search(
                query=cleaned_query,
                top_k=top_k,
            )

    except Exception as exc:

        st.error("The research question could not be processed.")

        st.exception(exc)

        return

    st.divider()

    st.subheader("Evidence-Grounded Answer")

    st.write(answer.answer_text)

    _render_grounding_status(answer)

    st.divider()

    _render_claims(answer)

    st.divider()

    _render_evidence(answer)

    _render_validation_issues(answer)

    st.caption("""
        Scope: Results describe evidence available
        in the indexed corpus. Missing evidence
        should not be interpreted as proof that
        research does not exist elsewhere.
        """)
