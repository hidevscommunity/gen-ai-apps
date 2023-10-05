import streamlit as st
from langchain.llms import Replicate
from replicate_text_image import text2image

pic_address = ''

st.title("🦜️🔗 LangChain text-to-image")


with st.sidebar:
    st.header("Input：")

    width = st.slider('width', 240, 1024,1024)
    height = st.slider('height',240, 1024,1024)
    prompt = st.text_area("Input image prompt：",max_chars=200)
    button = st.button('create')
    if button:
        if prompt:
                with st.spinner("Wait a moment..."):
                    pic_address = text2image(prompt=prompt,heigh=height,width=width)
        else:
            st.info("please input prompt")

if pic_address:
    st.image(pic_address)



