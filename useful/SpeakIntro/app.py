# Let's get pipelines from transformers
from transformers import pipeline
# Let's import Gradio
import gradio as gr

def main():
  
    # Let's set up the model
    model = pipeline("automatic-speech-recognition", model="moraxgiga/audio_test")
    title = "Audio2Text"
    description = "Record your audio in English and send it in order to received a transcription"


    # Function
    def transcribe(audio):
        # Let's invoke "model" defined above
        text = model(audio)["text"]
        return text


    # Interface Set-Up
    '''gr.Interface(
        fn=transcribe,
        inputs=[gr.Audio(source="microphone", type="filepath")],
        title="Audio-to-text",
        description="kat enterprises llc demo text-to-speech model",
        outputs=["textbox"]
    ).launch()
    '''

    demo = gr.Interface(fn=transcribe ,
                        inputs=[gr.Audio(source="microphone", type="filepath")],
                        outputs=[gr.Textbox(label="Result", lines=3)],
                        title="Audio-to-text",
                        description="kat enterprises llc demo text-to-speech model"
                    )
    demo.launch()