# Summarize with further elaboration with generative ai
import streamlit as st
import pandas as pd
from pytube import YouTube
import os
import requests
from time import sleep

import assemblyai as aai
from transformers import pipeline, set_seed

generator = pipeline('text-generation', model='gpt2')
set_seed(42)

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {
    "authorization": st.secrets["auth_key"],
    "content-type": "application/json"
}

@st.cache_data
def save_audio(url):
    yt = YouTube(url)
    try:
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download()
    except:
        return None, None, None
    base, ext = os.path.splitext(out_file)
    file_name = base + '.mp3'
    os.rename(out_file, file_name)
    print(yt.title + " has been successfully downloaded.")
    print(file_name)
    return yt.title, file_name

@st.cache_data
def upload_to_AssemblyAI(save_location):
    CHUNK_SIZE = 5242880
    print(save_location)

    def read_file(filename):
        with open(filename, 'rb') as _file:
            while True:
                print("chunk uploaded")
                data = _file.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    upload_response = requests.post(
        upload_endpoint,
        headers=headers, data=read_file(save_location)
    )
    print(upload_response.json())

    if "error" in upload_response.json():
        return None, upload_response.json()["error"]

    audio_url = upload_response.json()['upload_url']
    print('Uploaded to', audio_url)

    return audio_url, None

@st.cache_data
def start_analysis(audio_url):
    print(audio_url)

    ## Start transcription job of audio file
    data = {
        'audio_url': audio_url,
        'iab_categories': True,
        'content_safety': True,
        "summarization": True,
        "summary_model": "informative",
        "summary_type": "bullets"
    }

    transcript_response = requests.post(transcript_endpoint, json=data, headers=headers)
    print(transcript_response.json())

    if 'error' in transcript_response.json():
        return None, transcript_response.json()['error']

    transcript_id = transcript_response.json()['id']
    polling_endpoint = transcript_endpoint + "/" + transcript_id

    print("Transcribing at", polling_endpoint)
    return polling_endpoint, None

@st.cache_data
def get_analysis_results(polling_endpoint):

    status = 'submitted'

    while True:
        print(status)
        polling_response = requests.get(polling_endpoint, headers=headers)
        status = polling_response.json()['status']

        if status == 'submitted' or status == 'processing' or status == 'queued':
            print('not ready yet')
            sleep(10)

        elif status == 'completed':
            print('creating transcript')

            return polling_response

            break
        else:
            print('error')
            return False
            break


@st.cache_data
def generate_elaboration(text_summary):
    sequences = generator(summary, max_length=400, num_return_sequences=1)
    return sequences[0]['generated_text']


st.title("YouTube Content Ellaborator")
st.markdown("Elaborate existing video that is summarized for future video idea and course work ellaborative support")
st.markdown("1. a summary of the video,") 
st.markdown("2. Extensive ellaboration with generative AI according ") 
st.markdown("Make sure your links are in the format: https://www.youtube.com/watch?v=eT6Iz6S-n_s")

video_url = st.text_input('Youtube URL', 'https://www.youtube.com/watch?v=eT6Iz6S-n_s')

if video_url is not None:
    title = ""
    location = ""

    video_title, save_location = save_audio(video_url)

    if video_title:
        st.header(video_title)
        st.audio(save_location)

        # upload mp3 file to AssemblyAI
        audio_url, error = upload_to_AssemblyAI(save_location)
        
        if error:
            st.write(error)
        else:
            # start analysis of the file
            polling_endpoint, error = start_analysis(audio_url)

            if error:
                st.write(error)
            else:
                # receive the results
                results = get_analysis_results(polling_endpoint)

                summary = results.json()['summary']
                topics = results.json()['iab_categories_result']['summary']
                sensitive_topics = results.json()['content_safety_labels']['summary']

                st.header("Summary of this video")
                st.write(summary)

                st.header("Topics discussed")
                topics_df = pd.DataFrame(topics.items())
                topics_df.columns = ['topic','confidence']
                topics_df["topic"] = topics_df["topic"].str.split(">")
                expanded_topics = topics_df.topic.apply(pd.Series).add_prefix('topic_level_')
                topics_df = topics_df.join(expanded_topics).drop('topic', axis=1).sort_values(['confidence'], ascending=False).fillna('')

                st.dataframe(topics_df)
                
                generated = generate_elaboration(summary)
                
                st.header("Generated Extensive Elaboration")    
                st.markdown(generated)
