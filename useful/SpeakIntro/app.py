from transformers import pipeline
import gradio as gr
from git import Repo
import os

# model = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-large-xlsr-53-spanish")

# def transcribe(audio):
#   text = model(audio)["text"]
#   return text

# gr.Interface(
#     fn=transcribe,
#     inputs=[gr.Audio(source="microphone", type="filepath")],
#     outputs=["textbox"],
# ).launch()

# 

GITHUB_REPO_URL = os.environ['GITHUB_REPO_URL']


if not os.path.exists('repo_directory'):  
    Repo.clone_from(GITHUB_REPO_URL, 'repo_directory'  )


# git@github.com:
# from repo_directory.useful.
print(os.system('ls -al'))
print(os.system('ls -al repo_directory'))
print(os.system('ls -al repo_directory/useful'))

