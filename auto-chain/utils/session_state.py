import streamlit as st
last_saved_session_state = None
import os
def load_session_state():
    global last_saved_session_state
    last_saved_session_state = str(st.session_state.conversation_chain)
    
def init_session_state():
    if "url" not in st.session_state:
        st.session_state.url = {"clicked":False,"path":""}
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "chat_input" not in st.session_state:
        st.session_state.chat_input = None
    if "execute" not in st.session_state:
        st.session_state.execute = {"current_id":0,"ids":{}}
    if "files" not in st.session_state:
        st.session_state.files = []
    if "show_thought_process" not in st.session_state:
        st.session_state.show_thought_process = bool(os.getenv("SHOW_THOUGHTS"))
    if "max_iterations" not in st.session_state:
        st.session_state.max_iterations = 0
    if "executing" not in st.session_state:
        st.session_state.executing = False
    if "model" not in st.session_state:
        st.session_state.model = {}    
    if "conversation_chain" not in st.session_state:
        st.session_state.conversation_chain = {}
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "processed" not in st.session_state:
        st.session_state.processed = False
    if "agent_changed" not in st.session_state:
        st.session_state.agent_changed  = True
    if "df_changed" not in st.session_state:
        st.session_state.df_changed  = False
    if "agent" not in st.session_state:
        st.session_state.agent  = None
def reset_session_state():
    st.session_state.files = []
    st.session_state.chat_history = None
    st.session_state.conversation_chain = {}
    st.session_state.model = {}
    st.session_state.max_iterations = 0
    st.session_state.agent = None
    st.session_state.processed  = False
    st.session_state.agent_changed  = True
    st.session_state.df_changed  = True

    st.experimental_rerun()

def change_agent_session_state(option):
    st.session_state.agent = option
    st.session_state.chat_history = None
    st.session_state.agent_changed = False

def messages_session_state():
    return st.session_state.conversation_chain[st.session_state.agent]["messages"]
def executor_session_state():
    return st.session_state.conversation_chain[st.session_state.agent]["executor"]
def memory_session_state(agent):
    return st.session_state.conversation_chain[agent]["executor"].memory
def issues_session_state():
    return st.session_state.conversation_chain[st.session_state.agent]["issues"]
def true_key_session_state(starts_with):
    # Filter keys that start with "r-"
    filtered_keys = [key for key in st.session_state if key.startswith(starts_with)]
    # Find the key set to True
    result_key = None
    for key in filtered_keys:
        if st.session_state[key] is True:
            result_key = key
            break
    return result_key

def compare_session_state():
    if (str(st.session_state.conversation_chain)!=last_saved_session_state):
        return True
    return False