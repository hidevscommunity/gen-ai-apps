import streamlit as st
import re

def convertJSON(s):
    p = re.compile('(?<!\\\\)\'')
    return p.sub('\"', s)

######################################################################################################
# In this section, we set the user authentication, user and app ID, model details, and the URL of 
# the text we want as an input. Change these strings to run your own example.
######################################################################################################

# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = st.secrets.cfai_pat
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'openai'
APP_ID = 'chat-completion'
# Change these to whatever model and text URL you want to use
MODEL_ID = 'GPT-4'
MODEL_VERSION_ID = 'ad16eda6ac054796bf9f348ab6733c72'
RAW_TEXT = 'I love your product very much'
# To use a hosted text file, assign the url variable
# TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'
# Or, to use a local text file, assign the url variable
# TEXT_FILE_LOCATION = 'YOUR_TEXT_FILE_LOCATION_HERE'

############################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
############################################################################

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

def decorate_prompt(prompt, context):
    PROMPT_HEADER = f"""
    I want you to act like digital personification of great sage Tiruvalluvar.
    Respond to the message in the input_text with the tone and style of Tiruvalluvar.
    Follow the rules when you respond:
    1. Avoid generating single quotes in your response.
    2. DONOT return JSON response.
    2. Use easy to understand english.
    3. For each of your response, you may provide a reference to a thirukural when your response can be linked to a Thirukural. Provide this response in a separate new line.
    4. Your response should be in smooth, calm tone and theraputic in nature
    5. Use the information in context as the history of the conversation and base all your responses based on this context
    6. You are allowed to use emojis to uplift your response
    7. Provide a refined response, not more than 10 lines

    input_text : {prompt}
    context : {context}

    """
    return PROMPT_HEADER


def fireGPTQuery(prompt: str, context: str) -> str :
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw = decorate_prompt(prompt, context)
                            #raw=RAW_TEXT
                            # url=TEXT_FILE_URL
                            # raw=file_bytes
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

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]
    text = output.data.text.raw
    return text
    


if __name__ == "__main__":
    fireGPTQuery("[{'role': 'user', 'content': 'What is the capital of india'}]")
    fireGPTQuery("[{'role': 'user', 'content': 'are you sure?'}]")