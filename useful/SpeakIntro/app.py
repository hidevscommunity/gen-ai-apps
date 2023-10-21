from transformers import pipeline
import gradio as gr

model = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-large-xlsr-53-spanish")

def transcribe(audio):
  text = model(audio)["text"]
  return text

gr.Interface(
    fn=transcribe,
    inputs=[gr.Audio(source="microphone", type="filepath")],
    outputs=["textbox"],
).launch()