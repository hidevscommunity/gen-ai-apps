import assemblyai as aai
import streamlit as st
import os
import uuid
from dotenv import load_dotenv
load_dotenv('.env')

aai.settings.api_key = os.getenv("API_KEY")

config = aai.TranscriptionConfig(
  summarization=True,
  summary_model=aai.SummarizationModel.informative, # optional
  summary_type=aai.SummarizationType.bullets # optional
)

topics_config = aai.TranscriptionConfig(iab_categories=True)
transcriber = aai.Transcriber()

@st.cache_data
def get_chapters(url):
    config = aai.TranscriptionConfig(auto_chapters=True)
    transcript = transcriber.transcribe(url, config)
    return transcript.chapters

@st.cache_data
def summarize_video(video_url):
    transcript = transcriber.transcribe(video_url, config) # add your file here
    chapters = get_chapters(video_url)
    os.remove(video_url)
    return transcript.text, chapters


def identify_speakers(video_url):
    transcript = transcriber.transcribe(video_url, config=aai.TranscriptionConfig(speaker_labels=True))
    utterances = transcript.utterances
    for utterance in utterances:
        speaker = utterance.speaker
        text = utterance.text
        print(f"{speaker}: {text}\n")

def topic_detection(audio_file):
    transcript = transcriber.transcribe(audio_file, config=topics_config)
    for result in transcript.iab_categories.results:
        for label in result.labels:
            print(label.label)
def generate_subtitle(audio_file):
    uid = uuid.uuid4()
    file_path = f"generated_files/generated_subtitle_{uid}.srt"
    transcript = transcriber.transcribe(audio_file)
    subtitle = transcript.export_subtitles_srt()
    subtitle_txt = open(file_path, 'a')
    subtitle_txt.write(subtitle)
    subtitle_txt.close()
    os.remove(audio_file)
    return file_path