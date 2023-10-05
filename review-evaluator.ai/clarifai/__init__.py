from os import environ

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

PAT = environ['CLARIFAI_PAT']
USER_ID = 'hiro'
APP_ID = 'review-sentinel'

APP_ID = 'review-sentinel'
WORKFLOW_ID = 'sentiment-analysis'
metadata = (('authorization', 'Key ' + PAT),)
userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

from dataclasses import dataclass
import time
from colorama import Fore
from pprint import pprint


@dataclass
class Workflow():
    id: str

    userDataObject = userDataObject

    metadata = metadata

    channel = None

    def __post_init__(self):
        self.channel = ClarifaiChannel.get_grpc_channel()
        self.stub = service_pb2_grpc.V2Stub(self.channel)

    def run(self, raw_text: str):
        start_time = time.time()

        res = self.stub.PostWorkflowResults(
            service_pb2.PostWorkflowResultsRequest(
                user_app_id=self.userDataObject,
                workflow_id=self.id,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=raw_text
                            )
                        )
                    )
                ]
            ),
            metadata=self.metadata
        )
        end_time = time.time()

        print(f"{Fore.GREEN} Elapsed time: {end_time - start_time:.6f} seconds")

        if res.status.code != status_code_pb2.SUCCESS:
            print(res.status)
            pprint(res)
            raise Exception("Post workflow results failed, status: " + res.status.description)
        return res
