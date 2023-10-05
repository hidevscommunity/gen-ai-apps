import assemblyai as aai
import requests
import streamlit as st
import time
import json

API_KEY=st.secrets["aai_api"]
# replace with your API token
base_url = "https://api.assemblyai.com/v2"

headers = {
    "authorization": API_KEY,
    "content-type": "application/json"
}


def transcribe(audio_file):
    upload_response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=audio_file)
    audio_url = upload_response.json()['upload_url']
    print(audio_url)
    data = {
    "audio_url": audio_url,
    "iab_categories": True,
    "speaker_labels": True
    
    }
    url = base_url + "/transcript"
    response = requests.post(url, json=data, headers=headers)
    transcript_id = response.json()['id']
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result['status'] == 'completed':
            utterances = transcription_result['utterances']
            transcript = []
            for utterance in utterances:
                speaker = utterance['speaker']
                text = utterance['text']
                transcript.append({f"Speaker {speaker}": text})
            return [transcript, transcription_result['id']]


        elif transcription_result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(3)
        
def summarize(transcription_id, context):
    transcript_ids = [transcription_id]

    data = {
        "transcript_ids": transcript_ids,
        "context": context,
        "answer_format": '''**<topic header>**
<topic summary>
'''
    }

    lemur_output = post_lemur(API_KEY, data)
    lemur_response = lemur_output.json()
    if "error" in lemur_response:
        print(f"Error: { lemur_response['error'] }")
    else:
        return(lemur_response['response'])
def post_lemur(api_token, data):
    url = "https://api.assemblyai.com/lemur/v3/generate/summary"

    headers = {
        "authorization": api_token
    }

    response = requests.post(url, json=data, headers=headers)
    return response




