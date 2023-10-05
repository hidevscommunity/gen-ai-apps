import streamlit as st
from helper_func import utils
from streamlit_lottie import st_lottie
import datetime as dt
from helper_func import db

st.set_page_config(
    page_title="PharmaAssist",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.form("signup_form", clear_on_submit=False):
    st.subheader("Receive Curated GPPQE Questions In Your Inbox 😃")

    col1, col2 = st.columns([2, 1])

    with col2:
        lottie_comment = utils.load_lottiefile("animations/coffee.json")

        st_lottie(
            lottie_comment,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",  # medium ; high
            height=100,
            width=None,
            key=None,
        )
    col1.write(
        "**PharmAssist** sends you weekly updates of Curated Questions in your inbox."
    )
    col1.write("**Sign Up to Join the Waitlist** 👇")

    st.write("**Name**")
    name = st.text_input("name", label_visibility="collapsed")

    st.write("**Email**")
    email = st.text_input("email", label_visibility="collapsed")

    submit = st.form_submit_button("Sign Up", type="primary")


if submit:
    name = name.strip().title()
    email = email.strip()
    if utils.validate_email(email):
        details = {"name": name.title(), "email": email, "created_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        response = db.update_user(details)
        if response:
            st.success("You have been added to the waitlist")
            st.balloons()
        else:
            st.error("You are already registered")
    else:
        st.error("Invalid Email Address")
