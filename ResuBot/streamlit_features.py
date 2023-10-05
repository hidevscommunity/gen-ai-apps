import streamlit as st
import subprocess
from langchain.document_loaders import PyMuPDFLoader
from llm_functions import summary_jd
from llm_functions import revise_resume
import os

def main(api_key, user_path):
    # st.header("My Website")
    # st.subheader("Data Analytics")
    # st.text("Simple text")
    
    os.system("playwright install")

    uploaded_file = st.file_uploader("Upload your resume", accept_multiple_files=False)
    filename = user_path + "/origintresume.pdf"
    if uploaded_file is not None:
        with open(filename, 'wb+') as f: 
            f.write(uploaded_file.getvalue())
        loader = PyMuPDFLoader(filename)
        pages = loader.load()
        st.session_state["originresume"] = pages[0]
    
    
    # title = st.text_input('Updata your resume', 'What to update?')
    # # st.write('update content is:', title) 

    # col1, col2= st.columns(2)
    # with col1:
    #     st.button("Generate")
    # with col2:
    #     binary_contents = b'example content'
    #     st.download_button('Download latest resume', binary_contents)


    st.session_state["job_url"] = st.text_input('Input the url of the job', '')
    
    if 'latex_templet' not in st.session_state:
        with open('myfile.tex') as fin:
            st.session_state['latex_templet'] = fin.read()
        
    if 'generated' not in st.session_state:
        st.session_state.generated = False
    
    col1, col2, col3, col4= st.columns(4)
    with col1:
        if st.button("Generate"):
            jd = summary_jd(api_key, st.session_state["job_url"])
            new_resume_latex = revise_resume(api_key, st.session_state["originresume"], jd, st.session_state['latex_templet'])
            new_resume_latex = new_resume_latex.split("\documentclass")[-1].split("\end{document}")[0]
            new_resume_latex = '\documentclass' + new_resume_latex + '\end{document}'
            filename = user_path +'/new_resume_latex.tex'
            with open(filename, 'w') as fout:
                fout.write(new_resume_latex)
                
            subprocess.run(['pdflatex', '-interaction=nonstopmode', filename])
            filename = user_path + '/new_resume_latex.pdf'
            # subprocess.run("mv new_resume_latex.pdf " + filename)
            os.system("mv new_resume_latex.pdf " + filename)
            
            st.toast('Mission Complete!')
            st.session_state.generated = True
            
    with col3:
        try:
            if st.session_state.generated == False:
                raise Exception("Sorry, you should generate you resume first.")
            else:
                with open(filename, 'rb') as resume:
                    st.download_button('Download resume', resume, "Resume.pdf")
        except:
            st.warning("resume not ready, please generate")
            
    with col4:
        try:
            if st.session_state.generated == False:
                raise Exception("Sorry, you should generate you resume first.")
            binary_contents = b'example content'
            st.download_button('Download cover leter', coverleter, "Cover letter.pdf")
        except:
            st.warning("cover leter not ready, please generate")
    
    if st.session_state.generated == True:
        # st.markdown(jd)
        # st.markdown(new_resume_latex)
        pass
            