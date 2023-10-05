import os
import streamlit as st
from langchain.llms import OpenAI
import pandas as pd
import pdfplumber
from docx import Document
from io import BytesIO
import websockets
import asyncio
import base64
import json
import pyaudio
from audiorecorder import audiorecorder

if 'text' not in st.session_state:
	st.session_state['text'] = 'User Audio: '
	st.session_state['run'] = False
	st.session_state['submit'] = False
Assembly_AI_key = os.environ.get("Assembly_AI_key")
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Titles
st.set_page_config(page_title="General AI Agent")
st.markdown("# General AI Agent")
st.sidebar.header("General AI Agent")
st.write(
	"""This demo helps you figure out general questions. Enjoy! """
)
audio = audiorecorder("Click to record", "Click to stop recording")
# File uploader PDF
def extract_from_pdf(file):
	with pdfplumber.open(file) as pdf:
		text = ''
		for page in pdf.pages:
			text += page.extract_text()
	return text

# File uploader Word
def extract_from_docx(file):
	doc = Document(file)
	text = ''
	for paragraph in doc.paragraphs:
		text += paragraph.text + '\n'
	return text

uploaded_files = st.file_uploader("(Optional) Upload files", type=['pdf', 'docx'], accept_multiple_files=True)

file_info = "None"
if uploaded_files:
	file_info = ""
	for uploaded_file in uploaded_files:
		file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
		# st.write(file_details)
		file_info += str(file_details)

		if uploaded_file.type == "application/pdf":
			extracted_text = extract_from_pdf(uploaded_file)
			# st.write(extracted_text)
			file_info += str(extracted_text)

		elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
			extracted_text = extract_from_docx(uploaded_file)
			# st.write(extracted_text)
			file_info += str(extracted_text)
		

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

def stop_listening():
	audio_text = st.session_state['text']
	st.session_state.user_text = audio_text
	user_audio_input.markdown(audio_text)
	st.session_state['text'] = ''
	st.session_state['submit'] = True	
	st.session_state['run'] = False
	
description, start, stop = st.columns(3)
description.markdown("#### Record your audio:")
start.button('Start Recording', on_click=start_listening)
stop.button('Stop Recording', on_click=stop_listening)
text = st.text_area('Enter your question:', \
					'What are the three key pieces of advice for learning how to code?', \
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


asyncio.run(send_receive())


# Generate Response
def generate_response(input_text):
	st.session_state['run'] = False
	llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
	st.info(llm(input_text))
#with st.form('my_form'):
	#text = st.text_area('Enter your question:', 'What are the three key pieces of advice for learning how to code?')
	
submitted = st.button('Submit')
if not openai_api_key.startswith('sk-'):
	st.warning('Please enter your OpenAI API key!', icon='⚠')
if (st.session_state['submit'] == True or submitted) and openai_api_key.startswith('sk-'):
	query = f"<<<User question: {text} >>> \
		<<<Additional File Information and Contents: {file_info}>>>"
	print(query)
	generate_response(query)
	st.session_state['submit'] == False
