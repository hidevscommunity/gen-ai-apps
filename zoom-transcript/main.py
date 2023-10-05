import os
import streamlit as st
from dotenv import load_dotenv
import assemblyai as aai
from utils.zoom import ZoomClient

load_dotenv()

# Define the Streamlit app title
st.title("Transcribe Your Zoom Meeting")
st.text("Make Your Meeting Easy")

# Load environment variables
ZOOM_ACCOUNT_ID = st.text_input("Enter Zoom Account ID:")
ZOOM_CLIENT_ID = st.text_input("Enter Zoom Client ID:")
ZOOM_CLIENT_SECRET = st.text_input("Enter Zoom Client Secret:", type="password")
aai.settings.api_key = st.secrets["api_key"]

# Create a Streamlit button to trigger the transcription process
if st.button("Transcribe Zoom Meeting"):
    # Initialize the Zoom client
    a = ZoomClient(account_id=ZOOM_ACCOUNT_ID, client_id=ZOOM_CLIENT_ID, client_secret=ZOOM_CLIENT_SECRET)

    # Get Zoom recordings
    recs = a.get_recordings()

    if recs['meetings']:
        rec_id = recs['meetings'][0]['id']
        my_url = a.get_download_url(rec_id)

        # Initialize the AssemblyAI transcriber
        transcriber = aai.Transcriber()

        # Perform transcription
        transcript = transcriber.transcribe(my_url)

        # Display the transcript on the Streamlit app
        st.header("Transcript:")
        st.text(transcript.text)

        # Save the transcript to a file
        with open('transcript.txt', 'w') as f:
            f.write(transcript.text)
    else:
        st.warning('No meetings to transcribe.')
