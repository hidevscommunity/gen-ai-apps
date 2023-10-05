import streamlit as st
from PIL import Image
import base64 
import fitz

def render_file(page_index): 
    col1, col2, col3, col4 = st.columns([6,0.1,6,0.1])
    with col1:
        # st.text("Original Document:")
        # base64_pdf = base64.b64encode(bytes_data).decode("utf-8")
        # pdf_display = f"""
        #     <iframe src="data:application/pdf;base64,{base64_pdf}" width="600px" height="800px" type="application/pdf"></iframe>
        # """
        # st.markdown(pdf_display, unsafe_allow_html=True)
        
        doc = fitz.open("data/original/temp.pdf")
        
        page = doc[int(page_index)]
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        st.image(img)
        

    with col2:
        st.empty()

    with col3:
        # st.text("De-identified Document:")

        # with open("data/filtered/temp_masked.pdf", "rb") as f:
        #     base64_pdf = base64.b64encode(f.read()).decode("utf-8")

        # pdf_display = f"""
        #     <iframe src="data:application/pdf;base64,{base64_pdf}" width="600px" height="800px" type="application/pdf"></iframe>
        # """
        # st.markdown(pdf_display, unsafe_allow_html=True)
        doc = fitz.open("data/filtered/temp_masked.pdf")
        
        page = doc[int(page_index)]
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        st.image(img)

    with col4:
        st.empty()


def download_pdf_btn():
    with open("data/filtered/temp_masked.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="Export Filtered PDF",
                    data=PDFbyte,
                    file_name="filtered.pdf",
                    mime='application/octet-stream')