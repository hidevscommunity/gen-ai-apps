from gtts import gTTS
from playsound import playsound
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


import streamlit as st


def text_to_speech(input_text):
    logger = logging.getLogger(f"{__name__}.text_to_speech")
    logger.info("Running text to speech function")
    language = "en"

    # Define the path to the "data" folder one level above the current directory
    data_folder = os.path.join(os.path.pardir, "data")

    # Create the "data" folder if it doesn't exist
    if not os.path.exists(data_folder):
        logger.info("Data folder missing. Creating data folder")
        os.makedirs(data_folder)

    # Save the TTS as an MP3 file in the "data" folder
    mp3_file_path = os.path.join(data_folder, "../data/reading.mp3")
    myobj = gTTS(text=input_text, lang=language, slow=False)
    myobj.save("../data/reading.mp3")

    # Play the MP3 file
    absolute_mp3_path = os.path.abspath(mp3_file_path)
    # playsound(absolute_mp3_path)
    st.audio(absolute_mp3_path)


if __name__ == "__main__":
    text_to_speech("Hello, This is a speech to text.")
