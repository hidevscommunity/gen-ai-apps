import os
import base64

def load_sample_job():
    with open(os.path.join("sample", "job_description.txt")) as f:
        description = f.readlines()
        return "".join(description)
    

def get_binary_file_content(file_path):
    with open(file_path, "rb") as f:
        return f.read()


def get_encoded_file_data(file_path):
    binary_content = get_binary_file_content(file_path)
    return base64.b64encode(binary_content).decode()


def create_download_link(file_path, display_text, file_name=None):
    encoded_content = get_encoded_file_data(file_path)
    file_name = file_name or os.path.basename(file_path)
    href = f'<a href="data:file/octet-stream;base64,{encoded_content}" download="{file_name}">{display_text}</a>'
    return href