import streamlit as st
import openai
from PIL import Image
import io

st.markdown("# Design:rainbow[AI]de")

with st.expander("About this tool"):
    st.write("LangChain, Clarifai")

########
image = st.file_uploader('Upload a PNG image', type=['jpg', 'png'])

if image is not None:
    image = Image.open(image, mode="r")
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes = image_bytes.getvalue()

    ##################################################################################################
    # In this section, we set the user authentication, user and app ID, model details, and the URL
    # of the image we want as an input. Change these strings to run your own example.
    #################################################################################################

    # Your PAT (Personal Access Token) can be found in the portal under Authentification
    PAT = st.secrets["clarifai_pat"]
    # Specify the correct user_id/app_id pairings
    # Since you're making inferences outside your app's scope
    USER_ID = 'salesforce'
    APP_ID = 'blip'
    # Change these to whatever model and image URL you want to use
    MODEL_ID = 'general-english-image-caption-blip-2-6_7B'
    MODEL_VERSION_ID = 'd5ce30a4f98646deb899a19ff4becaad'

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




    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=image_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]

    print("Predicted concepts:")
    for concept in output.data.concepts:
        print("%s %.2f" % (concept.name, concept.value))

    # Uncomment this line to print the full Response JSON
    st.write(output)