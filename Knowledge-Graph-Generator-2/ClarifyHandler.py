from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import streamlit as st
from pytube import YouTube
from GraphRenderer import *

class ClarifyHandler:
	def __init__(self,PAT='dc572b447198470daf94aa4a3f2dce82'):
		self.PAT = PAT
		self.USER_ID = 'salesforce'
		self.APP_ID = 'blip'
		self.MODEL_ID = 'general-english-image-caption-blip-2-6_7B'
		self.MODEL_VERSION_ID = 'd5ce30a4f98646deb899a19ff4becaad'
		self.channel = ClarifaiChannel.get_grpc_channel()
		self.stub = service_pb2_grpc.V2Stub(self.channel)
		self.metadata = (('authorization', 'Key ' + self.PAT),)
		self.userDataObject = resources_pb2.UserAppIDSet(user_id=self.USER_ID, app_id=self.APP_ID)

	def get_video_captions_from_file(self,uploaded_file_video):
		with st.spinner("Analyzing Video...."):

			file_bytes = uploaded_file_video.read()

			post_model_outputs_response = self.stub.PostModelOutputs(
				service_pb2.PostModelOutputsRequest(
					user_app_id=self.userDataObject,
					model_id=self.MODEL_ID,
					version_id=self.MODEL_VERSION_ID,
					inputs=[
						resources_pb2.Input(
							data=resources_pb2.Data(
								video=resources_pb2.Video(
									base64=file_bytes
								)
							)
						)
					]
				),
				metadata=self.metadata
			)
			if post_model_outputs_response.status.code == status_code_pb2.MODEL_DEPLOYING:
				st.error("Model is being deployed please wait!!!")
				return None
		

			if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
				print(post_model_outputs_response.status)
				raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
			output = post_model_outputs_response.outputs[0]
			descs=set()
			for i in output.data.frames[:5]:
				descs.add(i.data.text.raw)

			data=""
			for i in descs:
				data+=i
			return data
		
	def get_video_captions_from_url(self,linkid):
		video_url = 'https://www.youtube.com/watch?v='+linkid
		with st.spinner("Fetching video..."):
			try:
				yt = YouTube(video_url)
				streams = yt.streams.filter(progressive=True, file_extension='mp4')
				stream_360p = streams.filter(res='360p').first()
				save_path = ''
				filename = 'video.mp4'
				stream_360p.download(output_path=save_path, filename=filename)
				st.success(f"360p video '{yt.title}' downloaded successfully to {save_path}/{filename}.mp4")
			except Exception as e:
				st.error(f"An error occurred: {e}")
		with open("video.mp4","rb") as f:
			return self.get_video_captions_from_file(f)

	def get_image_captions_from_file(self,uploaded_file_image):
		file_bytes = uploaded_file_image.read()

		post_model_outputs_response = self.stub.PostModelOutputs(
			service_pb2.PostModelOutputsRequest(
				user_app_id=self.userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
				model_id=self.MODEL_ID,
				version_id=self.MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
				inputs=[
					resources_pb2.Input(
						data=resources_pb2.Data(
							image=resources_pb2.Image(
								base64=file_bytes
							)
						)
					)
				]
			),
			metadata=self.metadata
		)
		if post_model_outputs_response.status.code == status_code_pb2.MODEL_DEPLOYING:
			st.error("Model is being deployed please wait!!!")
			return None
		if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
			print(post_model_outputs_response.status)
			raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

		output = post_model_outputs_response.outputs[0]
		return output.data.text.raw

	def get_image_captions_from_url(self,imgurl):
		post_model_outputs_response = self.stub.PostModelOutputs(
			service_pb2.PostModelOutputsRequest(
				user_app_id=self.userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
				model_id=self.MODEL_ID,
				version_id=self.MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
				inputs=[
					resources_pb2.Input(
						data=resources_pb2.Data(
							image=resources_pb2.Image(
								url=imgurl
							)
						)
					)
				]
			),
			metadata=self.metadata
		)
		if post_model_outputs_response.status.code == status_code_pb2.MODEL_DEPLOYING:
			st.error("Model is being deployed please wait!!!")
			return None
		if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
			print(post_model_outputs_response.status)
			raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
		output = post_model_outputs_response.outputs[0]
		return output.data.text.raw
