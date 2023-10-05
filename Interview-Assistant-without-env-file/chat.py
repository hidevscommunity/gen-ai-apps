import streamlit as st
import os.path
import tempfile
import numpy as np
import openai
import wavio as wv

import utils
import qa_model

st.set_page_config(page_title="Interviewee.ai",
                   layout="centered",
                   initial_sidebar_state="auto")

st.title("Ace Your Interviews!💪🤯")


def initialize_session_state():
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I am your Hiring Manager today. Please provide your documents."}]

    if 'document' not in st.session_state:
        st.session_state['document'] = None

    if 'submit' not in st.session_state:
        st.session_state['submit'] = False

    if 'total_tokens' not in st.session_state:
        st.session_state['total_tokens'] = 0

    if 'total_cost' not in st.session_state:
        st.session_state['total_cost'] = 0


initialize_session_state()


def click_button():
    st.session_state['submit'] = True


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

with st.sidebar:
    st.markdown(
        "## How to use:\n"
        "1. Upload a Pdf, Doc or Audio file📄\n"
        "2. Start chatting with the bot🤖\n"
    )

    # st.subheader("Please upload Resume, Job Description or Candidate Audio")
    options = st.multiselect(
        label='Choose from the options below:',
        options=['Resume', 'JD', 'Resume and JD', 'Candidate Audio'],
        help='This is required for preparing you for your interviews!')

    if 'Resume' in options:
        resume = st.file_uploader("Upload resume", accept_multiple_files=False, type=['pdf', 'docx'])

    if 'JD' in options:
        jd = st.file_uploader("Upload the job description", accept_multiple_files=False, type=['pdf', 'docx'])

    if 'Resume and JD' in options:
        resume = st.file_uploader("Upload resume", accept_multiple_files=False, type=['pdf', 'docx'])
        jd = st.file_uploader("Upload the job description", accept_multiple_files=False, type=['pdf', 'docx'])

    if 'Candidate Audio' in options:
        uploaded_file = st.file_uploader("Choose a sound file", type=["wav", "mp3", "m4a"])

    button = st.button("Submit", on_click=click_button, disabled=st.session_state['submit'] == True)

    if button:
        st.success('Submission Successful! You may start chatting now.')
        with st.spinner("Reading your files"):
            if 'Resume' in options:
                if resume:
                    text = utils.extract_text(resume)
                    doc = utils.get_langchain_doc(text)
                    # expander = st.expander("View parsed resume doc", expanded=False)
                    # expander.code(doc)
                    st.session_state['document'] = [doc]
                    # messages = get_resume_initial_message(doc)

            if 'JD' in options:
                if jd:
                    text = utils.extract_text(jd)
                    doc = utils.get_langchain_doc(text)
                    # expander = st.expander("View job description", expanded=False)
                    # expander.code(doc)
                    st.session_state['document'] = [doc]

            if 'Candidate Audio' in options:
                if uploaded_file:
                    file_name = uploaded_file.name
                    print(file_name.split(".")[-1])
                    # Load the sound file
                    if file_name.split(".")[-1] in ["wav", "mp3"]:
                        temp_dir = tempfile.mkdtemp()
                        variable = np.random.randint(1111, 1111111)
                        # file_name = st.text_input('Enter file name', fr'recording{variable}.m4a')
                        temp_path = os.path.join(temp_dir, file_name)
                        # audio_in = AudioSegment.from_file(uploaded_file.name, format="m4a")
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getvalue())

                        audio_file = open(temp_path, "rb")
                        candidate_notes = openai.Audio.translate("whisper-1", audio_file)["text"]
                        doc = utils.get_langchain_doc(candidate_notes)
                        # expander = st.expander("The transcription of the uploaded audio:", expanded=False)
                        # expander.code(candidate_notes)
                        st.session_state['document'] = [doc]

            if 'Resume and JD' in options:
                if resume:
                    text = "Resume \n\n"
                    text = text + utils.extract_text(resume)
                    text = text + "\nJob Description \n\n"
                    text = text + utils.extract_text(jd)
                    doc = utils.get_langchain_doc(text)
                    expander = st.expander("View parsed resume and JD doc", expanded=False)
                    expander.code(doc)
                    st.session_state['document'] = [doc]

if query := st.chat_input("Enter query", disabled=not (st.session_state['submit'] and st.session_state['document'])):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

if st.session_state.messages[-1]["role"] != "assistant":
    if st.session_state['submit'] == True and st.session_state['document'] is not None:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ''
            doc = st.session_state['document']
            bot_answer, total_tokens, total_cost = qa_model.generate_langchain_response(doc, query)
            st.session_state['total_tokens'] += total_tokens
            st.session_state['total_cost'] += total_cost
            for item in bot_answer:
                full_response += item
                placeholder.markdown(full_response + "|")
            placeholder.markdown(full_response)

            # For the metrics
            # with st.sidebar:
            #     st.metric(label="Total Tokens", value=st.session_state['total_tokens'],
            #     )

            #     st.metric(label="Total Cost", value=f"${st.session_state['total_cost']}",
            #     )
            #     print(st.session_state['total_cost'])
            #     print(total_cost)
            st.session_state.messages.append({"role": "assistant", "content": bot_answer})
            # st.write(bot_answer)
