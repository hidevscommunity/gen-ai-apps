import streamlit as st
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
import pandas as pd  # Import pandas library for reading CSV files

def extract_text_from_csv(uploaded_file):
    try:
        # Read the CSV file using pandas
        df = pd.read_csv(uploaded_file)
        # Assuming your CSV file has a column named 'text' containing text data
        text_data = ' '.join(df['text'].astype(str))
        return text_data
    except Exception as e:
        st.error(f"Error extracting text from CSV: {e}")
        return None

def generate_response(uploaded_file, openai_api_key, query_text):
    # Load document if file is uploaded
    if uploaded_file is not None:
        text_data = extract_text_from_csv(uploaded_file)
        if text_data:
            # Split documents into chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.create_documents([text_data])
            # Select embeddings
            embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
            # Create a vectorstore from documents
            db = Chroma.from_documents(texts, embeddings)
            # Create retriever interface
            retriever = db.as_retriever()
            # Create QA chain
            qa = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=openai_api_key), chain_type='stuff', retriever=retriever)
            return qa.run(query_text)

# Page title
st.set_page_config(page_title='Ask the CSV Data')
st.title('🦜🔗 Ask the CSV Data')

# File upload
uploaded_file = st.file_uploader('Upload a CSV file', type=['csv'])  # Specify 'csv' as the accepted file type
# Query text
query_text = st.text_input('Enter your question:', placeholder='Please provide a short summary.', disabled=not uploaded_file)

# Form input and query
result = []
with st.form('myform', clear_on_submit=True):
    openai_api_key = st.text_input('OpenAI API Key', type='password', disabled=not (uploaded_file and query_text))
    submitted = st.form_submit_button('Submit', disabled=not(uploaded_file and query_text))
    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response = generate_response(uploaded_file, openai_api_key, query_text)
            result.append(response)
            del openai_api_key

if len(result):
    st.info(response)