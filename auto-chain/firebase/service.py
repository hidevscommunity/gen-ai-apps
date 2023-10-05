import firebase_admin
from firebase_admin import credentials,firestore,storage
import os
import datetime
from utils.session_state import *
from utils.cache import *
import streamlit as st
if not firebase_admin._apps:
    
    cred = credentials.Certificate({
            "type": "service_account",
            "project_id": os.environ["project_id"],
            "private_key_id": os.environ["private_key_id"],
            "private_key":  os.environ["private_key"],
            "client_email": os.environ["client_email"],
            "client_id": os.environ["client_id"],
            "auth_uri":"https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.environ["client_x509_cert_url"],
            "universe_domain": "googleapis.com"
    })
    app =firebase_admin.initialize_app(cred,{
        'storageBucket':os.environ["storageBucket"]
    })
db = firestore.client()
bucket = storage.bucket()


def upload(id):
    folder_path = f"dataset/process/{st.session_state.user_id}/{st.session_state.session_id}"
    count = 0
    length = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            length += 1
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)

            st.progress(count/length, text=f'Uploading {local_file_path[len(folder_path) + 1:]}')

            remote_file_path = os.path.join(id, local_file_path[len(folder_path) + 1:])
            local_file_path = local_file_path.replace('\\','/')
            remote_file_path = remote_file_path.replace('\\','/')
            blob = bucket.blob(remote_file_path)
            blob.upload_from_filename(local_file_path)
            count = count+1


    return length
def delete_folder( folder_path):
    # List all the blobs (files and subdirectories) in the specified folder
    blobs = bucket.list_blobs(prefix=folder_path)

    # Delete each blob (file) and subdirectory
    for blob in blobs:
        blob.delete()





def download(id,length):
    directory_path = id
    if(not load_from_cache(id)):
        # List all files in the directory
        blobs = bucket.list_blobs(prefix=directory_path)
        # Specify the local directory where you want to save the downloaded files
        local_directory_path = f"dataset/process/{st.session_state.user_id}/{st.session_state.session_id}"
        # Iterate over each file in the directory and download it
        count = 0
        for blob in blobs:

            st.progress(count/length, text=f'Getting {blob.name[len(directory_path):]}')
            # Create the local file path by removing the directory path prefix
            local_file_path = local_directory_path + blob.name[len(directory_path):]
            local_folder_path = os.path.dirname(local_file_path)
            # Download the file to the specified local path
            if not os.path.exists(local_folder_path):
                os.makedirs(local_folder_path)
            blob.download_to_filename(local_file_path)

            count += 1
        ##Add to Cache
        add_to_cache(id)
    
def load_all(sortby):
    
    if os.environ['PARSE_ALL_ENVIRONMENTS'] == "True":
        doc_ref = db.collection('data').where('show','==',True).order_by(sortby, direction=firestore.Query.DESCENDING)
    else:
        doc_ref = db.collection('data').where('show','==',True).where('user','==',st.session_state.user_id).order_by(sortby, direction=firestore.Query.DESCENDING)
    documents = doc_ref.get()
    names = []
    for doc in documents:
        dict = doc.to_dict() 
        names.append(dict)
    return names
def load(id):
    model = None
    agents = None
    model_doc = db.collection('data').document(id).get()
    if(model_doc.exists):
        model = model_doc.to_dict()
        agents_doc = db.collection('conversation').document(id).get()
        if agents_doc.exists:
            agents = agents_doc.to_dict()
            download(id,model['files'])
        else:
            agents = None
    else:
        model = None
    return model,agents
def delete(id):
    model = db.collection('data').document(id)
    agents = db.collection('conversation').document(id)
    delete_folder(id)
    model.delete()
    agents.delete()
    delete_from_cache(id)
    

def save(id,name,chain,options):

    if(id == "NEW"):
        model = db.collection('data').document()
        agents = db.collection('conversation').document(model.id)
    else:
        model = db.collection('data').document(id)
        agents = db.collection('conversation').document(model.id)
    conversation = {}
    total_issues = 0
    for i in options:
        
        memory = memory_session_state(i)
        if(memory):
            memory = str(memory.chat_memory.messages)
        else:
            memory = "None"
        conversation[i] = {
            "messages":chain[i]["messages"],
            "issues":chain[i]["issues"],
            "memory":memory
        }
        total_issues+=len(chain[i]["issues"])
    if(id != "NEW"):
        delete_folder(model.id)
    files = upload(model.id)
    timestamp = int(datetime.datetime.now().timestamp()*1000)
    if(id == "NEW"):
        model.set({
            'id':model.id,
            'name':name,
            'index':st.session_state["model"]["index"],
            'show':True,
            'files':files,
            'total_issues':total_issues,
            'created_at':timestamp,
            'last_updated':timestamp,
            'environment':os.environ['ENVIRONMENT'],
            'user':st.session_state.cookie
        })
    else: 
        model.update({
            'name':name,
            'index':st.session_state["model"]["index"],
            'files':files,
            'total_issues':total_issues,
            'last_updated':timestamp
        })
    agents.set({
        'conversation':conversation
    })
    add_to_cache(model.id)
    return model.id
    

        
