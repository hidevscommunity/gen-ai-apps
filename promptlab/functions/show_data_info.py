# show_data_info.py

import streamlit as st

def show_data_info(df):

    st.markdown(f'<h3 style="border-bottom: 2px solid #288CFC; ">{"Explore"}</h3>', 
                unsafe_allow_html=True)
    st.text(" ")
    
    rows, cols = st.columns(2)
    
    with rows:
        st.metric("Total rows:", df.shape[0])
        
    with cols:
        st.metric("Total columns:", df.shape[1])