import os 
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
import streamlit as st
from streamlit_chat import message

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
model_id = "gpt-3.5-turbo-instruct"


loaders = PyPDFLoader('docs/medica.pdf')

index = VectorstoreIndexCreator().from_loaders([loaders])

st.title('🦜 Query your PDF document ')
prompt = st.text_input("Enter your question to query your PDF documents")

if prompt:
    # Get the resonse from LLM
    # We pass the model name (3.5) and the temperature (Closer to 1 means creative resonse)
    # stuff chain type sends all the relevant text chunks from the document to LLM
    response = index.query(llm=OpenAI(model_name=model_id, temperature=0.2,
                                      openai_api_key=OPENAI_API_KEY),
                                      question=prompt, chain_type='stuff')

    # Add the question and the answer to display chat history in a list
    # Latest answer appears at the top
    st.session_state.question.insert(0, prompt)
    st.session_state.answer.insert(0, response)
    
    # Display the chat history
    for i in range(len(st.session_state.question)):
        message(st.session_state['question'][i], is_user=True)
        message(st.session_state['answer'][i], is_user=False)

if 'answer' not in st.session_state:
    st.session_state['answer'] = []

if 'question' not in st.session_state:
    st.session_state['question'] = []
