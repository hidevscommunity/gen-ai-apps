import gc
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
from streamlit.runtime.runtime import Runtime
import streamlit as st


def st_runtime():
    global _st_runtime

    if _st_runtime:
        return _st_runtime

    for obj in gc.get_objects():
        if type(obj) is Runtime:
            _st_runtime = obj
            return _st_runtime

_st_runtime = None


runtime = st_runtime()
def get_info(s_id):
    if runtime:
        session_info = runtime.get_client(session_id=s_id)
        return session_info
    


import os
import json
import shutil
from utils.helpers import remove_dir
import streamlit as st
def delete_from_process(user_id,session_id):
    path = f'dataset/process/{user_id}/{session_id}'
    try:
        shutil.rmtree(path)
    except Exception as e:
        pass 
def add_to_process(session_id,user_id):
    ## Load Metadata
    ids = load_sessions()
    ids[session_id] = user_id  
    ## Save Metadata
    save_sessions(ids)
def clear_sessions():
    ids = load_sessions()
    keys_to_delete = []
    for session_id in ids:
       if get_info(session_id) is None:
           delete_from_process(ids[session_id],session_id)
           keys_to_delete.append(session_id)
    for key in keys_to_delete:
        ids.pop(key)
    save_sessions(ids)

def load_sessions():
    ids = json.loads(open(f'dataset/sessions.json', 'r').read())
    return ids
def save_sessions(ids):
    with open('dataset/sessions.json', "w") as json_file:
        json.dump(ids, json_file, indent=4) 
