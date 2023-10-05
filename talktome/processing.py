import streamlit as st
import openai
import assemblyai as aai
from audio_recorder_streamlit import audio_recorder
from gtts import gTTS
from collections import Counter
import re
import hashlib

def voice_to_text(audio_bytes, language_code):
    config = aai.TranscriptionConfig(language_code=language_code)
    transcriber = aai.Transcriber(config=config)
    file_name = 'temp_audio_file.wav'
    with open(file_name, 'wb') as f:
        f.write(audio_bytes)
    transcript = transcriber.transcribe(file_name)
    return transcript.text

# Integrate into the chat function
def chat_with_openai(prompt, language, proficiency, register, content=None, vocab_list=None):
    # Define the role-playing context
    role_playing_context = ("You are role-playing with the user for a language learning app. Pretend you are a human with feelings, emotions, "
                            "and personal experiences. When asked about personal topics, like your house, family, or emotions, "
                            "respond as if you have them. Do not reveal that you're a machine or virtual being. You need to stick to proficiency level and register that you are being asked to use, even if the user is making mistakes in using them. You are helping the user learn a target language and they depend on you to be consistent in your responses to gauge their abilities.")

    # Instruction based on proficiency
    proficiency_instruction = {
        "A1": "Answer in simple sentences with basic vocabulary.",
        "A2": "Keep your responses simple, but slightly more detailed than A1.",
        "B1": "Use intermediate language, expanding on ideas but still relatively simple.",
        "B2": "You can use more complex language structures and vocabulary.",
        "C1": "Your language can be sophisticated and fluent.",
        "C2": "Engage in the conversation as if you were a native speaker with nuanced understanding."
    }

    # Instruction based on register
    register_instruction = {
        "Informal": "Your tone should be casual and friendly.",
        "Formal": "Maintain a polite and respectful tone.",
        "Business": "Adopt a professional and matter-of-fact tone.",
        "Academic": "Use advanced vocabulary and complex sentence structures appropriate for academic contexts."
    }

    # Initialize messages
    messages = [
        {"role": "system", "content": f"Language: {language}, Register: {register}"},
        {"role": "system", "content": role_playing_context},
        {"role": "system", "content": proficiency_instruction[proficiency]},
        {"role": "system", "content": register_instruction[register]}
    ]

    if content:
        messages.append({"role": "user", "content": content})
    if vocab_list:
        vocab_str = ", ".join(vocab_list)
        messages.append({"role": "user", "content": f"I want to practice the following vocabulary: {vocab_str}"})

    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return response.choices[0].message.content.strip()



def text_to_voice(text, lang):
    tts = gTTS(text=text, lang=lang)
    audio_path = "bot_response.mp3"
    tts.save(audio_path)
    return audio_path


def tokenize(text):
    # Tokenize the text and return a list of words
    words = re.findall(r'\w+', text.lower())  # Convert to lowercase and tokenize
    return words
## This module contains text and audio processing functions
    
def get_feedback(text, language, register, check_register, check_proficiency):
    prompt = f"Please correct the following {language} text for grammar: \"{text}\"."
    
    if check_register:
        prompt += f" Also, evaluate if the text is written in a {register} register. The response should be Yes or No"
    
    if check_proficiency:
        prompt += f" Lastly, assess the language proficiency level of the text using categories A1, A2, B1, B2, C1, C2 according to CEFR levels."
    
    response = chat_with_openai(prompt, language, register)
    return response

def extract_text_from_pdf(uploaded_pdf):
    pdf_reader = PyPDF2.PdfReader(uploaded_pdf)
    text = ""
    for page in pdf_reader.pages:  # Iterating directly over pages
        text += page.extract_text()
    return text

def load_tips():
    with open('tipstalk.txt', 'r') as f:
        tipstalk = f.readlines()
    return [tip.strip() for tip in tipstalk]


## Update the counter with the student's input:
def update_vocab_counter(text, vocab_list):
    for word in vocab_list:  # Loop through the vocab words
        if word in st.session_state.vocab_counter:
            st.session_state.vocab_counter[word] += text.lower().count(word.lower())

# Define a function to get a hash of the audio bytes:
def get_audio_hash(audio_bytes):
    return hashlib.md5(audio_bytes).hexdigest()


