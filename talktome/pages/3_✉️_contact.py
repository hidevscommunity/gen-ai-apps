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
st.title('Contact')
st.write("Have your say! Let me know what you think of the idea of this app and what features you would like to see in the future.")

contact_form = """
<form action="https://formsubmit.co/ad1b4a421f4310ed3e5b4d6903c79b2c" method="POST">
<input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email address" required>
     <textarea name="message" placeholder="Your message" required></textarea>
     <button type="submit">Send</button>
</form>
"""
st.markdown(contact_form, unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")