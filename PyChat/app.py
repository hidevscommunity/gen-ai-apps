import os
import streamlit as st
import json
from llama_index import VectorStoreIndex, ServiceContext,Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
from llama_index import download_loader
from streamlit_lottie import st_lottie
from pathlib import Path
openai.api_key=st.secrets.openai_key

def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
lottie_chatbot=load_lottiefile("lottiefiles/chat.json")
st.set_page_config(layout="centered", page_title="PyChat",initial_sidebar_state="auto", menu_items=None, page_icon="🤖")

st.title("PyChat : Chat with python docs 📚",)
st_lottie(lottie_chatbot,speed=1,reverse=False,loop=True,quality="low",height=300,width=300)

if "messsages" not in st.session_state.keys():
    st.session_state.messages=[{"role":"assistant","content":"Hi, I am PyChat, your python docs assistant. How can I help you today?","time":"00:00"}]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading data..."):
        PDFReader = download_loader("PDFReader")
        loader = PDFReader()
        documents = loader.load_data(file=Path('./data/python.pdf'))
        service_context=ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo",temperature=0.5,system_prompt="You are an expert on the Python library and your job is to answer technical questions. Assume that all questions are related to the Python programming language. Keep your answers technical and based on facts and do not hallucinate features."))
        index=VectorStoreIndex.from_documents(documents,service_context=service_context)
        return index
index=load_data()

chat_engine = index.as_chat_engine(chat_mode="condense_question")

if prompt:= st.chat_input("Your question"):
    st.session_state.messages.append({"role":"user","content":prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner(text="Thinking..."):
            response=chat_engine.chat(prompt)
            st.write(response.response)
            message={"role":"assistant","content":response.response}
            st.session_state.messages.append(message)        