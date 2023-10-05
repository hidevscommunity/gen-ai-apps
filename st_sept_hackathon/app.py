import streamlit as st
from utils_clarifai.text import query_gpt4
from utils_clarifai.image import save_image, describe_image

st.title("Integrating text2text and img2text LLMs (POC)")

col1, col2 = st.columns(2)

with col1:
    input_text = st.text_area("**Question**")

    if input_text != "":
        reply = query_gpt4(input_text)
        st.write(reply)

with col2: 
    uploaded_file = st.file_uploader("**Add Pic**", type= ['png', 'jpg'])
    if uploaded_file is not None:
        # Get actual image file
        bytes_data = save_image(uploaded_file)
        st.image(bytes_data)
        caption = describe_image(bytes_data)
        st.write(caption)