from transformers import pipeline
import gradio as gr
import openai, os


def ai_engine(user_input, key_api):
    
    openai.api_key = key_api
    final_prompt =[{"role": "user", "content": "Need about us section description on this content. " + user_input}]
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=final_prompt,
    temperature=0,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.2,
    presence_penalty=0.0,
    stop=[" \n"]
    )

    # Output
    return response.choices[0].message.content

    
# Function
def transcribe(audio,key_api ):
    model = pipeline("automatic-speech-recognition", model="moraxgiga/audio_test")
    text = model(audio)["text"]
    text = ai_engine(text,key_api)

    return text

def main():
  
    title = "SpeakIntro"
    description = "Record your audio in English and get your about section descriptions."


    demo = gr.Interface(fn=transcribe ,
                        inputs=[gr.Audio(source="microphone", type="filepath"),'text'],
                        outputs=[gr.Textbox(label="Result", lines=3)],
                        title=title,
                        description=description
                    )
    demo.launch()