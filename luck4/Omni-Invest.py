import json
import requests
import streamlit as st
import time
import elasticsearch
from st_pages import Page, show_pages, add_page_title

st.set_page_config(
    page_title = "Omni-Invest",
    page_icon = "🌏"
    
)

st.title("👋 Welcome to 🌏Omni-Invest🌏")

st.title("💫Purpose")
st.info("As we worked for a startup that deals with startup and investment company information, we started this project to devise a way to quickly search and classify a large amount of data and diverse data types. ", icon ="👋")

st.title("💫Over View of Our Services")
st.subheader("1. Unveil Your Investment Minion")
st.write("A fun and engaging project that aims to decode individuals' investment preferences into unique 4-letter codes")
st.subheader("2. SearchWave")
st.write("A search engine that redefines how information is discovered. We have identified the tendencies of investment companies through our own data preprocessing.")
st.subheader("3. ScanScribe")
st.write("An all-in-one solution for efficient document handling and it aims to revolutionize the way of managing documents and data")
st.subheader("4. Chat with the StartupInsight")
st.write("A chatbot you can chat with, topics about the data we have")
