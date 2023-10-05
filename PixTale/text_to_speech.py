import requests

def text2speech(message, hugging_face_key):
    """
    Convert a text message to speech using Hugging Face's Text-to-Speech API.
    
    Parameters:
    message (str): The text to be converted to speech.
    hugging_face_key (str): The Hugging Face API key for authorization.
    
    Returns:
    None: Writes the generated audio to a file.
    """
    API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    headers = {"Authorization": f"Bearer {hugging_face_key}"}
    payloads = {"inputs": message}

    response = requests.post(API_URL, headers=headers, json=payloads)
    
    if response.status_code == 200:
        with open('audio.flac', 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to convert text to speech. Status code: {response.status_code}")
        print(f"Response: {response.json()}")
