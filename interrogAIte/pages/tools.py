import streamlit as st

import requests
import json


if "image_generated" not in st.session_state['curr_data']:
    st.session_state["curr_data"]["image_generated"]=0
api_token = st.secrets["aai_api"]
hf_api = st.secrets["hf_api"]
def q_format_option(prompt):
    questions = [
    {
        "question": prompt,
        "answer_options": [
            "Yes",
            "No"
        ]
    }
]
    return questions

def q_format(prompt):
    questions = [
    
    {
        "question": f"{prompt}",
        "answer_format": "In detail description"
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

def query(payload):
    API_URL = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V1.4"
    headers = {"Authorization": f"Bearer {hf_api}"}
    payload1 = dict(inputs=payload)
    response = requests.post(API_URL, headers=headers, json=payload1)
    return response.content

def image_generator():
    st.subheader("Generate an image from the transcript")
    
    st.write("If a description of a suspect is given by the witness, this feature generates the composite drawing of the image")
    if st.session_state["curr_data"]["image_generated"]:
        st.image(st.session_state["curr_data"]["image_generated"])
    else:
        if st.session_state["curr_data"]["transcribed"]:
            _, id = st.session_state["curr_data"]["transcribed"]
        else:
            st.write("Please wait for transcription to complete")
            return
        answer = question(id, q_format_option("Is any one of the speakers giving a description of the features of the suspect?"))
        check = answer["response"][0]["answer"]
        
        if check =="Yes":
            st.write("The witness appears to be describing an image")
            
            if st.button("Generate image"):
                desc  = question(id, q_format("Describe the person mentioned in detail from the description given by the witness in transcript"))
                st.write(desc["response"][0]["answer"])
                image=query("Generate a police composite sketch of " + desc["response"][0]["answer"])
                st.image(image)
                st.session_state["curr_data"]["image_generated"]=image
        else:
            st.write("The witness does not appear to be describing any person")
image_generator()