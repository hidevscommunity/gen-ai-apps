import re
import json
import streamlit as st
import pandas as pd
def st_multi_modal(container,input_string='',subcontainers = []):
    objects = extract_multi_modal(input_string)
    for i,object in enumerate(objects):
        if 0 <= i < len(subcontainers):
             subcontainer = subcontainers[i]
        else:
             subcontainer = container.empty()
             subcontainers.append(subcontainer)
        if(object['type'] == 'text'):
                subcontainer.write(object['content'])
        elif(object['type'] == 'image'):
                object['source'] = subcontainer.image(object['source'].replace(
                                            'dataset/process',
                                            f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}'
                                    )
                                   ,width=250)
        elif(object['type'] == 'chart'):
                subcontainer.image(object['source'].replace(
                                            'dataset/process',
                                            f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}'
                                    ))
        elif(object['type'] == 'table'):
                data = pd.read_csv(object['source'].replace(
                                            'dataset/process',
                                            f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}'
                                    ))
                data.columns = (' ' * i for i in range(data.shape[1]))
                
                subcontainer.dataframe(data,hide_index=True)
                
    return subcontainers
def extract_multi_modal(input_string):
    # Use regex to find all content between < >
    matches = re.findall(r'<(.*?)>', input_string)
    
    parsed_data = []
    
    # Split the input_string using the < > matches
    split_content = re.split(r'<.*?>', input_string)
    
    # Iterate through the split content and matches
    for i in range(len(split_content)):
        if i < len(matches):
            if(split_content[i]!=''):
                parsed_data.append({"type": "text", "content": split_content[i]})
            parsed_json = json.loads(matches[i])    
            parsed_data.append(parsed_json)
        else:
            parsed_data.append({"type": "text", "content": split_content[i]})
    
    return parsed_data

