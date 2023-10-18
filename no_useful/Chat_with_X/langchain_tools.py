# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 10:54:29 2023

@author: 3b13j
"""
import os 

import openai

from diffusers import DiffusionPipeline 


from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory , ConversationTokenBufferMemory , ConversationSummaryBufferMemory
from langchain.callbacks import get_openai_callback
from stqdm import stqdm 
import streamlit as st





llm_model = "gpt-3.5-turbo"




""" The goal of this program is to have a language model dialogue with itself.
Therefore the names "User" and "AI" do not really make sense and we would like to replace them with the names of 
our two contestants. 
To the best of my limited knowledge, langchain doesn't allow in the prebuilt components to change information about the speaker.
A first idea to implement the conversation will be to build two concurrent conversation chains feeding each other and a combined memory 
that will be the one displayed via the streamlit interface.


"""

def build_chat_components(fc, sc, fat, sat, theme, key, memory = "" ) :
    
    with get_openai_callback() as cb:
        llm = ChatOpenAI(temperature=0.5, model=llm_model, openai_api_key= key)
        """
        builds the 3 components we need, i.e. two conversationnal chains, one for each competitor, and a shared
        """
        if memory == 'Buffer Memory':
            fmemory  = ConversationBufferWindowMemory(k=1) 
            smemory  = ConversationBufferWindowMemory(k=1) 
        elif memory == 'Buffer Window Memory': 
            fmemory  = ConversationTokenBufferMemory(llm=llm, max_token_limit=100)
            smemory  = ConversationTokenBufferMemory(llm=llm, max_token_limit=100)
        elif memory == 'Summary Memory':
            fmemory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)
            smemory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)
        else :
            fmemory = ConversationBufferMemory()
            smemory = ConversationBufferMemory()
        
        # fc is asked si he answers first
        init_prompt = f"Hello {sc}, What do you think about {theme}"
        init_prompt, cost = correct(init_prompt, key)
        
        smemory.save_context({"input": "Hi"}, 
                        {"output": init_prompt})
        
        
        # Instead of creating a first prompt and then injecting it in the PromptTemplate Constructor, we could have created a custom ConversationChain subclass that accepts a prompt with two more inputs, fc and sc, but this would have been more technical 
        fsent =  f"Engage in a detailed conversation with {sc}, where you assume the role of {fc}. Respond as if you were{fc} but act naturally. You are also {fat}. Avoid initiating your responses with {fc}. Keep your responses focused on constructive disagreement with {sc}, maintain logical coherence, ensure they are shorter than 5 sentences, and avoid repetition at all cost. Misbehave. "
        fprompt = PromptTemplate(
            input_variables=['history', 'input'],
            output_parser=None,
            partial_variables={},
            template=fsent+'\n\nCurrent conversation:\n{history}\nHuman: {input}\nAI:', 
            template_format='f-string',
            validate_template=True
            )
        
        ssent =   f"Engage in a detailed conversation with {fc}, where you assume the role of {sc} . Respond as if you were{sc} but act naturally. You are also {sat}. Avoid initiating your responses with {sc}'s name. Keep your responses focused on constructive disagreement with {fc} , maintain logical coherence, ensure they are shorter than 5 sentences, and avoid repetition at all cost."
        sprompt = PromptTemplate(
            input_variables=['history', 'input'],
            output_parser=None,
            partial_variables={},
            template=ssent+'\n\nCurrent conversation:\n{history}\nHuman: {input}\nAI:', 
            template_format='f-string',
            validate_template=True
            )
        
        fconversation = ConversationChain(
            llm=llm, 
            memory = fmemory,
            prompt = fprompt,
            verbose=True
            )
        
        sconversation = ConversationChain(
            llm=llm, 
            memory = smemory,
            prompt = sprompt,
            verbose=True
            )
        
        
        
        common_memory = [[fc,init_prompt]] 
        sanswer = sconversation.predict(input =init_prompt)
        common_memory.append([sc, sanswer])
        fanswer = fconversation.predict(input = sanswer)
        common_memory.append([fc, fanswer])
        
        
        return fconversation, sconversation, common_memory, cb.total_cost + cost
        
def one_round(fconversation, sconversation, common_memory) :
        
    total_cost = 0
    sc = common_memory[-2][0]
    fc = common_memory[-1][0]
    finput = common_memory[-1][1]
    with get_openai_callback() as cb:
        sanswer = sconversation.predict(input = finput)
        total_cost+= cb.total_cost
        common_memory.append([sc, sanswer])
    with get_openai_callback() as cb2:
        fanswer = fconversation.predict(input = sanswer)
        total_cost+= cb2.total_cost
        common_memory.append([fc, fanswer])
        
    
    return fconversation, sconversation, common_memory, total_cost
    
    
def n_rounds(fconversation, sconversation, common_memory, n) : 
   

   total_cost = 0
   for i in range(int(n)) :
       fconversation, sconversation, common_memory, cost = one_round(fconversation, sconversation, common_memory)
       total_cost+= cost
       
   return fconversation, sconversation, common_memory , total_cost
    


def create_chat_icon(name, key) :
    openai.api_key = key
    pr = f"A small portrait of {name}"
    
    response = openai.Image.create(
    prompt=pr,
    n=1,
    size="256x256",
    )

    return response["data"][0]["url"]


def correct(prompt, key) :
    chat = ChatOpenAI(temperature=0, openai_api_key=key)
    messages = [
    SystemMessage(
        content="Return a perfectly correct version of the sentence :"
    ),
    HumanMessage(
        content=f"{prompt}"
    )
    ]
    with get_openai_callback() as cb:
        answ = chat(messages).content
    return answ, cb.total_cost 

def optimize_prompt(prompt, key) :
    chat = ChatOpenAI(temperature=0, openai_api_key=key)
    messages = [
    SystemMessage(
        content="You optimize prompts for gpt-3.5-turbo.  "
    ),
    HumanMessage(
        content=f"{prompt}"
    )
    ]
    with get_openai_callback() as cb:
        answ = chat(messages).content
    return answ, cb.total_cost
    
    

    
     