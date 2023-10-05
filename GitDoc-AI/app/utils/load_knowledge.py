import os
from PyPDF2 import PdfReader
import tiktoken
import zipfile
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

load_dotenv()

tiktoken.encoding_for_model('gpt-3.5-turbo')
tokenizer = tiktoken.get_encoding('cl100k_base')

def tiktoken_len(text):
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)
    
def process_other_file(file_path, relative_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as file:
            text = file.read()

    text_splitter = get_text_splitter()
    chunks = text_splitter.create_documents([text], metadatas=[{"page": 1, "file": relative_path}])
    return chunks

def process_pdf_file(pdf_file_path, relative_path):
    pdfFileObj = open(pdf_file_path, 'rb')
    pdfReader = PdfReader(pdfFileObj)
    num_pages = len(pdfReader.pages)
    chunks = []

    for i in range(num_pages):
        pageObj = pdfReader.pages[i]
        text = pageObj.extract_text()
        text_splitter = get_text_splitter()
        chunks.extend(text_splitter.create_documents([text], metadatas=[{"page": i, "file": relative_path}]))

    return chunks

def get_text_splitter():
    chunk_size = st.session_state["chunk_size"] or 500
    chunk_overlap = st.session_state["chunk_overlap"] or 100
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=tiktoken_len,
        separators=["\n\n", "\n", " ", ""]
    )

def process_folder(folder, file_types, branch):
    chunks = []
    file_extensions = file_types
    for root, _, files in os.walk(folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, folder)
            relative_path = st.session_state["document_url"] + "/blob/" + branch + '/' + relative_path

            if file_name.endswith(tuple(file_extensions)) is True and file_name.endswith(".pdf"):
                chunks.extend(process_pdf_file(file_path, relative_path))
            elif file_name.endswith(tuple(file_extensions)) is True:
                chunks.extend(process_other_file(file_path, relative_path))
            else:
                continue
    return chunks

def create_vector(folder_path, file_types, branch = "main"):
    chunks = process_folder(folder_path, file_types, branch)
    openai_api_key = st.session_state.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, disallowed_special=())
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore

def unzip_file(zip_file):
    file_name = os.path.splitext(zip_file.name)[0]
    branch = file_name.split('-')[-1]

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        unzip_dir = 'unzipped_files'
        zip_ref.extractall(unzip_dir)
        return unzip_dir + '/' + file_name, branch

def create_vectorstore(unzip_path, file_types, branch):
    vectorstore = create_vector(unzip_path, file_types, branch)
    try:
        os.remove(unzip_path)
    except:
        print("Error while deleting directory ", unzip_path)
        for root, dirs, files in os.walk(unzip_path):
            for file in files:
                os.remove(os.path.join(root, file))
        pass

    return vectorstore
