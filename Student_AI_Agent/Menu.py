import streamlit as st
import os
st.set_page_config(
    page_title="Student AI Agent",
    page_icon="👋",
)

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    # Student AI Agent
    #### Your AI Agent that solves questions including homework, exam, interview, and general assistants
    **👈 Select a demo from the sidebar** to see some examples of our AI agents
"""
)
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
os.environ['Assembly_AI_key'] = st.secrets['Assembly_AI_key']