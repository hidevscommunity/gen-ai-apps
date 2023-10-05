import weaviate

import json
import streamlit as st

weaviate_key = st.secrets["weaviate_key"]
open_ai_key = st.secrets["openai_key"]

def set_up_weaviate():
    client = weaviate.Client(
        url = "https://streamlit-hackathon-kvxr2loy.weaviate.network",  
        auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_key),
        additional_headers = {
        "X-OpenAI-Api-Key": open_ai_key 
    }
    )

    class_obj = {
        "class": "Question",
        "vectorizer": "text2vec-openai",
        "moduleConfig": {
            "text2vec-openai": {},
        }
    }

    client.schema.create_class(class_obj)

    return client


def load_data_to_weaviate(data):

    client = weaviate.Client(
        url = "https://streamlit-hackathon-kvxr2loy.weaviate.network",  
        auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_key),
        additional_headers = {
        "X-OpenAI-Api-Key": open_ai_key 
    }
    )

    client.batch.configure(batch_size=100)  # Configure batch

    with client.batch as batch:  # Initialize a batch process
        for i, d in enumerate(data):  # Batch import data
            print(f"importing question: {i+1}")
            properties = {
                "answer": d["answer"],
                "question": d["question"],
            }
            batch.add_data_object(
                data_object=properties,
                class_name="Question"
            )

def query_weaviate(query):
    client = weaviate.Client(
        url = "https://streamlit-hackathon-kvxr2loy.weaviate.network",  
        auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_key),
        additional_headers = {
        "X-OpenAI-Api-Key": open_ai_key 
    }
    )


    response = (
        client.query
        .get("Question", ["question", "answer"])
        .with_near_text({"concepts": [f"query"]})
        .with_limit(3)
        .do()
    )

    return [response['data']['Get']['Question'][i]["answer"] for i in range(0,3)]

def clear_weviate():
    client = weaviate.Client(
        url = "https://streamlit-hackathon-kvxr2loy.weaviate.network",  
        auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_key),
        additional_headers = {
        "X-OpenAI-Api-Key": open_ai_key 
    }
    )
        
    client.batch.delete_objects(class_name='Question')