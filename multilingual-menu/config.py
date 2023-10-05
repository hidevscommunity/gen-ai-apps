
import streamlit as st
PAT = st.secrets["PAT"]
USER_ID =st.secrets["USER_ID"]
APP_ID = st.secrets["APP_ID"]
MODEL_ID = st.secrets["MODEL_ID"]

IMAGE_PAT = st.secrets["IMAGE_PAT"]
IMAGE_USER_ID = st.secrets["IMAGE_USER_ID"]
IMAGE_APP_ID = st.secrets["IMAGE_APP_ID"]
IMAGE_MODEL_ID = st.secrets["IMAGE_MODEL_ID"]
IMAGE_MODEL_VERSION_ID = st.secrets["IMAGE_MODEL_VERSION_ID"]


template = """Question: {question}
Answer: Let's think step by step."""