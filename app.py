import streamlit as st
from multiapp import MultiApp
from apps import project_overview, content_based_filtering, collaborative_filtering

app = MultiApp()

css = """
<style>
dv.block-containe {
    padding: 1rem 1rem 5rem;
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

st.markdown("""
## Capstone Project
# Recommendation System
"""
, unsafe_allow_html=True)

# Add all your application here
app.add_app("Project Overview", project_overview.app)
app.add_app("Content Based Filtering", content_based_filtering.app)
app.add_app("Collaborative Filtering", collaborative_filtering.app)

# The main app
app.run('Navigation', 'radio')