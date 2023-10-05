import requests
import streamlit as st

st.cache_data.clear()


def query(payload, api):
    API_URL = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V1.4"
    headers = {"Authorization": f"Bearer {api}"}
    payload1 = dict(inputs=payload)
    response = requests.post(API_URL, headers=headers, json=payload1)
    return response.content


def query1(payload, api):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {api}"}
    payload1 = dict(inputs=payload)
    response = requests.post(API_URL, headers=headers, json=payload1,)
    return response
