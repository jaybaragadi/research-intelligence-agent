import streamlit as st

from src.ui.corpus import (
    CORPUS_PAPERS,
)


def render_home_page() -> None:

    st.title("Research Intelligence Agent")

    st.subheader("Evidence-Grounded Research Analysis")

    st.write("""
        This application analyzes an indexed corpus of
        research papers focused on Large Language Models
        and automated software test generation.
        """)

    st.info("""
        The system is designed around evidence grounding.
        Research findings are linked back to the indexed
        paper, page, section, and evidence chunk.
        """)

    st.subheader("Research Capabilities")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
            **Evidence-Grounded Q&A**

            Ask research questions and retrieve
            supporting evidence from the corpus.

            **Paper Comparison**

            Compare methodologies, feedback strategies,
            evaluation approaches, and limitations.
            """)

    with col2:

        st.markdown("""
            **Research Gap Analysis**

            Identify explicit gaps and corpus-level
            evidence imbalances without treating missing
            retrieval as proof that research does not exist.

            **Literature Review Generation**

            Generate structured, evidence-grounded
            literature reviews across multiple papers.
            """)

    st.subheader("Indexed Research Corpus")

    for paper in CORPUS_PAPERS:

        st.markdown(f"""
            **{paper.paper_id}**

            {paper.title} ({paper.year})
            """)

        st.divider()
