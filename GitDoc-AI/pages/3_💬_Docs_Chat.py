import streamlit as st
from app.components.chat import display_chat
from app.components.sidebar import sidebar
from app.langchain.chains import qa_chain
import pickle

def initialise():
    if 'knowledge_base' not in st.session_state:
        st.session_state['knowledge_base'] = None

def main():
    st.set_page_config(page_title="Docs Chat", page_icon="💬")
    sidebar()
    initialise()
    st.header('💬 Docs Chat')
    uploader = st.empty()
    uploaded_file = uploader.file_uploader("Upload your knowledge file from [Build Knowledge](/Build_Knowledge)", type=["pkl"])
    if uploaded_file is not None:
        vectorstore = pickle.load(uploaded_file)
        st.session_state['knowledge_base'] = vectorstore

    if st.session_state['knowledge_base'] is not None and uploaded_file is not None:
        display_chat(qa_chain)
        if st.session_state['messages']:
            uploader.empty()


if __name__ == "__main__":
    main()