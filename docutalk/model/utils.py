from langchain.text_splitter import CharacterTextSplitter
from llama_index import SimpleDirectoryReader
import streamlit as st
import re


TEXT_CARET = "\u258c"
PAT = st.secrets.CLARIFAI_PAT
ENV = st.secrets.ENV
VERBOSE = True if ENV == "dev" else False


@st.cache_resource()
def get_document():
    reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
    documents = reader.load_langchain_documents()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(documents)
    return documents


def get_error_message(e: Exception) -> str:
    error_string = str(e)
    pattern = r'"(.*?)"'
    match = re.findall(pattern, error_string)
    try:
        error_desc = match[0]
    except:
        error_desc = error_string
    response = "Oops! Something went wrong. Error: " + error_desc
    return response
