import streamlit as st
from documents import process_files
from utils.conversation_chain import get_conversation_chain
def st_process():
    upload_docs = st.file_uploader(
            "Upload your Documents here and click on 'Process'", accept_multiple_files=True,type=["txt","pdf","png","mp3","docx","csv","jpg"])
    process_button = st.button("Process",use_container_width=True,type='primary')



    if process_button:
        my_bar = st.progress(0, text="Operation in progress")
        with my_bar:
            process_files(upload_docs)
            c = get_conversation_chain()
            if (c):
                st.session_state.processed = True
                st.session_state.model = {
                    'id':'NEW',
                    'index':0,
                    'name':'',
                    'show':True
                }
                
                st.experimental_rerun()
            else:
                st.error('No Agents Avaialable')