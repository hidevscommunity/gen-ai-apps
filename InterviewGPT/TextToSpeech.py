from gtts import gTTS  
from playsound import playsound  

def text2speech(text):
	language='en'
	obj = gTTS(text=text, lang=language, slow=False)  
	obj.save("voice.mp3")  