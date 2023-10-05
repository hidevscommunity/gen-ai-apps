"""This is the Streamlit app file for Socrates v2.

Invoke locally with:
    poetry run streamlit run socrates_v2/app.py
"""

import streamlit as st

from socrates_v2 import chat_utils

st.set_page_config(page_title="Socrates 2.0", page_icon=":brain:")
st.title("Socrates 2.0 :brain:")

st.warning(":construction_worker: Socrates 2.0 is a work in progress.")

class SocratesChatbot:

    def main(self):
        chat_utils.show_sidebar()
        chat_utils.show_chat()

if __name__ == "__main__":
    obj = SocratesChatbot()
    obj.main()
