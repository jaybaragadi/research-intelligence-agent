import streamlit as st

APP_PAGES = [
    "Home",
    "Research Q&A",
    "Paper Search",
    "Compare Papers",
    "Research Gaps",
    "Literature Review",
]


def render_sidebar() -> str:

    with st.sidebar:

        st.title("Research Intelligence Agent")

        st.caption("Evidence-grounded analysis " "of software-testing research")

        st.divider()

        page = st.radio(
            "Navigation",
            APP_PAGES,
            index=0,
        )

        st.divider()

        st.markdown("""
            **Research Domain**

            Large Language Models for
            Automated Software Test Generation
            """)

        st.caption("Current corpus: 10 research papers")

    return page
