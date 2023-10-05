import streamlit as st
from ClarifyHandler import *
from LangchainHandler import *
from AssemblyAIHandler import *

st.set_page_config(layout="wide")
st.title("Knowledge Graph Generator ")
st.write("🦜🔗 Langchain, 🤖 Clarifai, 🎵Assembly AI")
with st.sidebar:    
    st.title("Easy configure")
    selected_option = st.radio("Create Knowledge Graph from:", ("Long Textual Data","Keywords", "Video from Device", "Video from YouTube", "Image from Device","Image from URL","Audio from URL"))
    selected={
        "desc":False,
        "keywords":False,
        "video":False,
        "link":False,
        "image":False,
        "imagelink":False,
        "audiolink":False
    }
    if(selected_option=="Long Textual Data"):
        desc=st.text_area("Enter Text Description")
        for i in selected.keys():
            selected[i]=False
            if i=="desc":
                selected[i]=True
    elif(selected_option=="Keywords"):
        keywords=st.text_area("Enter Comma separated Keywords")
        for i in selected.keys():
            selected[i]=False
            if i=="keywords":
                selected[i]=True
    elif(selected_option=="Video from Device"):
        st.info("Model Takes a while to deploy after submitting your input, so if error comes try after 5 minutes. Once the model is deployed there will be no errors!")
        uploaded_file_video = st.file_uploader("Choose a video...", type=["mp4", "mpeg"])
        for i in selected.keys():
            selected[i]=False
            if i=="video":
                selected[i]=True
    elif(selected_option=="Video from YouTube"):
        st.info("Model Takes a while to deploy after submitting your input, so if error comes try after 5 minutes. Once the model is deployed there will be no errors!")
        linkid=st.text_input("Enter youtube video id")
        for i in selected.keys():
            selected[i]=False
            if i=="link":
                selected[i]=True
    elif(selected_option=="Image from Device"):
        st.info("Model Takes a while to deploy after submitting your input, so if error comes try after 5 minutes. Once the model is deployed there will be no errors!")
        uploaded_file_image = st.file_uploader("Choose an image...", type=["jpeg", "jpg","png"])
        for i in selected.keys():
            selected[i]=False
            if i=="image":
                selected[i]=True
    elif(selected_option=="Image from URL"):
        st.info("Model Takes a while to deploy after submitting your input, so if error comes try after 5 minutes. Once the model is deployed there will be no errors!")
        linkimg=st.text_input("Enter image link")
        for i in selected.keys():
            selected[i]=False
            if i=="imagelink":
                selected[i]=True
    elif(selected_option=="Audio from URL"):
        linkaudio = st.text_input("Enter audio file link")
        for i in selected.keys():
            selected[i]=False
            if i=="audiolink":
                selected[i]=True
    submit=st.button("Create Mind Map")
    
if submit:
    with st.spinner("Please wait, processing your request...."):
        graphRenderer=GraphRenderer(500,450)
        langchainHandler=LangchainHandler()
        if selected["desc"]:
            data=langchainHandler.get_relation_triplets(desc)
            graphRenderer.draw_graph(data)
        elif selected["keywords"]:
            data=langchainHandler.keyword_prompt(keywords)
            data=langchainHandler.get_relation_triplets(data)
            graphRenderer.draw_graph(data)
        elif selected["video"] or selected["link"] or selected["image"] or selected["imagelink"]:
            clarifyHandler=ClarifyHandler()
            if selected["video"]:
                    data=clarifyHandler.get_video_captions_from_file(uploaded_file_video)
                    if data!=None:
                        data=langchainHandler.get_relation_triplets(data)
                        graphRenderer.draw_graph(data)
            elif selected["link"]:
                    data=clarifyHandler.get_video_captions_from_url(linkid)
                    if data!=None:
                        data=langchainHandler.get_relation_triplets(data)
                        graphRenderer.draw_graph(data)
            elif selected["image"]:
                    st.sidebar.image(uploaded_file_image,width=200)
                    data=clarifyHandler.get_image_captions_from_file(uploaded_file_image)
                    if data!=None:
                        data=langchainHandler.get_relation_triplets(data)
                        graphRenderer.draw_graph(data)
            elif selected["imagelink"]:
                    data=clarifyHandler.get_image_captions_from_url(linkimg)
                    if data!=None:
                        data=langchainHandler.get_relation_triplets(data)
                        graphRenderer.draw_graph(data)
        elif selected["audiolink"]:
            assemblyHandler=AssemblyHandler()
            data=assemblyHandler.get_audio_transcript(linkaudio)
            data=langchainHandler.get_relation_triplets(data)
            graphRenderer.draw_graph(data)
    
footer="""<style>
.footer {
position:fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by Aditya Yadav - Streamlit LLM Hackathon🤖</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
    
