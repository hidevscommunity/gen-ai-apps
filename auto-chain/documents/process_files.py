    
import os
from utils.helpers import remove_dir,reset_dataset_directory
from .get_vectorstore import get_vectorstore
from .parse_documents import *
import streamlit as st
import json
def process_files(files):
    documents = []
    reset_dataset_directory()
    images_metadata = []
    vectorstore_metadata = []
    for i,file in enumerate(files):
        st.progress((i)/len(files), text=f'Processing {file.name}')
        if file.name.endswith('.pdf'):
            file_path,docs = parse_pdf(file)
            documents.extend(docs)
            vectorstore_metadata.append({"file_path":file_path.replace('\\','/')})
        elif file.name.endswith('.csv'):
            parse_csv(file)
        elif file.name.endswith('.pptx'):
            file_path,docs = parse_pptx(file)
            documents.extend(docs)
            vectorstore_metadata.append({"file_path":file_path.replace('\\','/')})
        elif file.name.endswith('.links.txt'):
            file_path,docs = parse_links(file)
            documents.extend(docs)
            vectorstore_metadata.append({"file_path":file_path.replace('\\','/')})
        elif file.name.endswith('.txt'):
            file_path,docs = parse_txt(file)
            
            documents.extend(docs)
            vectorstore_metadata.append({"file_path":file_path.replace('\\','/')})
        elif file.name.endswith('.docx'):
            file_path,docs = parse_docx(file)
            documents.extend(docs)
            vectorstore_metadata.append({"file_path":file_path.replace('\\','/')})
        elif file.name.endswith('.png') or file.name.endswith('.jpg') or file.name.endswith('.jpeg'):
            file_path,docs,metadata = parse_image(file)
            documents.extend(docs)
            images_metadata.append({
                "image_path":file_path.replace('\\','/'),
                "description":metadata
            })
        elif file.name.endswith('.mp3'):
            file_path,docs = parse_audio(file)
            documents.extend(docs)
            vectorstore_metadata.append({"file_path":file_path.replace('\\','/')})
        st.session_state.files.append(file.name)
    with open(f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/input/images/metadata.json', "w") as json_file:
        json.dump(images_metadata, json_file, indent=4)
    with open(f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/input/vector/metadata.json', "w") as json_file:
        json.dump(vectorstore_metadata, json_file, indent=4)    
    remove_dir('temp')
    # create vector store
    vectorstore = get_vectorstore(documents)
    

    if(vectorstore):
        vectorstore.save_local(f"dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/input/vector")
   