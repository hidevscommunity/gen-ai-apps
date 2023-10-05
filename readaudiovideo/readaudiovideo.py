import streamlit as st
from st_clickable_images import clickable_images
from tempfile import NamedTemporaryFile
import pandas as pd
from pytube import YouTube
import os
import requests
from time import sleep
from fpdf import FPDF 
import datetime
import base64
from pathlib import Path
from streamlit_option_menu import option_menu



st.set_page_config(
  page_title="read-audio-video",
  page_icon="  ",
  layout="wide",
  initial_sidebar_state="expanded",
) 


upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"



@st.cache_data
def save_audio(url) :
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
    return yt.title, file_name, yt.thumbnail_url

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
        # st.write(polling_response.json())
        # st.write(status)

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

with st.sidebar:
        st.markdown("[![Foo](https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Linkedin_unofficial_colored_svg-48.png)](https://www.linkedin.com/in/mahantesh-hiremath/) If you want api key DM me APIKEY.I will send you for a limited time.")        
        choice = st.selectbox(
        'Do you want to transcribe YouTube or Audio/Video?',
        ('YouTube','Audio/Video'))
        AssemblyAI_key = st.sidebar.text_input("AssemblyAI api key", type="password")
        headers = {
         "authorization": AssemblyAI_key,
        "content-type": "application/json"
        }
if choice == 'YouTube':
        with st.sidebar:
                st.markdown("""STEP1 : Input Api Key""")
                st.markdown("""STEP2 : C&P youtube urls with ; take from youtube.""")
                st.markdown("""Format should be as below(notice watch?v=). More url more time it takes""")
                st.markdown("""https://www.youtube.com/watch?v=fDE1e8sQA7I;
                            https://www.youtube.com/watch?v=TmAO9jBqJf4;
                            https://www.youtube.com/watch?v=p3HHBQ-chN4;
                            https://www.youtube.com/watch?v=6Mya4C3Yr7I;""")
                st.markdown("""STEP3 : Press Ctrl+Enter all thumbnails will appear""")
                st.markdown("""STEP4 : You can click on any thumbnail respective audio you can see also transcript will be generated.""")


        st.title("Extract YouTube Video content to PDF or TXT")
        #link to  YouTube channel
        st.markdown(" 👉 [🎥Visit my YouTube channel for more details](https://bit.ly/atozaboutdata)")

        file = st.text_area("Input url separated by ; then press ctrl+enter",height=100)
        urls_list=[q.strip() for q in file.split(';') if q.strip()]
        if file is not None:
            titles = []
            locations = []
            thumbnails = []

            for video_url in urls_list:
                # download audio
                video_title, save_location, video_thumbnail = save_audio(video_url)
                if video_title:
                    titles.append(video_title)
                    locations.append(save_location)
                    thumbnails.append(video_thumbnail)

            selected_video = clickable_images(thumbnails,
            titles = titles,
            div_style={"height": "400px", "display": "flex", "justify-content": "center", "flex-wrap": "wrap", "overflow-y":"auto"},
            img_style={"margin": "5px", "height": "150px"}
            )

            st.markdown(f"Thumbnail #{selected_video+1} clicked" if selected_video > -1 else "No youtube thumbnail clicked")

            if selected_video > -1:
                video_url = urls_list[selected_video]
                video_title = titles[selected_video]
                save_location = locations[selected_video]

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

                        summary = results.json()['text']
                        bullet_points = results.json()['summary']
                        st.markdown("Complete transcription  of youtube video")
                        st.markdown("If you want to download as .pdf select below content and ctrl+P and save ")
                        st.markdown(
                            f'<iframe srcdoc="{summary}" width="100%" height="300px"></iframe>',
                            unsafe_allow_html=True
                            )
                        st.header("Video summary ")
                        st.write(bullet_points)
else:
            with st.sidebar:
                st.markdown("""STEP1 : Input Api Key""")
                st.markdown("""STEP2 : Upload any .mp3, .mp4 or .wav file""")
                st.markdown("""STEP3 : Relax and see the magic begins""")
            st.title("Extract Audio or Video content to PDF or TXT")
            #link to  YouTube channel
            st.markdown(" 👉 [🎥Visit my YouTube channel for more details](https://bit.ly/atozaboutdata)")
            st.markdown(" 👉 [Snowflake DCWT 2023 Bengaluru Opening Keynote recording](https://drive.google.com/drive/folders/14Uj3GmjIl0IA-KPo7V0v4OwPAYUyubSJ)")
            file = st.file_uploader("Upload an audio or video file", type=["mp3", "mp4", "wav"])

            if file is not None:
                if file.type == "audio/mpeg" or file.type == "video/mp4" or file.type == "audio/wav":
                    st.audio(file, format='audio/wav')

                    # Save the uploaded file
                    with NamedTemporaryFile(delete=False) as temp_file:
                        temp_file.write(file.read())
                        uploaded_file_path = temp_file.name

                    st.markdown("File successfully uploaded!")
                    st.balloons()

                    # Applying the same transcription logic as before
                    audio_url, error = upload_to_AssemblyAI(uploaded_file_path)
                    if error:
                        st.write(error)
                    else:
                        polling_endpoint, error = start_analysis(audio_url)
                        if error:
                            st.write(error)
                        else:
                            results = get_analysis_results(polling_endpoint)
                            summary = results.json()['text']
                            bullet_points = results.json()['summary']
                            st.markdown("Complete transcription of the uploaded file")
                            st.markdown("If you want to download as .pdf, select the below content and use Ctrl+P to save it.")
                            st.markdown(f'<iframe srcdoc="{summary}" width="100%" height="300px"></iframe>',
                                unsafe_allow_html=True
                            )
                            st.header("File summary")
                            st.write(bullet_points)

                else:
                    st.error("Please upload a valid audio or video file (mp3, mp4, or wav).")                        

