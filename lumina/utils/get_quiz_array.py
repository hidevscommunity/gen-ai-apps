# Imports
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import streamlit as st

# Generating Quiz from LLM

def get_quiz_array(text):
    original_string = """{text}

    The text provided above is a transcribed text from an educational video lecture. Your job is to act as a teacher, creating a test using the transcribed video lecture text. The test should contain only multiple choice questions with 4 possible answers to each question and there need to be 10 questions in total. The test is to be made using the information provided only in the transcribed text. You are not supposed to create questions using context outside of the transcribed test. You must also not provide false information as it can ruin the academic integrity of the institution that you are employed at.
    Your response must be in the form of an array, where the 0th index is the question number, 1st index is the question, 2nd index is the first choice, 3rd index is the second choice, 4th index is the third choice, 5th index is the fourth choice, 6th index is the correct answer. Below provided is an example array that you must give your response as. You are supposed to only provide me the response in accordance to the format stated below.
    An example array:
    [[1, "What is the capital of Pakistan?", "Karachi", "Lahore", "Islamabad", "Peshawar", "Islamabad"], [2, "How many kidneys does a human have?", "1", "2", "3", "4", "2"]]

    Give me the result in the form of an array as stated in my question above."""

    # Replace "{text}" with the replacement_text
    prompt = original_string.replace("{text}", text)

    # Your PAT (Personal Access Token) can be found in the portal under Authentification
    PAT = st.secrets["PAT"]
    USER_ID = st.secrets["USER_ID"]
    APP_ID = st.secrets["APP_ID"]
    MODEL_ID = st.secrets["MODEL_ID"]
    MODEL_VERSION_ID = st.secrets["MODEL_VERSION_ID"]
    RAW_TEXT = prompt

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID, 
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=RAW_TEXT
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

    output = post_model_outputs_response.outputs[0]

    result = output.data.text.raw

    return result