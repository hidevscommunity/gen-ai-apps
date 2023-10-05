__import__('pysqlite3')

import warnings
warnings.filterwarnings('ignore')

import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import streamlit as st
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceEndpoint, HuggingFaceHub, HuggingFacePipeline
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from tempfile import NamedTemporaryFile 

st.title("Streamlit Hackathon 2023")
st.subheader(":purple[QA-PDF]",divider="rainbow")
st.markdown("**A bot to answer questions from the uploaded PDF document**")

os.environ['HUGGINGFACEHUB_API_TOKEN'] = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
embeddings = HuggingFaceEmbeddings()
repo_id = "tiiuae/falcon-7b-instruct"
llm = HuggingFaceHub(repo_id=repo_id)

uploaded_file = st.file_uploader("Upload PDF", "pdf")
if uploaded_file is not None:
    with st.spinner('Please wait for the bot to respond.'):
        bytes_data = uploaded_file.read()
        with NamedTemporaryFile(delete=False) as tmp:
            tmp.write(bytes_data)
        loader = PyPDFLoader(tmp.name)
        pages = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(pages)
        embeddings = HuggingFaceEmbeddings()
        docsearch = Chroma.from_documents(texts, embeddings)
        
        prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Also try to be subjective on the answer and don't include unwanted text
        {context}
        Question: {question}
        Briefly Answer:"""

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        chain_type_kwargs = {"prompt": PROMPT}
    st.success("Model and Embedding are loaded")

    query = st.text_input("Ask your Question")
    if query:
        qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=docsearch.as_retriever(), chain_type_kwargs=chain_type_kwargs)
        st.subheader("Answer")
        answer = qa.run(query).split("\n")[0]
        st.info(answer)

    os.remove(tmp.name)
