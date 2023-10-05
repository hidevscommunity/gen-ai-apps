import streamlit as st
from dotenv import load_dotenv
import os

def setup_langsmith():
    load_dotenv()
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] =  st.secrets["LANGCHAIN_API_KEY"] if "LANGCHAIN_API_KEY" in st.secrets else os.environ["LANGCHAIN_API_KEY"]
    os.environ["LANGCHAIN_PROJECT"] = "GitDoc-AI"

def main():
    setup_langsmith()
    st.set_page_config(
        page_title="Home",
        page_icon="🏠",
    )
    st.write("# 📚 GitDoc AI")
    st.caption("Your ultimate GitHub Documentation Explorer!")
    st.write("It's your trusty sidekick for navigating through the vast world of open-source projects, making code exploration and documentation retrieval a breeze.")
    st.info('Check out GitDoc AI over [Streamlit](/Streamlit_AI)')
    st.markdown(
    """ 
        ### Key Features
        - 📖 **Rich Documentation Access:** Instantly access project documentation, READMEs, code snippets, and more.
        - 🌟 **Interactive Chat:** Engage with GitDoc for info, questions, and code insights.
        - 🧠 **AI-Powered Insights:** Intelligent code tips with advanced Language Models.
        - 🚀 **Boost Your Development:** Speed up coding, troubleshoot, and stay updated.
        - 🌈 **User-Friendly Interface:** Enjoy a smooth coding experience.

        ### Try Now
        1. 📝 Create a knowledge base at [Build Knowledge](/Build_Knowledge)
        2. 🤖 Connect a chatbot at [Docs Chat](/Docs_Chat)
    """
    )
    st.write("Github Repo : [GitDoc AI](https://github.com/SSK-14/GitDoc-AI)")

if __name__ == "__main__":
    main()
