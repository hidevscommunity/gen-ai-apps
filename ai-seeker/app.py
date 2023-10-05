# Import required libraries
import streamlit as st
import youtube
import confluence
import modJira
import time
import similarity
import ingest

atlassian_username = st.secrets["atlassian_username"]
atlassian_password = st.secrets["atlassian_password"]
# global transcript_result
# transcript_result = ""

# Set page configuration and title for Streamlit
st.set_page_config(page_title="AI-Seeker", page_icon="📼", layout="wide")

# Add header with title and description
st.markdown(
    '<p style="display:inline-block;font-size:40px;font-weight:bold;">AI-Seeker</p> <p style="display:inline-block;font-size:16px;">AI-Seeker is a web-app tool that utilizes APIs to extract text content from YouTube, Confluence and Jira. It incorporates Llama-2-7B-Chat-GGML model with Langchain to provide users with a summary and query-based smart response depending on the content of the media source.<br><br></p>',
    unsafe_allow_html=True
)

txtInputBox = "YouTube"


with st.sidebar.title("Configuration"):
    usecase = st.sidebar.selectbox("Select Media Type:",("YouTube", "Confluence", "Jira"))
    if usecase == "YouTube":
        txtInputBox = "Enter ID of YouTube Video"
        default_value = "Y8Tko2YC5hA"
    elif usecase == "Confluence":
        txtInputBox = "Enter ID of your Confluence Page"
        default_value = "393217"
    elif usecase == "Jira":
        txtInputBox = "Enter the name of your JIRA Project"
        default_value = "jira_test"

    video_id = st.sidebar.text_input(txtInputBox,value=default_value)

    strTranscript = ""
    training_status = "yet_to_start"
    btnTranscript = st.sidebar.button("Transcript")
    btnSummary = st.sidebar.button("Summary")
    btnTrain = st.sidebar.button("Train")
    if btnTrain:
        with st.spinner("Training in Progress..."):
            ingest.main()

    query = st.sidebar.text_input('Enter your question below:', value="What is Python?")
    btnAsk = st.sidebar.button("Query")

    btnClear = st.sidebar.button("Clear Data")
    if btnClear:
        st.session_state.clear()

def fnJira():
    st.info("Transcription")

    if btnTranscript:

        if 'transcript_result' not in st.session_state:
            st.session_state['transcript_result'] = modJira.get_details(video_id, atlassian_username, atlassian_password)
            transcript_result = st.session_state['transcript_result']
            st.dataframe(transcript_result)
    else:
        if 'transcript_result' in st.session_state:
            transcript_result = st.session_state['transcript_result']
            st.dataframe(transcript_result)

    st.info("Query")
        
    if btnAsk:
        with st.spinner(text="Retrieving..."):
            if 'transcript_answer' not in st.session_state:
                answer = modJira.ask_question(query)
                st.session_state['transcript_answer'] = answer
                #st.success(answer)
            if 'transcript_answer' in st.session_state:
                answer = st.session_state['transcript_answer']

            st.success(answer)

    else:
        if 'transcript_answer' in st.session_state:
            answer = st.session_state['transcript_answer']

            st.success(answer)


def fnConfluence():
    st.info("Transcription")

    if btnTranscript:

        if 'transcript_result' not in st.session_state:
            st.session_state['transcript_result'] = confluence.transcript(video_id,atlassian_username, atlassian_password)
        transcript_result = st.session_state['transcript_result']
        st.markdown(f"<div style='height: 100px; overflow-y: scroll;'>{transcript_result}</div>", unsafe_allow_html=True)
    else:
        if 'transcript_result' in st.session_state:
            transcript_result = st.session_state['transcript_result']
            st.markdown(f"<div style='height: 100px; overflow-y: scroll;'>{transcript_result}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        # with col12:
        st.info("Summary")
        if btnSummary:
            if 'transcript_summary' not in st.session_state:
                with st.spinner(text="Retrieving..."):
                    st.session_state['transcript_summary'] = confluence.summarize()
                    summary = st.session_state['transcript_summary'] 
                    st.success(summary)
        else:
            if 'transcript_summary' in st.session_state:
                summary = st.session_state['transcript_summary']
                st.success(summary)

    with col2:
        st.info("Query")
        
        if btnAsk:
            with st.spinner(text="Retrieving..."):
                if 'transcript_answer' not in st.session_state:
                    answer = confluence.ask_question(query)
                    st.session_state['transcript_answer'] = answer
                    #st.success(answer)
                if 'transcript_answer' in st.session_state:
                    answer = st.session_state['transcript_answer']

                st.success(answer)

        else:
            if 'transcript_answer' in st.session_state:
                answer = st.session_state['transcript_answer']

                st.success(answer)

def fnYoutube():
    st.info("Transcription")

    if btnTranscript:

        if 'transcript_result' not in st.session_state:
            st.session_state['transcript_result'] = youtube.audio_to_transcript(video_id)
        transcript_result = st.session_state['transcript_result']
        st.markdown(f"<div style='height: 100px; overflow-y: scroll;'>{transcript_result}</div>", unsafe_allow_html=True)
    else:
        if 'transcript_result' in st.session_state:
            transcript_result = st.session_state['transcript_result']
            st.markdown(f"<div style='height: 100px; overflow-y: scroll;'>{transcript_result}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        # with col12:
        st.info("Summary")
        if btnSummary:
            if 'transcript_summary' not in st.session_state:
                with st.spinner(text="Retrieving..."):
                    st.session_state['transcript_summary'] = youtube.summarize()
                    summary = st.session_state['transcript_summary'] 
                    st.success(summary)
        else:
            if 'transcript_summary' in st.session_state:
                summary = st.session_state['transcript_summary']
                st.success(summary)

    with col2:
        st.info("Query")
        
        if btnAsk:
            with st.spinner(text="Retrieving..."):
                if 'transcript_answer' not in st.session_state:
                    answer = youtube.ask_question(query)
                    st.session_state['transcript_answer'] = answer
                    #st.success(answer)
                if 'transcript_answer' in st.session_state:
                    answer = st.session_state['transcript_answer']

                st.success(answer)

                transcript_start_time, transcript_end_time = similarity.similarity(strQuery=answer)

                st.video(f"https://www.youtube.com/embed/{video_id}", format="video/mp4", start_time=int(transcript_start_time))

        else:
            if 'transcript_answer' in st.session_state:
                answer = st.session_state['transcript_answer']

                st.success(answer)

                transcript_start_time, transcript_end_time = similarity.similarity(strQuery=answer)

                st.video(f"https://www.youtube.com/embed/{video_id}", format="video/mp4", start_time=int(transcript_start_time))

if usecase == "YouTube":
    fnYoutube()
elif usecase == "Confluence":
    fnConfluence()
elif usecase == "Jira":
    fnJira()

# Hide Streamlit header, footer, and menu
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
#"""footer {visibility: hidden;}
#    header {visibility: hidden;}"""

# Apply CSS code to hide header, footer, and menu
st.markdown(hide_st_style, unsafe_allow_html=True)