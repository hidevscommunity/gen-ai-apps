import streamlit as st
from transcribe_and_summarize import summarize
if "summarize" not in st.session_state:
    st.session_state["summarize"]=0
def summary(context):
    if st.session_state["curr_data"]["transcribed"]:
        _, id = st.session_state["curr_data"]["transcribed"]
    else:
        st.write("Please wait for transcription to complete")
        return
        
    if not st.session_state["curr_data"]["summarized"]:
        with st.spinner("Generating summary of account..."):
            st.subheader("Summary: ")
            summary = summarize(id, context)
            st.success("Summary generated")
            st.session_state["curr_data"]["summarized"]=summary
            st.write(summary)
    else:
        st.subheader("Summary: ")
        summary=st.session_state["curr_data"]["summarized"]
        st.write(summary)
            
summary(st.session_state["curr_data"]['context'])