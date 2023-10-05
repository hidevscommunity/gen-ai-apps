import streamlit as st
from utils.session_state import executor_session_state
from utils.callback import CustomHandler
def execute(user_question):

    message_placeholder = st.container()
    try:
        executor_session_state()({
                "input":user_question
        },callbacks = [CustomHandler(message_placeholder = message_placeholder)])
        return True
    except:
        
        return False 
