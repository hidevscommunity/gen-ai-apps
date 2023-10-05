import streamlit as st
def func_show_source(source,documents):
    with st.sidebar:
        st.subheader(f"Source: {source}")
        for doc in documents:
            st.write(f"...{doc.page_content}...")
            st.write('----')

