from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext
import streamlit as st
from llama_index.llms import OpenAI
import openai

def indexing() -> None:
    """
    Parameters: None

    The function converts the data to whcih the LLM is grounded to vector indices and stores it in a json format in ./storage folder. The data from this folder is extracted in the main.py file

    Returns: None
    """
    openai.api_key = st.secrets['key']
    docs = SimpleDirectoryReader('./data').load_data()
    # print(len(docs))
    service_context = ServiceContext.from_defaults(llm=OpenAI(temperature=0.6, prompt=f"Assist in offering tailored hotel recommendations based on user inquiries, taking into account the desired location, budget constraints, and individual preferences. Ensure to present the most suitable options with comprehensive details regarding amenities, user reviews, and real-time availability. If you have access to URLs or web links associated with these recommendations, please provide them when available."))
    index = VectorStoreIndex.from_documents(documents=docs, service_context=service_context)
    index.storage_context.persist()
    print("data stored in ./storage folder")

indexing()
