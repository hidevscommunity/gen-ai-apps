import os
import shutil
import tempfile
import streamlit as st
    
def saveTemp(file, folder_name="temp"):
    
    # Generate a temporary file name
    tmp_file_name = next(tempfile._get_candidate_names())
    tmp_dir = os.path.join(folder_name, tmp_file_name)
    # Create the folder if it doesn't exist
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    

    # Create a temporary file in the specified folder with the generated name
    tmp_file_path = os.path.join(tmp_dir, file.name)
    with open(tmp_file_path, "wb") as tmp_file:
        tmp_file.write(file.getvalue())

    return {
        "file":tmp_file_path,
        "dir":tmp_dir,
        "name":tmp_file_name
    }

def get_file_names(directory_path):
    if not os.path.exists(directory_path):
        return None

    file_paths = []

    for root, _, files in os.walk(directory_path):
        if len(files) == 1:
            file_paths.append(os.path.join(root, files[0]))
        else:
            file_paths.extend([os.path.join(root, file) for file in files])
    if len(file_paths) == 1:
        return file_paths[0]
    if len(file_paths) == 0:
        return None
    return file_paths

def annotate(annotated,arguments):
    colors = ["#faf","#aff","#ffa","#faa","#afa"]
    annotations = ''
    annotations+=f'annotation("{",".join(arguments)}",background="{colors[0]}",fontSize="14px",marginRight="5px"),'
    for i,text in enumerate(annotated):
         annotations += f'annotation("{text}",background="{colors[i+1]}",fontSize="14px",marginRight="5px"),'
    return f'annotated_text({annotations})'
   
def remove_dir(path):
    try:
        shutil.rmtree(path)
    except Exception as e:
        pass

def reset_dataset_directory():
    remove_dir(f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}')
    os.makedirs(f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/input/tables')
    os.makedirs(f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/input/images')
    os.makedirs(f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/input/vector')
    os.makedirs(f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/output/tables')
    os.makedirs(f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/output/images')
    os.makedirs(f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/output/vector')
    