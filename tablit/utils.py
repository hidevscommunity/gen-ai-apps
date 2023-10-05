import json
import os
import shutil
import uuid
import zipfile
from base64 import b64encode
from datetime import datetime

import pandas as pd
import requests
import streamlit as st
from langchain.load.dump import dumps

TTL = "10m"


# Function to create and download a zip file
def create_zip_file(assets_path, selected_files, session_id):
    # Create a temporary directory to store the files
    temp_dir = "temp_zip"
    os.makedirs(temp_dir, exist_ok=True)
    file_paths = [os.path.join(assets_path, file) for file in selected_files]
    # Copy the files to the temporary directory
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        temp_file_path = os.path.join(temp_dir, file_name)
        shutil.copy(file_path, temp_file_path)

    # Create the zip file
    zip_file_name = f"{session_id}.zip"
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, temp_dir))

    # Remove the temporary directory
    shutil.rmtree(temp_dir)

    # Provide the download link
    st.download_button(
        label="Download Zip File",
        data=open(zip_file_name, "rb").read(),
        key="zip_download",
        file_name=zip_file_name,
        mime="application/zip",
    )


def get_session_id():
    # Generate a UUID
    my_uuid = uuid.uuid4()

    # Convert the UUID to a string and remove dashes
    uuid_without_dashes = str(my_uuid).replace("-", "")

    return uuid_without_dashes


def delete_empty_subfolders(folder_path):
    try:
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                if not os.listdir(dir_path):  # Check if the directory is empty
                    print(f"Deleting empty folder: {dir_path}")
                    os.rmdir(dir_path)  # Delete the empty directory
    except:
        pass


file_formats = {
    "csv": pd.read_csv,
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
    "xlsm": pd.read_excel,
    "xlsb": pd.read_excel,
}


@st.cache_data(ttl=TTL)
def load_data(uploaded_file):
    try:
        ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    except:
        ext = uploaded_file.split(".")[-1]
    if ext in file_formats:
        return file_formats[ext](uploaded_file)
    else:
        st.error(f"Unsupported file format: {ext}")
        return None


def _get_nimble_credential_string():
    nimble_username = st.secrets.NIMBLE_USERNAME
    nimble_password = st.secrets.NIMBLE_PASSWORD

    nimble_credential_string = b64encode(
        f"{nimble_username}:{nimble_password}".encode("utf-8")
    ).decode("utf-8")
    return nimble_credential_string


def read_config():
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)
    return config


@st.cache_data(ttl=TTL)
def search_platform(assets_path, platform, search_keyword):
    headers = {
        "Authorization": f"Basic {_get_nimble_credential_string()}",
        "Content-Type": "application/json",
    }
    config = read_config()

    mapping = config.get("crawler_mapping")
    if platform != "google":
        url = (
            mapping.get("ecommerce")
            .get(platform)
            .get("url")
            .format(search_keyword=search_keyword)
        )
        json_data = mapping.get("ecommerce").get("json_data")
        json_data["vendor"] = platform
        json_data["url"] = url
        post_url = mapping.get("ecommerce").get("post_url")
        data_key = "SearchResult"
    else:
        json_data = mapping.get("serp").get(platform).get("json_data")
        json_data["query"] = search_keyword
        post_url = mapping.get("serp").get("post_url")
        data_key = "OrganicResult"

    with st.spinner(text=f"Searching for `{search_keyword}` on `{platform}`"):
        response = requests.post(
            post_url,
            headers=headers,
            json=json_data,
        )
    try:
        data = response.json()["parsing"]["entities"][data_key]
        required_columns = config.get("required_columns").get(platform, [])
        df = pd.DataFrame(data)[required_columns]
    except:
        st.warning("Something went wrong while fetching data, please try again!")
        st.stop()

    st.sidebar.success(
        f"Found *{len(df)}* results for *{search_keyword}* on *{platform}*"
    )
    df_path = os.path.join(
        assets_path,
        f"{datetime.now():%Y_%m_%d_%H_%M_%S}_{search_keyword}_{platform}.csv",
    )
    df.to_csv(df_path, index=False)
    return df


def save_chat(assets_path, response):
    chats_path = os.path.join(assets_path, "chat.json")
    with open(chats_path, "w", encoding="utf-8") as f:
        f.write(dumps(response, pretty=True))
