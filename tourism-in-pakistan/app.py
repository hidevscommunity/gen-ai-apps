import os

import streamlit as st
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA


st.title("Tourism in Pakistan 🇵🇰")
st.subheader("Your travel guide for Pakistan!")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

db = FAISS.load_local("faiss_index", OpenAIEmbeddings())
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=db.as_retriever())

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    output = qa.run(prompt)

    st.session_state.messages.append({"role": "assistant", "content": output})
    st.chat_message("assistant").write(output)
