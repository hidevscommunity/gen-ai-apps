import streamlit as st
from helper_func.llm_model import *
from helper_func.text_utils import (
    clinical_options,
    chat_prompt,
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

    # topic = (
    #     "Select clinical disorder category"
    #     if sel_dis == "Standard Treatment Guidelines"
    #     else "Select health act section"
    # )
    # st.write(f"**{topic}**")
    # sel_topics = st.multiselect(
    #     "topics",
    #     default="Disorders_of_the_GIT"
    #     if sel_dis == "Standard Treatment Guidelines"
    #     else "Tobacco Control Measures",
    #     options=clinical_options
    #     if sel_dis == "Standard Treatment Guidelines"
    #     else health_act_options,
    #     placeholder="Select a topic",
    #     label_visibility="collapsed",
    # )

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

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "recorded_question" not in st.session_state:
    st.session_state["recorded_question"] = ""

st.title("Revise with AI 📖")
st.info(f"💡 Chat focus will be centered on the {sel_dis}. Change the document type at the sidebar.")
st.toast("This is a demo of the PharmaAssist AI. Please use it as a learning tool.")


col1, col2 = st.columns([1, 2])

if col1.button("Reset Chat"):
    st.session_state["chat_messages"] = []
    st.session_state["chat_history"] = []

with col2:
    col1, col2, col3 = st.columns(3)
    with col1:
        audio_bytes = audio_recorder(
            "Record your answer", icon_size="2x", pause_threshold=3
        )
        if audio_bytes:
            col2.audio(audio_bytes, format="audio/mpeg")
    
            if col3.button("Submit recording"):
                with open("data/recording.wav", "wb") as f:
                    f.write(audio_bytes)
                with st.spinner(
                    "Transcribing your answer (This may take longer than usual)..."
                ):
                    transcript = get_transcript("data/recording.wav")
                    st.session_state["recorded_question"] = transcript.text
                    if os.path.exists("data/recording.wav"):
                        os.remove("data/recording.wav")
                    audio_bytes = None
                st.toast("Transcibing completed")
                st.balloons()

# Display messages on rerun
for message in st.session_state["chat_messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


chat_question = st.chat_input(f"Let's get to know the {sel_dis}")
question = st.session_state["recorded_question"] if st.session_state["recorded_question"] != "" else chat_question

if question:
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state["chat_messages"].append({"role": "user", "content": question})

    with st.spinner("Generating response..."):
        conversationChain, mermory = get_conversation_chain(
            st.session_state["vectorStore"], chat_prompt, input_key="question"
        )
        mermory.clear()

        response = conversationChain(
            {
                "question": question,
                "chat_history": st.session_state["chat_history"],
                "student_answer": question,
            }
        )
    st.session_state["chat_history"].append(response["answer"])
    with st.chat_message("assistant"):
        st.markdown(response["answer"])
    st.session_state["chat_messages"].append(
        {"role": "assistant", "content": response["answer"]}
    )
    st.session_state["recorded_question"] = ""
    st.toast("Response generated")
    # st.balloons()
