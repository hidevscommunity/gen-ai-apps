from langchain.prompts.prompt import PromptTemplate
import openai
from dotenv import load_dotenv
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback
# import streamlit as st
load_dotenv()

openai.api_key = os.getenv('openai_api_key')


# @st.cache_data
def generate_response(messages):
    try:
        gpt4_response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages
        )
        return gpt4_response["choices"][0]["message"]["content"]
    except Exception as e:
        print("Exception: ", e)
        return None
    
def generate_langchain_response(document, query):

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    template = """You are a hiring manager at a company interviewing a candidate for a job.
    Ask the candidate to introduce themselves.
    Ask only one question at a time from the context provided, questions might be tricky or factual.
    Do not repeat questions.
    Ask follow-up questions if necessary.
    No matter what the candidate says, you have to only ask questions. Do not write explanations.
    Be formal.
    
    Context: {context}

    {chat_history}

    Candidate: {human_input}
    Assistant:"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input", "context"], template=template
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="human_input")
    chain = load_qa_chain(
        llm=llm, chain_type="stuff", memory=memory, prompt=prompt)
    
    with get_openai_callback() as cb:
        bot_answer = chain.run(input_documents=document, human_input=query, verbose=True)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")
        print(prompt)
        total_tokens = cb.total_tokens
        total_cost = round(cb.total_cost, 4)
        
    return bot_answer, total_tokens, total_cost