import assemblyai as aai
from tempfile import NamedTemporaryFile
import streamlit as st

class AssemblyHandler:
	def __init__(self,api_key=st.secrets["ASSEMBLYAI_API_KEY"]):
		aai.settings.api_key = api_key
	def get_audio_transcript(self,linkaudio):
		
		self.transcriber = aai.Transcriber()
		self.transcript = self.transcriber.transcribe(linkaudio)
		st.sidebar.header("Audio Transcript")
		st.sidebar.write(self.transcript.text)
		return self.transcript.text
