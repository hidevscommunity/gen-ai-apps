import os
import streamlit as st
from langchain.llms import OpenAI
import pandas as pd
from docx import Document
from io import BytesIO
import websockets
import asyncio
import base64
import json
import pyaudio

if 'text' not in st.session_state:
	st.session_state['text'] = 'User Audio: '
	st.session_state['run'] = False
	st.session_state['submit'] = False
# Assembly AI key
#Assembly_AI_key = "ebd9ba962ede4fdeb647cbdb247d8141"

Assembly_AI_key = os.environ.get("Assembly_AI_key")
openai_api_key = os.environ.get("OPENAI_API_KEY")

st.set_page_config(page_title="Interview AI Helper")
st.markdown("# Interview AI Helper")
st.sidebar.header("Interview AI Helper")
st.markdown('''
			
	This demo helps you to speak sample interview answers. Enjoy! 
	
	User Guide:
			Click on start recording to record the interview question. After the question finishes click stop recording button. Then the sample answer will automatically generated.
			
	Another option is manually type the question and click "Generate" button.
	'''
)
st.sidebar.title("Advanced Settings")
job_title = st.sidebar.text_input("Job title")
job_description = st.sidebar.text_input("Copy the job description to here")
speaking_length = st.sidebar.slider("Minutes for answering the question", 0.5, 10.0, 2.0, step = 0.5)  # Default to 2
word_per_min = st.sidebar.slider("Number of words per minutes", 100, 300, 180, step = 5)  # Default to 180
tone = st.sidebar.selectbox("Select tone", ["Normal", "Formal", "Professional", "Academic"], index=0) # Default to "Normal"


# Audio Recognition

user_audio_input = st.empty()
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
 
# starts recording
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

def start_listening():
	st.session_state['run'] = True
global audio_text
audio_text = ''

# Generate Response
def generate_response(input_text):
	st.session_state['run'] = False
	llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
	st.info(llm(input_text))
	
def stop_listening():
	audio_text = st.session_state['text']
	st.session_state.user_text = audio_text
	#user_audio_input.markdown(audio_text)
	st.session_state['text'] = ''
	st.session_state['submit'] = True		
	st.session_state['run'] = False

description, start, stop = st.columns(3)
description.markdown("#### Record your audio:")
start.button('Start Recording', on_click=start_listening)
stop.button('Stop Recording', on_click=stop_listening)
text = st.text_area('Recorded question shows below:',\
						key="user_text")
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
 

async def send_receive():
	
	print(f'Connecting websocket to url ${URL}')

	async with websockets.connect(
		URL,
		extra_headers=(("Authorization", Assembly_AI_key),),
		ping_interval=5,
		ping_timeout=20
	) as _ws:

		r = await asyncio.sleep(0.1)
		print("Receiving SessionBegins ...")

		session_begins = await _ws.recv()
		print(session_begins)
		print("Sending messages ...")


		async def send():
			try:
				while st.session_state['run']:
					try:
						data = stream.read(FRAMES_PER_BUFFER)
						data = base64.b64encode(data).decode("utf-8")
						json_data = json.dumps({"audio_data":str(data)})
						r = await _ws.send(json_data)

					except websockets.exceptions.ConnectionClosedError as e:
						print(e)
						assert e.code == 4008
						break

					except Exception as e:
						print(e)
						assert False, "Not a websocket 4008 error"

					r = await asyncio.sleep(0.01)
			except:
				print("error")


		async def receive():
			try:
				while st.session_state['run']:
					try:
						result_str = await _ws.recv()
						result = json.loads(result_str)['text']

						if json.loads(result_str)['message_type']=='FinalTranscript':
							answer = st.session_state['text'][:-1] +" "+result
							user_audio_input.markdown(answer)
							st.session_state['text'] = answer
							#st.markdown(st.session_state['text'])

					except websockets.exceptions.ConnectionClosedError as e:
						print(e)
						assert e.code == 4008
						break

					except Exception as e:
						print(e)
						assert False, "Not a websocket 4008 error"
			except:
				print("error")
				#user_audio_input.markdown(audio_text)
			
		send_result, receive_result = await asyncio.gather(send(), receive())

submitted = st.button('Submit')
asyncio.run(send_receive())
if not openai_api_key.startswith('sk-'):
	st.warning('Please enter your OpenAI API key!', icon='⚠')
if (st.session_state['submit'] == True or submitted) and openai_api_key.startswith('sk-'):
	min_word = int(speaking_length*word_per_min-25)
	max_word = int(speaking_length*word_per_min+25)
	query_AI = "You are an assistant answer job interview questions for {job_title} position. \
		<<<job title: {job_title}>>>\
		<<<job description: {job_description}>>>\
		<<<Your Response should between {min_word} and {max_word}>>>\
		<<<Speaking tone: {tone}>>>"
	query = f"<<<Answer the following question: {text} >>>"
	print(query)
	print(query_AI)
	generate_response(query_AI+query)
	st.session_state['submit'] == False
