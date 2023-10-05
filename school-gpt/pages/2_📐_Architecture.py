import streamlit as st


st.set_page_config(page_title='Architecture of School GPT',
                   page_icon='📐',
                )

with st.sidebar:
    st.image('./resources/OIG1.png')

st.markdown('### `For nerds out there, here is an overview of how School GPT is powered`', unsafe_allow_html=True)

st.image('./resources/arc3.png')
st.info('You can click the :green[arrow] at :orange[top right] of the image to enlarge it', icon="💡")