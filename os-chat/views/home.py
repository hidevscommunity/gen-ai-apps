import streamlit as st

from handlers.userinput import handle_userinput
from .sidebar import sidebar


def home():
    # initial session_state in order to avoid refresh
    if 'conversation' not in st.session_state:
        st.session_state.conversation = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    st.header('Chat based on open-source documentation! :globe_with_meridians:')
    user_question = st.text_input('Ask a question about your dvc pipeline:')

    if user_question:
        handle_userinput(user_question)

    sidebar()
