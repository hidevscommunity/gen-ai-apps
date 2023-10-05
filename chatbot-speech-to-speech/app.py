import streamlit as st
import streamlit.components.v1 as components
import base64
from tempfile import NamedTemporaryFile
from audiorecorder import audiorecorder
import whisper
from whispercpp import Whisper
from gtts import gTTS
import emoji

#from dotenv import load_dotenv, find_dotenv
#load_dotenv(find_dotenv())

# Streamlit
st.set_page_config(page_title="TalkativeAI", layout="wide", initial_sidebar_state=st.session_state.get("sidebar_state", "expanded"))
st.session_state.sidebar_state = "expanded"

import os
import openai

os.environ["OPENAI_API_BASE"] = "https://shale.live/v1"
os.environ["OPENAI_API_KEY"] = os.getenv("SHALE_API_KEY")

to_language_code_dict = whisper.tokenizer.TO_LANGUAGE_CODE
to_language_code_dict["automatic"] = "auto"
language_list = list(to_language_code_dict.keys())
language_list = sorted(language_list)
language_list = [language.capitalize() for language in language_list if language != "automatic"]
language_list = ["Automatic"] + language_list

@st.cache_resource  # 👈 Add the caching decorator
def load_model(precision):
    if precision == "whisper-tiny":
        model = Whisper('tiny')
    elif precision == "whisper-base":
        model = Whisper('base')
    else:
        model = Whisper('small')
    return model

from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=.7)

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

prompt_1 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a helpful AI assistant. Your name is TARS. Keep your answers short and to the point. It is very important that you reply to a questions in the language it was formulated."
    ),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("Reply to the following question in the language it was formulated: {input}. Just reply don't specify what you're doing.")
])

memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt_1, llm=llm)

#@st.cache_resource
#def aux():
#    memory = ConversationBufferMemory(return_messages=True)
#    conversation = ConversationChain(memory=memory, prompt=prompt_1, llm=llm)
#    return memory, conversation
#
#memory, conversation = aux()

def inference(audio):
    # Save audio to a file:
    with NamedTemporaryFile(suffix=".mp3") as temp:
        with open(f"{temp.name}", "wb") as f:
            f.write(audio.export().read())
        result = w.transcribe(f"{temp.name}", lang=lang)
        text = w.extract_text(result)
    return text[0]

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )


example1 = "Tell me a haiku about AI"


with st.sidebar:
    audio = audiorecorder("Click to send voice message", "Recording... Click when you're done", key="recorder")
    st.title("TalkativeAI")
    language = st.selectbox('Language', language_list, index=23)
    lang = to_language_code_dict[language.lower()]
    precision = st.selectbox("Precision", ["whisper-tiny", "whisper-base", "whisper-small"])
    w = load_model(precision)
    voice = st.toggle("Voice", value=True)
    st.write("Example:")
    Example1 = st.button(example1)
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if (prompt := st.chat_input("Your message")) or Example1 or len(audio):
    if Example1:
        prompt = example1
    # If it's coming from the audio recorder transcribe the message with whisper.cpp
    if len(audio)>0:
        prompt = inference(audio)

    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = conversation.predict(input=prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
        if voice:
            clean_response = emoji.replace_emoji(response, replace='')
            if lang=='es':
                tts = gTTS(clean_response, lang='es', tld='cl')
            else:
                tts = gTTS(clean_response, lang=lang)
            with NamedTemporaryFile(suffix=".mp3") as temp:
                tempname = temp.name
                tts.save(tempname)
                autoplay_audio(tempname)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
