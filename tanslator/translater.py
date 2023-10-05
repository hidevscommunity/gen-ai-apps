import streamlit as st
from googletrans import Translator
from gtts import gTTS
import tempfile
import os

translater=Translator()
st.title("Translator to English to Any ")
# Create a Streamlit column layout
left_column, right_column = st.columns([3, 2])



# Create a dropdown button on the right side
with right_column:
    option = right_column.selectbox("Select an option:", ["German", "Tamil", "Hindi"])
dic={"German":"de","Tamil":"ta","Hindi":"hi"}
res=dic[option]
col1,col2=st.columns(2)
with col1:

    user_input = st.text_area("English",height=200)

with col2:
    promt=translater.translate(user_input,dest=res)
    st.text_area(option,promt.text,height=200)
    
if st.button("Translat"):
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    audio_file_path = temp_audio_file.name

            # Convert text to speech using gTTS
    tts = gTTS(promt.text, lang=res)
    tts.save(audio_file_path)

            # Play the generated audio
    st.audio(audio_file_path, format="audio/mp3")