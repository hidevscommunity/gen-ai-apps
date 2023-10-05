import streamlit as st
import requests
from PIL import Image
import time

st.set_page_config(page_title="Grammar Corrector", page_icon="favicon.png")

API_URL = "https://api-inference.huggingface.co/models/grammarly/coedit-large"
headers = {"Authorization": st.secrets["auth_token"]}

def clear_input():
    st.session_state["input_text"] = ""

def break_line():
    html_str = f"""
    <br>
    """
    st.markdown(html_str, unsafe_allow_html=True)
	
st.markdown(
    """
    <style>
    .css-q8sbsg p {
        font-size: 20px;
		font-weight: 600;
    }
    </style>""",unsafe_allow_html=True)

image = Image.open('CoEdit.png')
st.image(image)
break_line()

instructions = {
	"Fix the grammar": "Please correct the grammatical errors from the following paragraph: ", 
	"Paraphrase": "Please paraphrase the following paragraph: ",
	"Summarize": "Please summarize the following paragraph: "}

option = st.selectbox('Select Instruction:', options= list(instructions.keys()))
input_text = st.text_area("Input: (Max Characters = 1000)", max_chars=1000, key='input_text')

col1, col2 = st.columns([2,15])
with col1:
	submit_button = st.button("Submit", type="primary")
with col2:
	clear_all_btn= st.button(label="Clear All", on_click=clear_input, type="secondary")

break_line()
if submit_button:
	with st.spinner('Processing...'):
	        data = {"inputs": instructions[option]+ f"\"{input_text}\"", "wait_for_model": True, "parameters": {"do_sample": False, "max_new_tokens":250}}
	        while True:            
	            response = requests.post(API_URL, headers=headers, json=data)
	            if 'error' in response.json():
	                time.sleep(15)
	            elif 'generated_text' in response.json()[0]:
	                st.markdown("""<p style="font-weight: 600; font-size: 20px;">Output: (Max tokens = 250)</p>""", unsafe_allow_html=True)
	                st.markdown(f"""<div style="text-align: justify; color: black; font-weight: 550; line-height: 1.35; padding: 18px; border-radius: 0.5rem; background-color: #FFFFFF;">{response.json()[0]["generated_text"]}</div>""", unsafe_allow_html=True)
	                break
