import streamlit as st

from src.ui.components.sidebar import (
    render_sidebar,
)

from src.ui.pages.compare_papers import (
    render_compare_papers_page,
)

from src.ui.pages.home import (
    render_home_page,
)

from src.ui.pages.literature_review import (
    render_literature_review_page,
)

from src.ui.pages.paper_search import (
    render_paper_search_page,
)

from src.ui.pages.research_gaps import (
    render_research_gaps_page,
)

from src.ui.pages.research_qa import (
    render_research_qa_page,
)


st.set_page_config(
    page_title="Research Intelligence Agent",
    page_icon="🔬",
    layout="wide",
)


page = render_sidebar()


if page == "Home":

    render_home_page()

elif page == "Research Q&A":

    render_research_qa_page()

elif page == "Paper Search":

    render_paper_search_page()

elif page == "Compare Papers":

    render_compare_papers_page()

elif page == "Research Gaps":

    render_research_gaps_page()

elif page == "Literature Review":

    render_literature_review_page()