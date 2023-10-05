import streamlit as st
import assemblyai as aai
from pytube import YouTube

# Set your AssemblyAI API key here
aai.settings.api_key = st.secrets["api_key"]

# Create a Streamlit app
st.title("Transcript Generator for YouTube Videos")

# User input: YouTube video URL
url = st.text_input("Enter the URL of the YouTube video")

if st.button("Transcribe"):
    if url:
        try:
            # Get the YouTube video
            yt = YouTube(url)

            # Select the audio stream (assuming you want audio transcription)
            audio_stream = yt.streams.filter(only_audio=True).first()

            # Download the audio stream
            audio_stream.download(filename="youtube_audio.mp3")

            # Initialize the transcriber
            transcriber = aai.Transcriber()

            # Transcribe the downloaded audio
            transcript = transcriber.transcribe("youtube_audio.mp3")

            # Display the transcript
            st.subheader("Transcript:")
            st.write(transcript.text)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a valid YouTube video URL")

st.sidebar.text("Powered by AssemblyAI")
