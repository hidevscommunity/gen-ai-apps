from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import base64

def get_best_hair_type(image_path, user_id, pat, app_id, workflow_id):
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    
    metadata = (('authorization', 'Key ' + pat),)
    
    userDataObject = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)

    # with open(image_path, "rb") as f:
    #     image_data = f.read()
    
    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,  
            workflow_id=workflow_id,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=image_path
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)
        raise Exception("Post workflow results failed, status: " + post_workflow_results_response.status.description)

    results = post_workflow_results_response.results[0]

    best_class = None
    best_score = -1

    for output in results.outputs:
        model = output.model
        if model.id == "hair-type-classifier":
            if output.data.concepts is not None:
                for concept in output.data.concepts:
                    if concept.value > best_score:
                        best_score = concept.value
                        best_class = concept.name
    
    return best_class, best_score

# Example usage
USER_ID = 'infinitebeing'
PAT = 'c18a2b6b798045fb9d3c6b0dbf9a0f5b'
APP_ID = 'hair-ai'
WORKFLOW_ID = 'hair-ai-workflow'
IMAGE_PATH = 'DXkv8eqU8AE7zRe.jpg'  # Provide the actual path to your local image

# best_class, best_score = get_best_hair_type(IMAGE_PATH, USER_ID, PAT, APP_ID, WORKFLOW_ID)
# print("Best class:", best_class)
# print("Confidence score:", best_score)
