import streamlit as st
from functions import add_eyewitness,display
from streamlit_option_menu import option_menu
from pathlib import Path

if 'count' not in st.session_state:
    st.session_state['count']=1
if "witnesses" not in st.session_state:
    st.session_state["witnesses"]={}
if "refresh" not in st.session_state:
    st.session_state['refresh']=0
if "curr_data" not in st.session_state:
    st.session_state['curr_data']={}
if "transcribed" not in st.session_state["curr_data"]:
    st.session_state["curr_data"]["transcribed"]=0
if "summarized" not in st.session_state["curr_data"]:
    st.session_state["curr_data"]["summarized"]=0
if "analyze" not in st.session_state:
    st.session_state['analyze']=0
if "examples_loaded" not in st.session_state:
    st.session_state["examples_loaded"]=0
def home():
    st.header("InterrogAIte - An online eyewitness testmiony analysis tool")
    st.markdown('''
                # Purpose

People who have seen something happen and can give a first-hand description of it are referred to as "eyewitnesses". After an event (disaster, crime, etc.) has occurred, authorities find eyewitnesses to the event and gather their testimony. Often, the process of recording, analyzing and searching through the testimony of eyewitnesses for valuable information is a long and difficult task. Here is where InterrogAIte comes in.

InterrogAIte is an LLM powered tool which automates the process of analyzing eyewitness testimony. The functions performed by InterrogAIte are:

* **Transcription** : The application provides a transcription of the audio recording of the testimony. This transcription is then used for the other features of the app.
* **Summarization** : This features automatically summarizes the given transcription after being provided with the context of the interview. It generates a short summary containing all the key points of the transcription
* **Chat**: The LLM-powered chat answers any questions asked about the transcript by the user. This reduces time spent searching for specific information and conclusions
* **Tools**: The tools section contains an Image Generator. This is especially helpful when the eyewitness is giving a description of another person (say, a suspect in a crime)

The main libraries used in this application are:
* **AssemblyAI**: Used for transcription of the audio file
* **LeMUR (AssemblyAI)**: Used to generate the summary, power the AI chat and extract key information from the transcript which is used to generate the image
* **HuggingFace** : Used to generate the image via a Realistic Vision model


# Examples

For an example, the tool has been pre-loaded with the testimony of two eyewitnesses, who were present at the site of the assassination of U.S. President John F. Kennedy. Charles Givens, was one of the employees at the building from which the shots were fired and one of the last people to interact with the suspect Lee Harvey Oswald before the shooting. Arnold Rowland was one of the witnesses from the plaza where the shooting occurred, and he describes a "different" person he believes he saw in a window on the same floor where Lee Harvey Oswald is believed to have fired the shots from. Credits: LEMMiNO
                
                ''')
    
    
def run():
    # adding examples
    if not st.session_state["examples_loaded"]:
        st.session_state["examples_loaded"]=1
        audio_file = open("arnold_rowland_testimony.mp3", "rb")
        audio_bytes = audio_file.read()
        pic = open("arnold_rowland.png", "rb")
        pic_bytes = pic.read()
        st.session_state["witnesses"][f"Witness {st.session_state['count']}"]={
                "Name": "Arnold Rowland",
                "desc": "Arnold Rowland was a high school student present at the plaza, who noticed the barrel of a gun poking out from one of the windows of the Texas Book Depository",
                "pic": pic_bytes if pic_bytes is not None else pic_bytes,
                "context": "The witness is describing a 'different' man he saw in the window of the floor where the shots were fired from",
                "audio_bytes": audio_bytes
                }
        st.session_state['count']+=1
        
        audio_file = open("charles_givens_testimony.mp3", "rb")
        audio_bytes = audio_file.read()
        pic = open("charles_givens.png", "rb")
        pic_bytes = pic.read()
        st.session_state["witnesses"][f"Witness {st.session_state['count']}"]={
                "Name": "Charles Givens",
                "desc": "Charles Givens was an employee at the Texas Book Depository, the building where the shots were fired from.",
                "pic": pic_bytes if pic_bytes is not None else pic_bytes,
                "context": "The witness is describing his last encounter with the suspect before the shooting",
                "audio_bytes": audio_bytes
                }
        st.session_state['count']+=1
        
        st.session_state['curr_data']=st.session_state['witnesses']["Witness 1"]
        
    eyewitnesses = ["Home","Add eyewitness"]
    eyewitnesses.extend([st.session_state['witnesses'][witness]['Name'] for witness in st.session_state['witnesses'] if witness is not None])

    with st.sidebar:
        eyewitness_selectbox=option_menu(
            menu_title= None,
            options=eyewitnesses
        )
        
    if st.session_state['refresh']==1:
        st.session_state['refresh']=0
        st.experimental_rerun()
    if eyewitness_selectbox=="Home":
        home()
    if eyewitness_selectbox=="Add eyewitness":
        add_eyewitness()
    for witness in st.session_state['witnesses']:
        if eyewitness_selectbox==st.session_state['witnesses'][witness]["Name"]:
            display(st.session_state['witnesses'][witness])
        
run()