# Imports
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import streamlit as st

# Your Personal Access Token (PAT) for Clarifai authentication
PAT = st.secrets.PAT

# Specify the user and app IDs for Clarifai
USER_ID = st.secrets.USER_ID
APP_ID = st.secrets.APP_ID

# The ID of the Llama2 workflow to use
WORKFLOW_ID = st.secrets.WORKFLOW_ID


# Function to get a response from the Llama2 model
def get_response(prompt):
    # Set up a connection to the Clarifai API using the specified PAT
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    # Create metadata for authentication
    metadata = (("authorization", "Key " + PAT),)
    print(f"metadata: {metadata}")

    # Create a user and app data object
    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
    print(f"userDataObject: {userDataObject}")

    # Initialize an empty response string
    response = ""

    # Send a request to the Llama2 model using the specified workflow and input text
    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,
            workflow_id=WORKFLOW_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(text=resources_pb2.Text(raw=prompt))
                )
            ],
        ),
        metadata=metadata,
    )

    # Check if the API request was successful
    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)
        print(response)
        return response

    # Extract results from the API response
    results = post_workflow_results_response.results[0]

    # Process each output produced by the model
    for output in results.outputs:
        model = output.model

        # Print predicted concepts for the model
        for concept in output.data.concepts:
            print("    %s %.2f" % (concept.name, concept.value))

        # Append the raw text output to the response string
        response += output.data.text.raw + "\n"

    # Print and return the response
    print(f"The model responds with: {response}")
    print(response)
    return response
