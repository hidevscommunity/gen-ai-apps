import streamlit as st
from pathlib import Path
import base64
from visualisations import *
from processing import *

st.set_page_config(page_title='TalkToMe', page_icon='🌍')

header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
    img_to_bytes("header.png")
)
st.markdown(
    header_html, unsafe_allow_html=True,
)

st.title("About")
st.subheader("About TalkToMe")
st.write("""
TalkToMe is designed to provide language learners an interactive platform to practice speaking in their target language. The bot uses a combination of advanced natural language processing algorithms to simulate a conversation, provide feedback on your proficiency, grammar, and vocabulary usage.

**Note:** This tool is intended for practice and should not be used as a sole method for learning a language. The bot's feedback is based on algorithms and may not always reflect human judgment.

If you have any feedback or suggestions, please let me know.
""")
st.write("TalkToMe - Your Language Learning Assistant. Created by a Language Enthusiasts for Language Learners.")