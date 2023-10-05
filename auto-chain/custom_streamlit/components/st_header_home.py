import streamlit as st
from annotated_text import annotated_text,annotation
def st_header_home(header,subheader):
    with header:
            annotated_text(
                    annotation(f"Auto Chain",background="transparent",fontSize="40px",fontWeight="bold"),
                    annotation("pre-alpha", "v0.0.6",background="#aabfff",fontSize="18px"),
            ) 
    with subheader:
        st.subheader("Your documents")
        