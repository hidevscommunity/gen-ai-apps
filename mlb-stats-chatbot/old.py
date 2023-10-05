from langchain.llms import Clarifai
from langchain.text_splitter import TokenTextSplitter
from langchain.chains import APIChain, SimpleSequentialChain, LLMChain, ConversationChain
import requests
from datetime import datetime

from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory

USER_ID = 'openai'
APP_ID = 'chat-completion'
MODEL_ID = 'GPT-4' 
MODEL_VERSION_ID = 'ad16eda6ac054796bf9f348ab6733c72'


baseball_api_doc = requests.get("http://localhost:8000/openapi.yaml").text

MLB_PROMPT_TEMPLATE = """You are given the below Major League Baseball (MLB) API Documentation:
{api_docs}
Using this documentation, generate the full API url to call for answering the user question.
The current year is 2023. You should make sure to include the required parameters when calling the various functions of the API.

Question:{question}
API url:"""

MLB_URL_PROMPT = PromptTemplate(
    input_variables=[
        "api_docs",
        "question",
    ],
    template=MLB_PROMPT_TEMPLATE,
)

CONVERSATION_TEMPLATE = f"""Conversation History:

{{history}}

You are a AI assistant retrieving infomation from a baseball API based on this documentation:

{{baseball_api_doc}}

Based on the user's query, do you need to call the API? Simply state 'Yes' if you need to. Otherwise, give an answer based on the user's question.

Query:{{human_input}}"""
CONVERSATION_PROMPT = PromptTemplate(input_variables=['human_input','baseball_api_doc','history'], template=CONVERSATION_TEMPLATE)

clarifai_llm = Clarifai(user_id=USER_ID,app_id=APP_ID, model_id=MODEL_ID, model_version_id=MODEL_VERSION_ID)
memory = ConversationBufferMemory(input_key='human_input')

convo_chain = LLMChain(llm=clarifai_llm, prompt=CONVERSATION_PROMPT, verbose=True, memory=memory)

api_agent_chain = APIChain.from_llm_and_api_docs(clarifai_llm, baseball_api_doc, verbose=True, api_url_prompt=MLB_URL_PROMPT)

human_input = "What is Adley Rustchman's batting average?"
convo_response = convo_chain.predict(human_input=human_input, baseball_api_doc=baseball_api_doc)

if convo_response == 'Yes':
    api_agent_chain.run(human_input)



