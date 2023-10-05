import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_lottie import st_lottie
from helper_func import utils

st.set_page_config(
    page_title="PharmaAssist",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Page title and description
st.title("Pharmacist Licensure Exam Prep (PharmAssist) 👨🏽‍⚕️👩🏽‍⚕️")
st.markdown(
        """
        * Welcome to the Pharmacist Licensure Exam Prep App also known as PharmAssist
        * This app is designed to help pharmacists prepare for their licensure exam by providing **multiple choice quizzes** based on the **Ghanaian Standard Treatment Guidelines** and the **Public Health Act** using **OpenAI & LangChain**
        * We also use AI to provide **open-ended questions**
        * Finally you can have a **chat session** with the AI as a form of revision"""
)
st.toast("This is a demo of the PharmaAssist AI. Please use it as a learning tool.")
# Navigation options
col1, col2, col3 = st.columns(3)
if col1.button(
    "Get started with open ended quiz assessment",
    type="primary",
    use_container_width=True,
):
    switch_page("open ended quiz 🎙️")
if col2.button(
    "Answer some multiple choice questions",
    type="primary",
    use_container_width=True,
):
    switch_page("multiple choice 🎲")

if col3.button(
    "Study the learning material",
    type="primary",
    use_container_width=True,
):
    switch_page("know your stuff 📖")
    
col1, col2 = st.columns(2)

with col1:
    # Features to come (Leaderboard, Newsletter, Flashcards)
    st.write("### Upcoming Features")
    st.write("Stay tuned for these exciting features coming soon:")
    st.write("- Leaderboard: Compete with others and track your progress.")
    st.write("- Flashcards: Study key topics with interactive flashcards.")

    # Footer or contact information
    if st.button("Click here for any inquiries or support 📭", type="primary", ):
        switch_page("contact 📧")
        
with col2:
    lottie_comment = utils.load_lottiefile("animations/doc_animation.json")
    st_lottie(
        lottie_comment,
        speed=1,
        reverse=False,
        loop=True,
        quality="high",  # medium ; high
        height=400,
        width=None,
        key=None,
    )