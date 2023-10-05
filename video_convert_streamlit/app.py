import streamlit as st
from moviepy.editor import *
import tempfile
import os
from yt_dlp import YoutubeDL
from time import sleep
from yt_dlp.utils import DownloadError
from googletrans import Translator

# Configuração da página

st.markdown("""
<style>
    .big-font {
        font-family: serif;
        font-size:35px !important;
        font-weight: bold;
        text-align: center;
        color: LightGray;
        border: 1px solid black;
        text-shadow: 2px 2px 2px grey;
    }
    #MainMenu {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Home", "Help"])

with tab1:
    st.image("Imagens/IMG_20230630_110827.png")
    #st.markdown('<h1 class="big-font">📽️ VIDEO CONVERTER ONLINE 🎶</h1>', unsafe_allow_html=True)
    st.divider()
    youtube_link = st.text_input('Insert a YouTube link and press Enter:', placeholder="paste the link here.", help="Click share on the YouTube video and copy the link that will be pasted here... It also works with Facebook videos.")
    video_file = st.file_uploader("Upload a video file:", type=['mp4', 'mov', 'avi', 'flv', 'wmv'],help="Select the video file you want to convert to audio.")

    def download_youtube_video(url):
        try:
            ydl_opts = {'outtmpl': 'downloaded_videos/%(title)s.%(ext)s'}
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_url = ydl.prepare_filename(info_dict)
                return video_url
        except DownloadError:
            st.error("⚠️ An error occurred while trying to download the video.  Please, to avoid possible errors, click share on the YouTube page and copy the generated link... If the error persists, try another link.")
            return None

    if video_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(video_file.read())
        
        video_clip = VideoFileClip(tfile.name)

        if st.button('Convert to MP3'):
            with st.spinner('Converting Video...'):
                audio_clip = video_clip.audio
                audio_file = f"{tfile.name}.mp3"
                audio_clip.write_audiofile(audio_file)
                audio_data = open(audio_file, 'rb').read()
                st.audio(audio_data, format='audio/mp3')
                st.download_button(label="Download MP3", data=audio_data, file_name="output.mp3", mime="audio/mpeg")

    if youtube_link:
        video_file_path = download_youtube_video(youtube_link)
        if video_file_path is not None:
            video_clip = VideoFileClip(video_file_path)
            st.video(video_file_path)

            if st.button('Convert video to MP3'):
                with st.spinner('Converting YouTube Video...'):
                    audio_clip = video_clip.audio
                    audio_file = f"{video_file_path}.mp3"
                    audio_clip.write_audiofile(audio_file)
                    audio_data = open(audio_file, 'rb').read()
                    st.audio(audio_data, format='audio/mp3')
                    st.info('Audio ready for download, click the button below:')
                    st.download_button(label="Download YouTube MP3", data=audio_data, file_name="youtube_output.mp3", mime="audio/mpeg")

            if st.button('Download YouTube Video'):
                with st.spinner('Preparing YouTube video for download...'):
                    sleep(3)
            
                    video_data = open(video_file_path, 'rb').read()

                    st.info('Video ready for download, click the button below:')
                    st.download_button(label="Click here to download the video", data=video_data, file_name="youtube_video.mp4", mime="video/mp4")

    st.divider()
    st.markdown("Developed by: Mauro Alves")
    
    st.markdown("""
        <a href="https://github.com/Maurynn" target="_blank" style="margin-right: 15px; text-decoration: none">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="Github logo" width="25" height="25">
        </a>
        <a href="https://linkedin.com/in/maurosp" target="_blank" style="margin-right: 15px; text-decoration: none">
        <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" alt="LinkedIn logo" width="25" height="25">
        </a>
        <a href="https://instagram.com/maurinn?igshid=ZDc4ODBmNjlmNQ==" target="_blank" style="margin-right: 15px; text-decoration: none">
        <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram logo" width="25" height="25">
        </a>
        <a href="https://wa.me/5511952483074" target="_blank" style="margin-right: 15px; text-decoration: none">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp logo" width="25" height="25">
        </a>
    """, unsafe_allow_html=True)


    #"[View the source code](https://github.com/Maurynn/video_convert_streamlit/blob/main/app.py)"

with tab2:
    st.header("Instructions for use:")
    st.write("""
    1. **Upload a video file:** Click the "Upload a video file" button and choose a video file from your device in one of the supported formats (.mp4, .mov, .avi, .flv, . wmv).
    
    2. **Insert a YouTube Link:** If you prefer, you can simply enter the YouTube video link in the "Insert a YouTube Link" input field.
    
    3. **Convert to MP3:** After uploading the video file or entering the YouTube link, click the "Convert to MP3" button.  The video will be converted to an MP3 audio file.
    
    4. **MP3 Download:** After conversion, a "Download MP3" button will appear.  Click it to download the MP3 audio file to your device.
    
    5. **Video Download:** If you have entered a YouTube link, you can also download the original video by clicking the "Download Video" button.
    
    If you have any questions or problems, please contact support.
    Email: mauro.mn@hotmail.com
    """)
