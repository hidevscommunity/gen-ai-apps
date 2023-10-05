import os
import streamlit as st
from langchain.llms import Replicate

os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

def text2image(prompt: str,heigh: int,width: int):
    text2image = Replicate(
        # stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf
        model="stability-ai/sdxl:d830ba5dabf8090ec0db6c10fc862c6eb1c929e1a194a5411852d25fd954ac82",
        input={"height": heigh,"width":width},
    )
    image_output = text2image(prompt)
    return image_output