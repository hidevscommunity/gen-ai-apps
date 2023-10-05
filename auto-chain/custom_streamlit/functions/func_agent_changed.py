import streamlit as st
from custom_streamlit.functions import func_stop_generating
from utils.session_state import executor_session_state
def func_agent_changed():
    ##Stop Generating Function
    max_iterations = executor_session_state().max_iterations
    executor_session_state().max_iterations = 0
    st.session_state['executing'] = False
    st.session_state.max_iterations = max_iterations
    st.session_state['execute']["ids"][st.session_state['execute']["current_id"]]["type"] = "Forced"
    
    st.session_state.agent_changed = True



