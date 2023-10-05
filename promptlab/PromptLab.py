### DISCLAIMER: I never said it was good code, it just somehow works 🫠
 
import streamlit as st
import pandas as pd
import openai
import base64
import os

from functions.show_data_info import show_data_info
from functions.improve_prompt import improve_prompt
from functions.run_prompts_app import run_prompts_app

image_path = os.path.dirname(os.path.abspath(__file__))

def set_page_config():
    st.set_page_config(
        page_title="PromptLab",
        page_icon=image_path+"/static/keboola.png",
        layout="wide"
        )

def display_logo():
    logo_image = image_path+"/static/keboola_logo.png"
    logo_html = f'<div style="display: flex; justify-content: flex-end;"><img src="data:image/png;base64,{base64.b64encode(open(logo_image, "rb").read()).decode()}" style="width: 150px; margin-left: -10px;"></div>'
    st.markdown(f"{logo_html}", unsafe_allow_html=True)

def set_api_key(): 
    OPENAI_API_KEY = st.sidebar.text_input('Enter your OpenAI API Key:',
        help= """
        You can get your own OpenAI API key by following these instructions:
        1. Go to https://platform.openai.com/account/api-keys.
        2. Click on the __+ Create new secret key__ button.
        3. Enter an identifier name (optional) and click on the __Create secret key__ button.
        """,
        type="password",
        )
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    openai.api_key = OPENAI_API_KEY
    return OPENAI_API_KEY

def get_uploaded_file(upload_option):
    if upload_option == 'Upload a CSV file':
        uploaded_file = st.sidebar.file_uploader("Choose a file")
        if 'uploaded_file' not in st.session_state:
            st.session_state['uploaded_file'] = None
        st.session_state['uploaded_file'] = uploaded_file

    elif upload_option == 'Use Demo Dataset':
        uploaded_file = image_path+"/data/sample_data.csv"
        if 'uploaded_file' not in st.session_state:
            st.session_state['uploaded_file'] = None
        st.session_state['uploaded_file'] = uploaded_file
    return st.session_state.get('uploaded_file')

def display_main_content(uploaded_file, openai_api_key):
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("The table has been successfully uploaded.")
        
        show_data_info(df)
        if st.session_state['uploaded_file'] is not None:
            st.dataframe(df, use_container_width=True)
        
        if not openai_api_key:
            st.warning("To continue, please enter your OpenAI API Key.")
            
        improve_prompt()
        run_prompts_app(df)
        st.text(" ")
        display_logo()
    else:
        st.markdown("""
        __Welcome to the PromptLab!__ 
                    
        🔄 Start by uploading your own CSV file or a provided demo dataset. After uploading the selected table, you should see a preview of your data.
                            """)

def main():
    set_page_config()
    display_logo()
    st.title("PromptLab 👩🏻‍🔬")

    openai_api_key = set_api_key()
    
    upload_option = st.sidebar.selectbox('Select an upload option:', 
                                    ['Upload a CSV file',
                                      'Use Demo Dataset'
                                     ]
 )
    
    uploaded_file = get_uploaded_file(upload_option)
    
    display_main_content(uploaded_file, openai_api_key)

if __name__ == "__main__":
    main()