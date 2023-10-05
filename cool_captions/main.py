#Library Imports
import streamlit as st 
import clarifai
from clarifai.client.user import User
from clarifai.client.workflow import Workflow
import openai
from tempfile import NamedTemporaryFile


# Setting up api for Clarifai and ChatGPT and credential
pat = st.secrets.CLARIFAI_PAT
client = User(user_id=st.secrets.USER_ID)
openai.api_key = st.secrets.API_KEY

# Header for the app
st.header("Quirky Image Caption Generator")
st.subheader("Submission for LLM Hackathon")
st.markdown("<p> <i> Sarah Faiz and Vibhor Gupta", unsafe_allow_html=True,help=None)	

#File Upload
image = st.file_uploader("Upload your image", type=["png", "jpg", "jpeg"], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")


# Checking Image 
if image is not None:
	col1,col2,col3 = st.columns([0.25,0.5,0.25])
	with col2:
		st.image(image, "Uploaded Image", width = 300)
	workflow = Workflow("https://clarifai.com/gvibhor/first_testing_app/workflows/blip_2")
	with NamedTemporaryFile(dir='.') as f:
		f.write(image.getbuffer())
		workflow_prediction = workflow.predict_by_filepath(f.name, input_type="image")

		# Original Caption from Clarifai
		workflow_results = workflow_prediction.results[0]
		for result in workflow_results.outputs:
			orig_caption = result.data.text.raw

		# ChatGPT's response generation 5 quirky captions
		completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
		#{"role": "system", "content": "You are a helpful assistant."},
		{"role": "user", "content": f"Write a mix of quirky, funny, and actual music lyrics captions for a social media post. Keep the captions a mix of long and one-to-three-word short ones for the image with {orig_caption}. Suggest a mix of 10  captions"}
		]
		)
		st.write("Here are some quirky captions for your image")
		captions = st.write(completion.choices[0].message["content"])
else:
	st.markdown("<h4 style='color:tomato'> No Image Uploaded, No Caption</h4>",unsafe_allow_html=True)


