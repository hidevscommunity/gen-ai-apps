import streamlit as st

def create_chat_area(chat_history):
    for i, chat in enumerate(chat_history):
        if chat['role'] == 'user':
            message = st.chat_message("user")
            message.write(chat['content'], unsafe_allow_html=True)
        if chat['role'] == 'assistant':
            with st.chat_message("assistant"):
                st.write(chat['content'], unsafe_allow_html=True)
                with st.expander("Show Video"):
                    st.info('Click one of the references in the answer to display the corresponding video segment.', icon="ℹ️")
                    st.write(chat['vid_content'], unsafe_allow_html=True)
