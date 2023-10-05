import streamlit as st
def func_toggle_thought_process():
    st.session_state.show_thought_process = not st.session_state.show_thought_process
