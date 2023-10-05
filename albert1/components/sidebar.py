import streamlit as st
from components.faq import faq

def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key



def sbar():
    with st.sidebar:
        # st.markdown(
        #     "## How to use\n"
        #     "1. Select one chat option from above \n"
        #     "2. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys)🔑\n"
        #     "3. Upload your file📄\n"
        #     "4. Ask questions about the uploaded file💬\n"
        # )
        
    # Create an expander for the "About" section
        about = st.sidebar.expander("About 🤖")

        # Write information about the chatbot in the "About" section
        about.info(
            "#### Albert is an AI Friend, designed for the users to discuss with their Queries in a very easy way.📄"
        )
        about.info("#### Powered by [Langchain & Streamlit⚡]")

        #st.markdown("---")       
        faq()
