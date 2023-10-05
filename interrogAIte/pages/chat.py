import streamlit as st

import requests
import json

api_token = st.secrets["aai_api"]
def q_format(prompt):
    questions = [
    
    {
        "question": f"{prompt}",
        "answer_format": "Short sentence"
    }
]
    return questions
def post_lemur(api_token, transcript_ids, questions):
    url = "https://api.assemblyai.com/lemur/v3/generate/question-answer"

    headers = {
        "authorization": api_token
    }

    data = {
        "transcript_ids": transcript_ids,
        "questions": questions,
        "model": "basic"
    }

    response = requests.post(url, json=data, headers=headers)
    return response
def question(transcript_id,question):
    lemur_output = post_lemur(api_token, [transcript_id], question)
    lemur_response = lemur_output.json()

    if "error" in lemur_response:
        print(f"Error: { lemur_response['error'] }")
    else:
        return(lemur_response)

def chat():
    st.subheader(f"Ask questions regarding the transcript by {st.session_state['curr_data']['Name']}")
    prompt = st.chat_input("Say something")
    
    if prompt:
        with st.chat_message("user"):
            st.write(f"{prompt}")
        with st.chat_message("assistant"):
            with st.spinner("Generating answer..."):
                # st.write(st.session_state["curr_data"]["transcribed"])
                
                _, id = st.session_state["curr_data"]["transcribed"]
                answer = question(id, q_format(prompt))
                st.write(answer["response"][0]["answer"])
chat()