import streamlit as st
######################################################################################################
# In this section, we set the user authentication, user and app ID, model details, and the URL of
# the text we want as an input. Change these strings to run your own example.
######################################################################################################
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from google.protobuf.struct_pb2 import Struct #for custom metadata
import simple
import add_text

PAT = st.secrets["CLARIFAI_PAT"]
USER_ID = st.secrets["clarifai_user_id"]

############################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
############################################################################

def call_workflow(stub, user_metadata, userDataObject, workflow, data_url, concepts=[]):
    st.write("workflow",workflow, "data",data_url)
    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,
            workflow_id=workflow,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(text=resources_pb2.Text(url=data_url))
                )
            ],
        ),
        metadata=user_metadata,
    )
    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        st.write(post_workflow_results_response.status)
        st.write(post_workflow_results_response)
        raise Exception(
            "Post workflow results failed, status: " + post_workflow_results_response.status.description
        )

    #st.write("post_workflow_results_response")
    #st.code(post_workflow_results_response)
    #st.write("post_workflow_results_response raw")
    #st.code(post_workflow_results_response.results[0].outputs[0].data.text.raw)
    # We'll get one WorkflowResult for each input we used above. Because of one input, we have here one WorkflowResult
    results = post_workflow_results_response.results[0]

    # Each model we have in the workflow will produce one output.
    for i,output in enumerate(results.outputs):
        model = output.model
        st.write("Predicted text",i)
        st.code(output.data.text.raw)

        if len(output.data.concepts)>0:
            st.write("Predicted concepts for the model `%s`" % model.id)
            for concept in output.data.concepts:
                st.write("	%s %.2f" % (concept.name, concept.value))

    res = str(results)
    #st.write(dir(results.outputs[0]))
    #metadata = {"res":res}
    custom_metadata = {
        "workflow":workflow,
        "data_url":data_url,
        "concepts": concepts,
    }
    custom_metadata["res"]=res
    
    # Uncomment this line to st.write the full Response JSON
    fstr = str(results.outputs[-1].data.text.raw)
    add_text.add_text(stub,userDataObject,user_metadata,fstr, concepts, custom_metadata)
