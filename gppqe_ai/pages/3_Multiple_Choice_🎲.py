import streamlit as st
from helper_func.llm_model import *
from helper_func.text_utils import clinical_options, objective_question_prompt, output_parser, health_act_options
from streamlit_extras.switch_page_button import switch_page

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

    topic = "Select clinical disorder category" if sel_dis == "Standard Treatment Guidelines" else "Select health act section"
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

    st.write("Question Type")
    sel_type = st.selectbox(
        "quiz_type",
        options=["Multiple-choice", "True/False"],
        label_visibility="collapsed",
    )

    st.write("Number of questions")
    num_questions = st.slider(
        "num_mcqs", min_value=5, max_value=10, value=7, label_visibility="collapsed"
    )

    # Footer or contact information
    if st.button("Click here for any inquiries 🧑🏽‍🔧", type="primary", ):
        switch_page("contact 📧")
        
if "discipline_type" not in st.session_state:
    st.session_state["discipline_type"] = ""

if st.session_state["discipline_type"] != sel_dis:
    if sel_dis == "Standard Treatment Guidelines":
        text_data = get_pdf_text("data/stg.pdf")
        get_embeddings(text_data, document="stg")

    elif sel_dis == "Public Health Act":
        text_data = get_pdf_text("data/public_health_act_2012.pdf")
        get_embeddings(text_data, document="pha")

    st.session_state["discipline_type"] = sel_dis

# Main
st.title("Multiple Choice Quiz 🎰")
st.toast("This is a demo of the PharmaAssist AI. Please use it as a learning tool.")

user_question = ""
ai_question = ""
chat_history = []
if st.button("Generate quiz", type="primary"):
    user_question = (
        f"Ask me {num_questions} random question on the following topics{sel_topics}"
    )
    with st.spinner("Generating Questions"):
        conversationChain, mermory = get_conversation_chain(
            st.session_state["vectorStore"],
            objective_question_prompt,
            input_key="question",
        )
        mermory.clear()
        response = conversationChain(
            {
                "question": user_question,
                "chat_history": chat_history,
                "option_type": sel_type,
            }
        )
    chat_history.append(response["answer"])
    ai_question = response["answer"]
    parsed_output = output_parser.parse(response["answer"])


# Initialize a dictionary to store selected answers
selected_answers = {}

if ai_question:
    st.session_state["parsed_output"] = parsed_output

if "parsed_output" not in st.session_state:
    st.session_state["parsed_output"] = {}

# Streamlit app layout

if st.session_state["parsed_output"]:
    parsed_output = st.session_state["parsed_output"]
    for i, question in enumerate(parsed_output["Questions"]):
        st.write(f"Question {i + 1}: {question}")
        options = parsed_output["Options"][i]
        selected_option = st.radio(
            "Select your answer:", options, key=f"option_{i}", horizontal=True
        )
        selected_answers[i] = selected_option

    # Check answers
    score = 0
    for i, selected_option in selected_answers.items():
        if selected_option == parsed_output["Answers"][i]:
            score += 1

    if st.button("Submit answers", type="primary"):
        st.success(f"You scored {score} out of {len(parsed_output['Questions'])}")

        # Display correct answers
        st.subheader("Correct Answers:")
        for i, answer in enumerate(parsed_output["Answers"]):
            st.write(
                f"Question {i + 1}: {parsed_output['Questions'][i]} - Correct Answer: {parsed_output['Answers'][i]}"
            )

else:
    st.info("💡 Click generate quiz to get multiple choice questions")
