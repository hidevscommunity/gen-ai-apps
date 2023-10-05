
from llama_index.llms import LangChainLLM
from langchain.llms import Clarifai
from llama_index import VectorStoreIndex, SummaryIndex
from llama_index import ServiceContext
from llama_index import Document
from llama_index import SimpleDirectoryReader
from llama_index.prompts  import PromptTemplate
from llama_index.chat_engine.simple import SimpleChatEngine
from llama_index import LLMPredictor
from pypdf import PdfReader

import streamlit as st

# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = st.secrets.cf_pat
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'anthropic'
APP_ID = 'completion'
# Change these to whatever model and text URL you want to use
MODEL_ID = 'claude-v2'
MODEL_VERSION_ID = 'ad16eda6ac054796bf9f348ab6733c72'

class LLM_Hander:
    def __init__(self):
        pat = PAT
        Cfllm = LangChainLLM(llm = Clarifai(
        pat=pat, user_id=USER_ID, app_id=APP_ID, model_id=MODEL_ID
            ))
        self.documents = []
        self.chat_template = """
            I want you to act as a teacher's assistant. Your task is to help teachers in cutting down their boring tasks.
            Follow the instructions given by the teacher and produce the outputs that the teacher is requesting.
            Retrieve information from the vector index about current input within the service context.
            Also follow the below rules when you respond.
            1. Avoid generating single quotes in your response.
            2. DONOT return JSON response.
            3. Use easy to understand english.
            """
        self.service_context = ServiceContext.from_defaults(llm_predictor=LLMPredictor(llm=Cfllm),
                                                            system_prompt=self.chat_template)
        self.query_index = None
        self.summary_index = None 
        
    def loadData(self, files):
        texts = []
        for f in files:
            st.session_state.fnames.append(f.name)
            reader = PdfReader(f)
            text = ""
            numPages = reader.pages
            for page in numPages:
                text += f'Page number: {reader.get_page_number(page)} \n Content : {page.extract_text()}'
            texts.append(text)

        self.documents = [Document(text=t) for t in texts]
    
    def prepareIndex(self):
        self.query_index = VectorStoreIndex.from_documents(self.documents, service_context=self.service_context)
        self.summary_index = SummaryIndex.from_documents(self.documents, service_context=self.service_context)

    def prepareBots(self):
        self.query_engine = self.query_index.as_query_engine()
        self.chat_engine = self.summary_index.as_chat_engine(chat_mode='react', verbose=True)
    
    def firePrompt(self, role, prompt):
        if role == 'student':
            try:
                return self.query_engine.query(prompt)
            except:
                return 'some error occured. please retry'
        if role == 'teacher':
            try:
                return self.chat_engine.chat(prompt)
            except:
                return 'some error occured. please retry'
            
    def clearHistory(self):
        self.chat_engine.reset()
    


    
