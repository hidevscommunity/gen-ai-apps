import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.messages import *
from langchain.vectorstores import FAISS
from models.agents import agents_classes
import json
from utils.helpers import get_file_names
def get_conversation_chain(conversation=None):
    st.progress(100, text=f'Getting Agents')
 
    embeddings = OpenAIEmbeddings()
    try:
        vectorstore = FAISS.load_local(f"dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/input/vector", embeddings)
    except:
        vectorstore = None
    try:
        csvs = get_file_names(f"dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/input/tables")
    except:
        csvs = None
    try:
        images = json.loads(open(f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/input/images/metadata.json', 'r').read())
        if(len(images) == 0):
            images = None
    except:
        images = None

    conversation_chain = {}
    for el in agents_classes:
        chat_memory = []
        if conversation:
            if el in conversation:
                chat_memory = eval(conversation[el]["memory"])
            
        arguments = agents_classes[el]['arguments']
        parameters = {}
        included = True
        for arg in arguments:
            value = eval(arg)
           
            if value is None:
                included = False
                break
            parameters[arg] = eval(arg)
        if included:
            if(conversation):
                if(el in conversation):
                    conversation_chain[el] = {
                        "executor":agents_classes[el]['func'](**parameters),
                        "messages":conversation[el]["messages"],
                        "issues":conversation[el]["issues"]
                    }
            else:
                conversation_chain[el] = {
                    "executor":agents_classes[el]['func'](**parameters),
                    "messages":[],
                    "issues":[]
                }
    if len(conversation_chain) == 0:
        return False
    st.session_state['conversation_chain'] = conversation_chain

   
    return True