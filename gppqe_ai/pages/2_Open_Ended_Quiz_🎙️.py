import streamlit as st
from helper_func.llm_model import *
from helper_func.text_utils import (
    clinical_options,
    subjective_question_prompt,
    subject_answer_prompt,
    health_act_options,
)
from streamlit_extras.switch_page_button import switch_page
from helper_func.transcribe import get_transcript
from audio_recorder_streamlit import audio_recorder

# Page settings
st.set_page_config(
    page_title="PharmaAssist",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
with st.sidebar:
    st.header("Edit question format")

    st.write("**Select document type**")
    sel_dis = st.selectbox(
        "quiz_type",
        options=["Standard Treatment Guidelines", "Public Health Act"],
        label_visibility="collapsed",
    )

    topic = (
        "Select clinical disorder category"
        if sel_dis == "Standard Treatment Guidelines"
        else "Select health act section"
    )
    st.write(f"**{topic}**")
    sel_topics = st.multiselect(
        "topics",
        default="Disorders_of_the_GIT"
        if sel_dis == "Standard Treatment Guidelines"
        else "Tobacco Control Measures",
        options=clinical_options
        if sel_dis == "Standard Treatment Guidelines"
        else health_act_options,
        placeholder="Select a topic",
        label_visibility="collapsed",
    )

    # Footer or contact information
    if st.button(
        "Click here for any inquiries 🧑🏽‍🔧",
        type="primary",
    ):
        switch_page("contact 📧")

if "discipline_type" not in st.session_state:
    st.session_state["discipline_type"] = ""

if st.session_state["discipline_type"] != sel_dis:
    if sel_dis == "Standard Treatment Guidelines":
        with st.spinner("Loading Standard Treatment Guidelines..."):
            text_data = get_pdf_text("data/stg.pdf")
            get_embeddings(text_data, document="stg")

    elif sel_dis == "Public Health Act":
        with st.spinner("Loading Public Health Act..."):
            text_data = get_pdf_text("data/public_health_act_2012.pdf")
            get_embeddings(text_data, document="pha")

    st.session_state["discipline_type"] = sel_dis


# Main

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "ai_question" not in st.session_state:
    st.session_state["ai_question"] = ""

if "recorded_answer" not in st.session_state:
    st.session_state["recorded_answer"] = ""

st.title("Open Ended Quiz 🎙️")
st.toast("This is a demo of the PharmaAssist AI. Please use it as a learning tool.")


col1, col2, col3 = st.columns([1, 1, 3])

user_question = ""
ai_question = ""
chat_history = []
if col1.button("Generate quiz", type="primary"):
    user_question = f"Ask me any random question on {sel_topics}"

    with st.spinner("Generating open-ended question"):
        conversationChain, mermory = get_conversation_chain(
            st.session_state["vectorStore"],
            subjective_question_prompt,
            input_key="question",
        )
        mermory.clear()
        response = conversationChain(
            {"question": user_question, "chat_history": chat_history}
        )

    chat_history.append(response["answer"])
    st.session_state["ai_question"] = response["answer"]

if col2.button("Reset Chat"):
    st.session_state["messages"] = []
    st.session_state["ai_question"] = ""


with col3:
    if st.session_state["ai_question"] != "":
        col1, col2, col3 = st.columns(3)
        with col1:
            audio_bytes = audio_recorder("Record your answer", icon_size="2x", pause_threshold=3)  
        
            if audio_bytes:    
                col2.audio(audio_bytes, format="audio/mpeg")

                if col3.button("Submit recording"):
                    with open("data/recording.wav", "wb") as f:
                        f.write(audio_bytes)
    
                    with st.spinner("Transcribing your answer (This may take longer than usual)..."):
                        transcript = get_transcript("data/recording.wav")
                        st.session_state["recorded_answer"] = transcript.text
                        if os.path.exists("data/recording.wav"):
                            os.remove("data/recording.wav")
                        audio_bytes = None
                    st.toast("Transcibing completed")
                    st.balloons()

# Display messages on rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_question:
    with st.chat_message("assistant"):
        st.markdown(st.session_state["ai_question"])
    st.session_state["messages"].append(
        {"role": "assistant", "content": st.session_state["ai_question"]}
    )

if not st.session_state["ai_question"]:
    st.info("💡 Click generate quiz to start the ChatBot")

prompt_placeholder = (
    "Answer the questions here..."
    if st.session_state["ai_question"] != ""
    else "Click the generate quiz button to get a quiz"
)

recorded_answer = st.session_state["recorded_answer"]
chat_answer = st.chat_input(
        prompt_placeholder, disabled=st.session_state["ai_question"] == ""
    )

answer = chat_answer if recorded_answer == "" else recorded_answer
if answer:
    with st.chat_message("user"):
        st.markdown(answer)
    st.session_state["messages"].append({"role": "user", "content": answer})

    with st.spinner("Generating response..."):
        conversationChain, mermory = get_conversation_chain(
            st.session_state["vectorStore"], subject_answer_prompt, input_key="question"
        )
        mermory.clear()
        answer_history = []

        response = conversationChain(
            {
                "question": st.session_state["ai_question"],
                "chat_history": answer_history,
                "student_answer": answer,
            }
        )
    answer_history.append(response["answer"])
    with st.chat_message("assistant"):
        st.markdown(response["answer"])
    st.session_state["messages"].append(
        {"role": "assistant", "content": response["answer"]}
    )
    st.session_state["recorded_answer"] = ""
    st.toast("Response generated")
    st.balloons()