import streamlit as st

st.set_page_config(
    page_title="Ask Valluvar Architecture for nerds",
    page_icon="🤓",
)

st.header('Ask Valluvar Software Architecture 🖥️ 📐')

with st.sidebar:
    st.image('./resources/vv.png', use_column_width='always')

st.markdown('### `For nerds out there, here is an overview of how Valluvar AI is powered`', unsafe_allow_html=True)

st.image('./resources/arc.png')
st.info('You can click the :green[arrow] at :orange[top right] of the image to enlarge it', icon="💡")