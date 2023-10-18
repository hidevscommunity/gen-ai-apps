import streamlit as st
from pathlib import Path

import json
from unstructured.partition.pdf import partition_pdf
from LangchainHandler import *
from WeaviateHandler import *
from TextToSpeech import *
from AssemblyAIHandler import *
from audio_recorder_streamlit import audio_recorder
import io

st.set_page_config(layout="wide")
st.title("InterviewGPT")
st.header("🦜🔗 Langchain, ✨ Weaviate")

with st.sidebar:
    st.title("Easy Configure")
    open_ai_key=st.text_input("Enter your OpenAI API Key")
    resume=st.file_uploader("Upload your resume📄",type=["pdf"])
    submit=st.button("Extract Data")

def display_dashboard(data):
    st.title("Resume Data")
    if "contact_name" in data:
        st.write("Name : ",data["contact_name"])
    if "contact_email" in data:
        st.write("Email : ",data["contact_email"])
    if "contact_phone_number" in data:
        st.write("Contact Number : ",data["contact_phone_number"])

    st.header("Work Experience")
    if "work_experience" in data:
        st.table(data["work_experience"])

    st.header("Projects")
    if "projects" in data:
        for i in data["projects"]:
            if "name" in i:
                st.write(i["name"])
            if "technologies_used" in i:
                techs=' , '.join(i["technologies_used"])
                st.write("Tech Stack : ",techs)
            if "description" in i:
                st.write("Description : ",i["description"])
            st.markdown("""
                        <hr>
                """, unsafe_allow_html=True)

    st.header("Education and Degrees")
    if "degree" in data:
        for i in data["degree"]:
            if "type" in i:
                st.write("Degree type : ",i["type"])
            if "subject/branch" in i:
                st.write("Subject/Branch : ",i["subject/branch"])
            if "school/college" in i:
                st.write("College/School Name : ",i["school/college"])
            if "year" in i:
                st.write("Year : ",i["year"])
            if "grade" in i:
                st.write("Grade : ",i["grade"])
            if "percentage" in i:
                st.write("Percentage : ",i["percentage"])
            st.markdown("""
                        <hr>
                """, unsafe_allow_html=True)
            
    st.header("Certificates")
    if "certificates" in data:
        for i in data["certificates"]:
            if "name" in i:
                st.write("Name : ",i["name"])
            if "issued_by" in i:
                st.write("Issued By : ",i["issued_by"])
            st.markdown("""
                        <hr>
                """, unsafe_allow_html=True)
    
            
    st.header("Technical Skills")
    if "skills" in data:
        for i in data["skills"]:
            st.write(i)
            
if submit:
    if resume:
        if open_ai_key:
            langchainHandler=LangchainHandler(key=open_ai_key)
            with open("resume.pdf","wb") as f:
                f.write(resume.getvalue())
            elements=partition_pdf(filename="resume.pdf")
            text=""
            for i in elements:
                text+=i.text+'\n'
            with st.spinner("Please wait Extracting Data..."):
                data=langchainHandler.get_resume_headers(text)
                st.sidebar.success("Data extracted")
                # data=temporary_data.data
                st.header("Resume - Parsed Data")
            with st.expander("Expand to view Resume Dashboard"):
                display_dashboard(data)
            st.header("Interview Questions based on your resume 💻")
            weaviateHandler=WeaviateHandler(openaikey=open_ai_key)
            questions,answers,company,role=weaviateHandler.get_questions(data)

            skill_questions=questions["skills"]
            skill_answers=answers["skills"]
            skill_company=company["skills"]
            skill_role=role["skills"]

            work_questions=questions["work_experience"]
            work_answers=answers["work_experience"]
            work_company=company["work_experience"]
            work_role=role["work_experience"]

            project_questions=questions["projects"]
            project_answers=answers["projects"]
            project_company=company["projects"]
            project_role=role["projects"]

            certificate_questions=questions["certificates"]
            certificate_answers=answers["certificates"]
            certificate_company=company["certificates"]
            certificate_role=role["certificates"]


            st.header("Based on Skills ⚙️")
            n=len(skill_questions)+len(work_questions)+len(project_questions)+len(certificate_questions)
            buttons=[0]*n
            nb=0
            assemblyAIHandler=AssemblyAIHandler()

            for i in range(len(skill_questions)):
                st.write(skill_questions[i])
                text2speech(skill_questions[i])
                audio_file = open('voice.mp3', 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')                
                st.write("Asked in : ",skill_company[i])
                st.write("Role : ",skill_role[i])

                with st.expander("View Answer"):
                    st.write(skill_answers[i])
                st.markdown("<hr>", unsafe_allow_html=True)
                nb+=1

            st.header("Based on Work-experience 🏢")
            for i in range(len(work_questions)):
                st.write(work_questions[i])
                text2speech(work_questions[i])
                audio_file = open('voice.mp3', 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
                st.write("Asked in : ",work_company[i])
                st.write("Role : ",work_role[i])
                with st.expander("View Answer"):
                    st.write(work_answers[i])
                st.markdown("<hr>", unsafe_allow_html=True)
                nb+=1

            st.header("Based on Project👨‍💻")
            for i in range(len(project_questions)):
                st.write(project_questions[i])
                text2speech(project_questions[i])
                audio_file = open('voice.mp3', 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
                st.write("Asked in : ",project_company[i])
                st.write("Role : ",project_role[i])
                with st.expander("View Answer"):
                    st.write(project_answers[i])
        
                st.markdown("<hr>", unsafe_allow_html=True)
                nb+=1

            st.header("Based on Certificates📜")
            for i in range(len(certificate_questions)):
                st.write(certificate_questions[i])
                text2speech(certificate_questions[i])
                audio_file = open('voice.mp3', 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
                st.write("Asked in : ",certificate_company[i])
                st.write("Role : ",certificate_role[i])
                with st.expander("View Answer"):
                    st.write(certificate_answers[i])

                st.markdown("<hr>", unsafe_allow_html=True)
                nb+=1
        else:
            st.error("Please enter your OpenAI API key")

    else:
        st.error("Please upload resume")

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
