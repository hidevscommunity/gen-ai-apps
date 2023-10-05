import numpy as np
import streamlit as st
import openai
import requests
import langchain
import os
from PIL import Image
from langchain.chains import LLMChain
from streamlit.components.v1 import components
from streamlit_javascript import st_javascript
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate

openai.api_key = st.secrets["credentials"]["openaikey"]
weatherapikey = st.secrets["credentials"]["weatherapikey"]

os.environ['OPENAI_API_KEY'] = openai.api_key

st.set_page_config(page_title="Moviemate", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Moviemate 🍿🎬")
st.info("You tell us how you feel, we'll recommend you what to watch")

js = """fetch("https://ipapi.co/json").then(function(response) {
    return response.json();
}) """

img = Image.open('./simpsons_cinema.jpg')
numpydata = np.asarray(img)
st.image(numpydata)

result = st_javascript(js)
if result != 0:
    lat = result['latitude']
    lon = result['longitude']
    print(lat, lon)
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lon) + '&appid='+weatherapikey).json()
    weather_desc = response['weather'][0]['description']    
    temp = response['main']['temp']
    humidity = response['main']['humidity']
    prompt = st.secrets["credentials"]["prompt"]
    friend_dialogue = st.text_input(label="How are you feeling now ?")
    if st.button('Submit'):    
        print(friend_dialogue)
        pt = PromptTemplate(template=prompt, input_variables=["weather_desc","temp","humidity", "friend_dialogue"])
        human_message_prompt = HumanMessagePromptTemplate(prompt=pt)
        chat_prompt_template = ChatPromptTemplate.from_messages([human_message_prompt])
        chat = ChatOpenAI(model='gpt-3.5-turbo',temperature=0.9)
        chain = LLMChain(llm=chat, prompt=chat_prompt_template)

        chat_response = chain.run({"weather_desc":weather_desc,"temp":temp,"humidity":humidity,"friend_dialogue":friend_dialogue})
        st.markdown(chat_response)
