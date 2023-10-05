from typing import Set
import numpy as np
from backend.core import Shan_Story_LLM_Core 
from backend.relation_update import calculate_rank_difference

import streamlit as st
from streamlit_chat import message
from backend.helper import person_list, Relation_dict, Person_dict, question_extract
from backend.core import respond_list_0, respond_list_score_0

import os
#from config import OPENAI_API_KEY
#os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


story_llm_obj = Shan_Story_LLM_Core()
run_llm_selection_chain = story_llm_obj.run_llm_selection_chain
run_llm_end_story_chain = story_llm_obj.run_llm_end_story_chain
run_llm_nextday_story_chain = story_llm_obj.run_llm_nextday_story_chain

#Asking for OPENAI_API_KEY
text_input_container = st.empty()
t = text_input_container.text_input("Enter Your OPENAI_API_KEY")

if t != "":
    text_input_container.empty()
    os.environ["OPENAI_API_KEY"] = t
    story_llm_obj.iniciate_llm()
    
st.header("Story of Shan")

generated_response = None

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = [
        f""" During my sophomore summer break, I found myself working at a coffee shop. As the clock struck three in the afternoon, the cozy ambiance was just beginning to fill with couples enjoying their coffee and sweet moments together.
        Suddenly, a guy with a skateboard appeared right in front of me. He had a mane of curly brown hair and deep, captivating eyes. His handsome features seemed even more alluring as he wiped his face, glistening with sweat. He said, "Give me an Americano, please." Then, with a surprised grin, he exclaimed, "Isn't this Shan? This is Jake! We took an economics class together!"
        """
    ]

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "selection" not in st.session_state:
    st.session_state["selection"] = '<select>'


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string


#Show begining of the stories
message(st.session_state["chat_answers_history"][0], key = "bot_story0")
if len(st.session_state["chat_answers_history"])==1:

    options = ['<select>'] +   respond_list_0

    selection = st.selectbox(
                    'Select an action',
                    (i for i in options), 0, key = "option_part1")

    if selection!= '<select>':
        selection = options.index(selection)
        st.session_state["chat_history"].append({})
        st.session_state["selection"] = selection-1


if st.session_state["selection"]!= '<select>':
    with st.spinner("Generating response.."):

        chat_history = st.session_state["chat_history"][1:]
        if len(st.session_state["chat_history"]) == 0:
            character = "Jake"
        else:
            character = np.random.choice(person_list)

        if len(st.session_state["user_prompt_history"])%5==3:
            generated_response = run_llm_end_story_chain(chat_history, st.session_state["selection"], character, Person_dict)
        elif len(st.session_state["user_prompt_history"])%5==4:
            generated_response = run_llm_nextday_story_chain(chat_history, st.session_state["selection"], character, Person_dict)
        else:
            generated_response = run_llm_selection_chain(chat_history, st.session_state["selection"], character, Person_dict)



        formatted_response = (
            f"{generated_response['new_story']}"
        )
        
        outputed_input = generated_response['human_input'].split("Shan have decided to responded: ")
        if len(outputed_input)>1:
            outputed_input = outputed_input[1]
        else:
            outputed_input = "Continue the story"
        formatted_human_input = (
            f"{ outputed_input}"
        )

        st.session_state["user_prompt_history"].append(formatted_human_input)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(generated_response)



if st.session_state["chat_answers_history"]:
    if len(st.session_state["chat_answers_history"])>1:
        #response, user_query = st.session_state["user_prompt_history"][-1], st.session_state["chat_answers_history"][-1]
        #message(user_query, is_user=True)
        #message(response)
        i=1
        for user_query, response in zip(
            st.session_state["user_prompt_history"][:],
            st.session_state["chat_answers_history"][1:]
        ):
            i+=1
            message(user_query, is_user=True, key = "user_continue{}".format(i))
            message(response, key = "bot_story_continue{}".format(i))

        if generated_response.get("questions")!=None:

            if generated_response:
                options =['<select>'] +  question_extract(generated_response)
            else:
                options = ['<select>'] +   respond_list_0
        else:
            options = ['<select>', "Continue the story"]
        options = [op for op in options if len(op)>0]
        selection = st.selectbox(
                        'Select an action',
                        (i for i in options), 0, key = "option_part2")
        
        if selection!= '<select>':
            print(selection)
            selection = options.index(selection)

            #st.session_state["chat_history"].append({})
            st.session_state["selection"] = selection-1
            #print(len(st.session_state["chat_history"]))
    