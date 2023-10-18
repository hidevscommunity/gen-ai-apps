import streamlit as st
import utils as ut

st.set_page_config(page_title='Contact Us', layout='wide')
ut.add_logo()
ut.set_acw_header("Contact Us")

contactus = '<p style="color:Grey; font-size: 16px;">Made with ❤️ by TechnoCouple!</p><p style="color:Grey; font-size: 16px;">For inquiries, reach us at <a href="mailto:technocoupled@gmail.com">technocoupled@gmail.com</a></p>'
st.markdown(contactus, unsafe_allow_html=True)