from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from config import *

def get_ingredient_from_image(uploaded_image):
    try:    
        channel = ClarifaiChannel.get_grpc_channel()
        stub = service_pb2_grpc.V2Stub(channel)
        metadata = (('authorization', 'Key ' + IMAGE_PAT),)
        userDataObject = resources_pb2.UserAppIDSet(user_id=IMAGE_USER_ID, app_id=IMAGE_APP_ID)

        image_content = uploaded_image.read()

        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id=IMAGE_MODEL_ID,
                version_id=IMAGE_MODEL_VERSION_ID,  
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            image=resources_pb2.Image(
                                base64=image_content
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )

        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
                error_msg = f"An unexpected error occurred ,Please enter your ingredients mannually bellow "
                st.error(error_msg)
                return None

        
        output = post_model_outputs_response.outputs[0]

        ingredient = output.data.concepts[0].name
        return ingredient
    except Exception as e:
        st.error(f"An unexpected error occurred ,Please enter your ingredients mannually bellow ")
        return None