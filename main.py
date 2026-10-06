import streamlit as st

st.set_page_config(
    page_title="Syariah Court Divorce Proceedings",
    page_icon="⚖️",
    layout="centered",
)

home = st.Page("pages/01_home.py", title="Home", icon="💬", default=True)
about = st.Page("pages/02_about.py", title="About", icon="ℹ️")
resources = st.Page("pages/03_resources.py", title="Resources", icon="📚")

nav = st.navigation([home, about, resources])

with st.sidebar:
    st.caption(
        "This site provides general information only and is not legal advice. "
        "For advice on your situation, consult a lawyer or the Syariah Court."
    )

nav.run()
