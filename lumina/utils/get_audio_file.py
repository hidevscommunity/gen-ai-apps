# Imports
from pytube import YouTube

# Video to Audio
def get_audio_file(url):
    try:
        video = YouTube(url)
        stream = video.streams.filter(only_audio=True).first()
        stream.download(filename="audio.mp3")
        print("Audio File downloaded in MP3")
    except KeyError:
        print("Unable to fetch video information. Please check the video URL or your network connection.")