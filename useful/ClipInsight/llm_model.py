from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import Replicate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import streamlit as st
from dotenv import load_dotenv
load_dotenv('.env')

def split_transcript(transcript):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50, length_function = len)
    text_chunks = text_splitter.split_text(transcript)
    return text_chunks

def create_conversational_chain(query, embeddings):
    llm = Replicate(
        streaming = True,
        model = "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781", 
        callbacks=[StreamingStdOutCallbackHandler()],
        input = {"temperature": 0.01, "max_length" :500,"top_p":1})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    vector_store = FAISS.load_local(folder_path="vectorstore", index_name="faiss_db_index", embeddings=embeddings)
    chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                 retriever=vector_store.as_retriever(),
                                                 memory=memory)
    result = chain({"question": query})
    return result["answer"]


def init_llama_response(transcript, query):
    text_chunks = split_transcript(transcript)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(folder_path="vectorstore", index_name="faiss_db_index")
    response = create_conversational_chain(query, embeddings)
    return response