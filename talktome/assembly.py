# `pip install assemblyai` (Windows)

import assemblyai as aai

aai.settings.api_key = "465f365129a140a8b5948bb83e4a7e5b"
transcriber = aai.Transcriber()

transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

print(transcript.text)