import uuid
import streamlit as st
import os.path
import tempfile
import numpy as np
import openai
import wavio as wv
from utils import *
from qa_model import generate_response
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate

template = """Ask meaningful and relatable follow up questions to the user based on the context that the user provides.
Ask questions related to that context, be precise.
Current conversation:
{history}
Human: {input}
AI Assistant:"""

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="")

st.title("Interview Question Generator")

st.subheader("Upload Resume, Job Description or Candidate Audio")

options = st.multiselect(
    'Choose from where you want questions to be generated',
    ['Resume', 'JD', 'Candidate Audio', 'Resume and JD'])

if 'Resume' in options:
    resume = st.file_uploader("Upload resume", accept_multiple_files=False, type=['pdf', 'docx'])
if 'JD' in options:
    jd = st.file_uploader("Upload the job description", accept_multiple_files=False, type=['pdf', 'docx'])

if 'Candidate Audio' in options:
    uploaded_file = st.file_uploader("Choose a sound file", type=["wav", "mp3", "m4a"])

if 'Resume and JD' in options:
    resume = st.file_uploader("Upload resume", accept_multiple_files=False, type=['pdf', 'docx'])

    jd = st.file_uploader("Upload the job description", accept_multiple_files=False, type=['pdf', 'docx'])

button = st.button("Submit")


# For question answering
q_a_container = st.container()


with q_a_container:
    if button:
        with st.spinner("Generating questions..."):
            if 'Resume' in options:
                if resume:
                    text = get_file_text(resume)
                    expander = st.expander("View parsed resume text", expanded=False)
                    expander.code(text)
                    messages = get_resume_initial_message(text)
                    message1 = get_resume_actionable_insights_initial_message(text)
                    message2 = get_user_work_exp(text)
                    res = generate_response(messages)
                    # res1 = generate_response(message1)
                    # res2 = generate_response(message2)

                    st.subheader("Ace your interview!")
                    # Split the text into a list of points
                    points = res.strip().split('\n')[2:]
                    print(points)
                    print("*"*10)
                    for i, point in enumerate(points, start=1):
                        print(point)
                        st.write(point)

                        PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
                        conversation = ConversationChain(
                            prompt=PROMPT,
                            llm=llm,
                            verbose=True,
                            memory=ConversationBufferMemory(ai_prefix="AI Assistant"),)
                        
                        with st.spinner("typing..."):
                                    for _ in range(2):
                                        try:
                                            input_text=None
                                            while input_text is None:
                                                input_text = st.text_input("Enter your answer: ", key=str(uuid.uuid4()))
                                            print("*"*10)
                                            print(input_text)
                                            if input_text:
                                                res = conversation.predict(input=input_text)
                                                print(res)
                                                st.write(res)

                                        except Exception as e:
                                            print(e)
                                            st.write("Sorry, I didn't get that. Please try again.")


            if 'JD' in options:
                if jd:
                    text = get_file_text(jd)
                    expander = st.expander("View job description", expanded=False)
                    expander.code(text)
                    messages = get_jd_initial_message(text)
                    res = generate_response(messages)
                    st.subheader("Generated questions from job description")
                    expander = st.expander("View Questions", expanded=True)
                    expander.write(res)
            if 'Candidate Audio' in options:
                if uploaded_file:
                    file_name = uploaded_file.name
                    print(file_name.split(".")[-1])
                    # Load the sound file
                    if file_name.split(".")[-1] in ["wav", "mp3"]:
                        temp_dir = tempfile.mkdtemp()
                        variable = np.random.randint(1111, 1111111)
                        file_name = st.text_input('Enter file name', fr'recording{variable}.m4a')
                        temp_path = os.path.join(temp_dir, file_name)
                        # audio_in = AudioSegment.from_file(uploaded_file.name, format="m4a")
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getvalue())

                        audio_file = open(temp_path, "rb")
                        with st.spinner("Transcribing Audio..."):
                            candiate_notes = openai.Audio.translate("whisper-1", audio_file)["text"]
                        # print(internship_notes)

                        expander = st.expander("The transcription of the uploaded audio:", expanded=False)
                        expander.code(candiate_notes)
                        messages = get_audio_initial_message(candiate_notes)
                        res = generate_response(messages)
                        st.subheader("Generated questions from candidate audio")
                        expander = st.expander("View Questions", expanded=True)
                        expander.write(res)

            if 'Resume and JD' in options:
                if resume:
                    text = "Resume \n\n"
                    text = text + get_file_text(resume)
                    text = text + "\nJob Description \n\n"
                    text = text + get_file_text(jd)
                    expander = st.expander("View parsed resume and JD text", expanded=False)
                    expander.code(text)
                    messages = get_resume_and_JD_initial_message(text)
                    res = generate_response(messages)
                    st.subheader("Generated questions from resume and job description")
                    expander = st.expander("View Questions", expanded=True)
                    expander.write(res)
