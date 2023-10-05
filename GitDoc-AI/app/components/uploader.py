import streamlit as st
import requests
import zipfile
from io import BytesIO
import os

def load_docs():
    col1, col2 = st.columns(2)
    with col1:
        st.slider('Chunk Size', min_value=100, max_value=2000, value=500, key="chunk_size", help="The length of individual data segments or blocks.")
    with col2:
        st.slider('Chunk Overlap', min_value=0, max_value=500, value=100, key="chunk_overlap", help="Degree of overlap between adjacent segments.")

    uploaded_file = st.file_uploader("If repo is private upload zip file (Optional)", type=["zip"])
    if uploaded_file is not None:
        return uploaded_file
    

def load_github_docs(document_url, branch='master'):
    filename = os.path.basename(document_url.rstrip('/').strip())
    unzip_path = 'unzipped_files' + '/' + filename + '-' + branch
    document_url = document_url + "/archive/refs/heads/" + branch + ".zip"
    temp_dir = os.path.join(os.getcwd(), 'unzipped_files')
    response = requests.get(document_url)
    if response.status_code == 200:
        zip_data = BytesIO(response.content)
        with zipfile.ZipFile(zip_data, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        return unzip_path, branch

    else:
        st.error(f"Failed to download the ZIP file. Status code: {response.status_code}")
        return None