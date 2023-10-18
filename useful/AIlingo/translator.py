import streamlit as st
import os
from langchain.chains.openai_functions.openapi import get_openapi_chain
from bs4 import BeautifulSoup
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title="Your AI language assistant", initial_sidebar_state="expanded")

# title section
col1, col2 = st.columns([2, 20], gap="large")
with col1:
    st.image("icons/robot.png", width=80)
with col2:
    st.title(''':rainbow[AIlingo]''')
st.divider()

# options for language selection
languages = ["Spanish", "English", "French", "Portuguese", "Chinese"]
languages_code = {"English": "en", "French": "fr", "Chinese": "zh-CN", "Portuguese": "pt", "Spanish": "es"}
translation, alternative, example = "", "", ""

# sidebar section
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="api_key", type="password")
    target = st.selectbox("Translate language", languages)
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

os.environ["OPENAI_API_KEY"] = openai_api_key

# parse api call response
def response_parser(response):
    if not response:
        return "", "", ""
    explanation = response['explanation']
    soup = BeautifulSoup(explanation, 'html.parser')
    translation_section = soup.find('translation')
    alternatives_section = soup.find('alternatives')
    example_convo_section = soup.find('example-convo')
    return translation_section.get_text(), alternatives_section.get_text(), example_convo_section.get_text()


# input section
submitted = False
col1, col2 = st.columns([1, 20], gap="medium")
with col1:
    st.image("icons/input.png", width=30)
with col2:
    st.header("Input")

with st.form("input"):
    user_input = st.text_input("Tell me the scenario that you need translation")
    submitted = st.form_submit_button("Translate")
st.divider()

# if submitted call speak API
if submitted and user_input:
    chain = get_openapi_chain("https://api.speak.com/openapi.yaml", verbose=True)
    response = chain.run(user_input + " in " + target)
    translation, alternative, example = response_parser(response)


# translation section
col1, col2 = st.columns([1, 20], gap="medium")
with col1:
    st.image("icons/translation.png", width=30)
with col2:
    st.header("Translation")

# write translation result to page
if translation:
    st.write(translation)
    # add text-to-speech part
    trans_sound_file = BytesIO()
    tts = gTTS(translation, lang=languages_code[target])
    tts.write_to_fp(trans_sound_file)
    st.audio(trans_sound_file)
st.divider()

# alternative section
col1, col2 = st.columns([1, 20], gap="medium")
with col1:
    st.image("icons/menu.png", width=30)
with col2:
    st.header("Alternatives")

if alternative:
    alternative_list = alternative.split("\n")
    filter_alter_list = []
    # generate translation and introduction
    for option in alternative_list:
        trans_start = option.find('"')
        trans_end = option.find('"', trans_start+1)
        if trans_start != -1:
            trans_content = option[trans_start + 1:trans_end]
            intro_content = option[trans_end+1:]
            filter_alter_list.append([trans_content,intro_content])
    column_num = len(filter_alter_list)
    columns = st.columns(column_num)
    # show the result in column container
    for i in range(column_num):
        with columns[i]:
            st.markdown("**"+filter_alter_list[i][0]+"**")
            alter_sound_file = BytesIO()
            tts = gTTS(filter_alter_list[i][0], lang=languages_code[target])
            tts.write_to_fp(alter_sound_file)
            st.audio(alter_sound_file)
            st.write(filter_alter_list[i][1])
st.divider()

# example section
col1, col2 = st.columns([1, 20], gap="medium")
with col1:
    st.image("icons/bubble-chat.png", width=30)
with col2:
    st.header("Example")

if example:
    example_list = [line for line in example.split("\n") if line]
    roles = ['user', 'assistant']
    role_index = 0
    st.write(example_list[0])
    # parse the dialogue and generate chat message
    for chat in example_list[1:]:
        message = st.chat_message(roles[role_index])
        message.write(chat[chat.find(":")+1:])
        sound_file = BytesIO()
        tts = gTTS(chat[chat.find(":")+1:], lang=languages_code[target])
        tts.write_to_fp(sound_file)
        st.audio(sound_file)
        role_index = (role_index + 1)%2


