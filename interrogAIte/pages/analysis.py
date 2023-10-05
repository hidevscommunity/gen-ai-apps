from transcribe_and_summarize import transcribe,summarize
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
if "curr_data" not in st.session_state:
    st.session_state['curr_data']={}
if "analyze" not in st.session_state:
    st.session_state['analyze']=0
if "transcribed" not in st.session_state["curr_data"]:
    st.session_state["curr_data"]["transcribed"]=0
if "summarized" not in st.session_state["curr_data"]:
    st.session_state["curr_data"]["summarized"]=0
if "summarize" not in st.session_state:
    st.session_state["summarize"]=0
def toggle():
    st.session_state["summarize"]= not st.session_state["summarize"]
def analyze(audio_file, context):
    grid = st.columns(3)
    placeholder = st.empty()
    if not st.session_state["curr_data"]["transcribed"]:
        with st.spinner("Generating transcription..."):
            st.subheader(f"Transcript of testimony by {st.session_state['curr_data']['Name']}")
            transcription, id = transcribe(audio_file)
            
            st.success("Transcription generated")
            st.session_state["curr_data"]["transcribed"]=[transcription, id]
            # st.write(transcription)
            for snippet in transcription:
                speaker = list(snippet.keys())[0]
                with st.chat_message(speaker):
                    st.write(snippet[speaker])
            st.write("\n")
    else:
        with placeholder.container():
            transcription, id = st.session_state["curr_data"]["transcribed"]
            st.subheader(f"Transcript of testimony by {st.session_state['curr_data']['Name']}")
            for snippet in transcription:
                speaker = list(snippet.keys())[0]
                with st.chat_message(speaker):
                    st.write(snippet[speaker])
                st.write("\n")
    transcription, id = st.session_state["curr_data"]["transcribed"]
        
    
        # placeholder=placeholder.empty()
        # with placeholder.container():
        #     if not st.session_state["curr_data"]["summarized"]:
        #         with st.spinner("Generating summary of account..."):
        #             st.subheader("Summary: ")
        #             summary = summarize(id, context)
        #             st.success("Summary generated")
        #             st.session_state["curr_data"]["summarized"]=summary
        #             st.write(summary)
        #     else:
        #         st.subheader("Summary: ")
        #         summary=st.session_state["curr_data"]["summarized"]
        #         st.write(summary)
        # st.session_state["summarize"]=0
if st.session_state["summarize"]:
        switch_page("summary")            
analyze(st.session_state["curr_data"]['audio_bytes'],st.session_state["curr_data"]['context'])
