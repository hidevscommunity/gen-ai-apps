import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import openai
import pandas as pd

key = st.sidebar.text_input('Enter your OpenAI API Key to access the app:', type = 'password')
openai.api_key = key

st.title('Interview Preparatory Assistant')
st.caption("🚀 Powered by OpenAI LLM")
st.subheader('Using job description and work experience the assistant\
             will generate possible interview questions and answers.')
job_description =  st.text_input('Enter Job Description and qualifications')
work_description = st.text_input('Explain field of expertise and work experience')
candidate_job_info = job_description + work_description
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
docs = text_splitter.create_documents([candidate_job_info])

if openai.api_key:
    llm = ChatOpenAI(temperature=0.1, model='gpt-3.5-turbo')
    template_string = """
    You are a technical interview preparatory AI bot.\
    Using following candidate_job_info, generate list of minimum 10 interview questions and \
    their proper answers considering current and previous trends in that field.

    Generate question-answer pair in JSON format with following keys:
    question
    answer

    candidate_job_info: {candidate_job_info}
    """
    prompt_template = ChatPromptTemplate.from_template(template_string)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain.run(docs)
    response = json.loads(response)
    interview_df = pd.DataFrame.from_dict(response)
    st.dataframe(interview_df)

else: 
    st.stop()