import assemblyai as aai

# replace with your API token

class AssemblyAIHandler:
	def __init__(self,key="3539fcd5f0c841779e6197159dfc2bdb"):
		aai.settings.api_key = key
		self.transcriber = aai.Transcriber()
	def speech_to_text(self,file="./myrecord.wav"):
		transcript = self.transcriber.transcribe(file)
		return transcript.text

