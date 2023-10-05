import assemblyai as aai
import streamlit as st

# replace with your API token
aai.settings.api_key = st.secrets['assemblyai']['api_key']

def get_transcript(file):
    # URL of the file to transcribe
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file)
    return transcript
