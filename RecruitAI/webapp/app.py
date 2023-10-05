import streamlit as st
import base64
from recruitai import RecruitAI

st.set_page_config(page_title='RecruitAI')

with st.sidebar:
    openai_api_key = st.text_input('Enter OpenAI API token:', type='password')
    if not (openai_api_key.startswith('sk-') and len(openai_api_key) == 51):
        st.warning('Please enter your OPENAI API KEY!', icon='⚠️')
    else:
        recruit_ai = RecruitAI(openai_api_key=openai_api_key)
        st.success('OPENAI API KEY provided', icon='🎉')

try:
    rad = st.sidebar.radio(
        'Browse the items',
        [
            "About RecruitAI",
            "TXT to PDF",
            "Analysis",
            "Creator"
        ]
    )

    if rad == 'About RecruitAI':
        st.title("Welcome to RecruitAI! :nerd_face:")
        st.markdown("""Are you ready to transform the way you find the best talent for your team? Introducing RecruitAI, a revolution in the candidate selection process!""")
        st.subheader("""What is RecruitAI?""")
        st.markdown("""RecruitAI is a powerful and innovative PDF resume analysis tool designed to simplify and streamline the candidate screening process. With cutting-edge artificial intelligence and an intuitive interface, RecruitAI lets you identify ideal candidates efficiently and accurately.""")
        st.markdown("""Explore in the following items and discovery how RecruitAI can help you! :star-struck:""")

    if rad == "TXT to PDF":

        st.title("Choose the TXT file to convert to PDF")
        st.markdown("""
                We know that many CVs and job descriptions are delivered in TXT
                format. Therefore, this tab is for you to be able to convert the
                TXT file to PDF. It's super easy, try it below. * PS: this part
                does not use the IA ​​model.
                """)
        txt_file = st.file_uploader(
            "Choose a TXT file",
            type=['txt'],
            accept_multiple_files=False
            )

        if txt_file:
            st.markdown("Click on the button below to convert the TXT file to PDF")
            txt_str = txt_file.read()
            txt_str = txt_str.decode('utf-8')

            if st.button("Convert"):
                pdf_bytes = recruit_ai.text2pdf(
                    txt_content=txt_str,
                    with_header=False
                    )

                st.success("File converted successfully!")
                name_pdf = txt_file.name.split(".")[0] + ".pdf"

                with open(name_pdf, "wb") as f:
                    f.write(pdf_bytes.getbuffer())
                with open(name_pdf, "rb") as f:
                    bytes = f.read()
                    b64 = base64.b64encode(bytes).decode()
                    pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="700" height="800" type="application/pdf"></iframe>'

                    st.markdown(pdf_display, unsafe_allow_html=True)

        else:
            st.warning("Please, choose a TXT file")

    if rad == "Analysis":
        st.markdown("""Below, choose a job description and a curriculum file,
                    respectively, to see how RecruitAI works.
                    """)

        col1, col2 = st.columns(2)

        with col1:
            job_description = st.file_uploader(
                "Choose a job description file",
                type=['pdf'],
                accept_multiple_files=False
                )

        with col2:
            curriculum = st.file_uploader(
                "Choose a curriculum file",
                type=['pdf'],
                accept_multiple_files=False
                )

        if job_description and curriculum:
            job_description_str = recruit_ai.get_text_from_pdf(job_description)
            curriculum_str = recruit_ai.get_text_from_pdf(curriculum)
            analyze = st.button("Analyze")

            if analyze:

                messages = recruit_ai.get_prompt(
                    requirements=job_description_str,
                    curriculum=curriculum_str
                    )
                with st.status("Analyzing resume, it won't take long, believe me :nerd_face:"):

                    response = recruit_ai.llm(messages)
                response_pdf_bytes = recruit_ai.text2pdf(
                    txt_content=response.content,
                    with_header=True
                    )

                final_named_pdf = "results.pdf"
                with open(final_named_pdf, "wb") as f:
                    f.write(response_pdf_bytes.getbuffer())
                with open(final_named_pdf, "rb") as f:
                    bytes = f.read()
                    b64 = base64.b64encode(bytes).decode()
                    pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="700" height="800" type="application/pdf"></iframe>'

                    st.markdown(pdf_display, unsafe_allow_html=True)

    if rad == "Creator":
        st.title("Creator: Ramon Medeiro")
        st.markdown("""Hi! I'm Ramon Medeiro, a Data Scientist. I'm a passionate about technology and I love to create new things.""") 
        st.markdown("""I'm always looking for new challenges and i'm creating this project to help people understand how to insert GenAI in different fields of application.""")
        st.markdown("""I created this project also with the intention of participating in the streamlit hackathon about LLMs.""")
        st.markdown("""If you want to know more about me, please visit my [LinkedIn](https://www.linkedin.com/in/ramon-medeiro-767722246/) or my [GitHub](https://github.com/ramoonmedeiro).""")

except Exception as e:
    st.error(
        """Please enter your API key. If you have already entered, the error
        is possibly in your credits or in relation to another part of the
        application. Contact me (r.medeiro10@gmail.com) if the error
        persists"""
        )

    st.error(e)
