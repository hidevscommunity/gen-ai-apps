import streamlit as st
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from ratelimit import limits, RateLimitException
from google.protobuf.struct_pb2 import Struct #for custom metadata

@limits(calls=10, period=1)
def add_text(stub,userDataObject,user_metadata,fstr, concepts=[], custom_metadata={}):
    text_data = resources_pb2.Text(raw=fstr)

    # Create and update input_metadata
    input_metadata = Struct()
    input_metadata.update(custom_metadata)

    #st.code(fstr)
    concepts2 = [resources_pb2.Concept(id=x, value=1.) for x in concepts]
    data = resources_pb2.Data(text=text_data,
                              concepts=concepts2,
                              metadata=input_metadata)
    post_inputs_response = stub.PostInputs(
        service_pb2.PostInputsRequest(
            user_app_id=userDataObject,
            inputs=[
                resources_pb2.Input( data=data)                
            ],
            
        ),
        metadata=user_metadata
    )
    
    if post_inputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_inputs_response.status)
        raise Exception("Post inputs failed, status: " + post_inputs_response.status.description)
    #st.write(fstr)
    st.write("Posted new results")
    st.code(post_inputs_response)
    #st.code(post_inputs_response.outputs[0].data.text.raw)



