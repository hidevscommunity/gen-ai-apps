import streamlit as st
from streamlit_features import main
from tempfile import TemporaryDirectory

st.header("ResuBot")
st.subheader("revising user's resume to match the requirements and expectations of a specific job website url")
st.text("1.upload your resume")
st.text("2.input job website url")
st.text("3.click generate")
st.text("4.download")
st.text("")

# if check_key():
#     with TemporaryDirectory() as user_path:
#         main(st.session_state["api_key"],user_path)

with TemporaryDirectory() as user_path:
    st.session_state["api_key"] = st.secrets['api_key']
    main(st.session_state["api_key"],user_path)