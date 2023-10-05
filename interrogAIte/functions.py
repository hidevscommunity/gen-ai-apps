import streamlit as st
from streamlit_extras.switch_page_button import switch_page
def add_eyewitness():
    st.header("Add an eyewitness")
    name = st.text_input("Enter the name of the eyewitness", key='name')
    desc = st.text_input("Enter a description of the witness", key = 'desc')
    pic = st.file_uploader("Upload the picture of the eyewitness",type=['.jpg','.jpeg','.png'], key='picture')
    pic_bytes=None
    if pic is not None:
        pic_bytes=pic.read()
        st.image(pic_bytes)
    context = st.text_input("Enter the context of the interview",help ='Enter what the subject being discussed is. This helps the model create an accurate summary of the text', key=f'context')
    audio_file = st.file_uploader("Upload the recording transcript: ",type=['.wav','.ogg','.mp3','.wave'], accept_multiple_files=False, key=f'uploader')
    if audio_file is not None:
        audio_bytes = audio_file.read()
        
        # st.write(st.session_state["witnesses"])
        if st.button("Add Eyewitness:"):
            st.session_state["witnesses"][f"Witness {st.session_state['count']}"]={
            "Name": name,
            "desc": desc,
            "pic": pic_bytes if pic_bytes is not None else pic_bytes,
            "context": context,
            "audio_bytes": audio_bytes
            }
            st.success("Eyewitness added successfully")
            st.session_state['count']+=1
            if st.session_state['refresh']==0:
                st.session_state['refresh']=1
    # if audio_file is not None:
    #     audio_bytes = audio_file.read()
    #     st.audio(audio_bytes, format='audio/wav')
    #     analysis_button = st.button("Perform analysis")
    #     if analysis_button:
    #         analyze(audio_bytes, context)
def display(data: dict):
    st.header(data["Name"])
    try:
        st.image(data["pic"], width=200)
    except AttributeError:
        st.write("No picture provided")
        
    audio_bytes = data['audio_bytes']
    context=data["context"]
    desc = data["desc"]
    
    st.subheader("Description")
    if desc:
        st.write(desc)
    else:
        st.write("No description provided for the witness")
    
    st.subheader("Context")
    if context:
        st.write(context)
    else:
        st.write("No context provided for the transcription")
        
    st.write("## Listen to transcript: ")
    st.audio(audio_bytes, format='audio/wav')
    analysis_button = st.button("Perform analysis")
    if analysis_button:
        st.session_state["curr_data"]=data
        st.session_state['analyze']=1
        switch_page("analysis")
    
