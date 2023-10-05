import streamlit as st

def display_sidebar():
    st.sidebar.title('How to Use Multilingual Menu 👨‍🍳🍳')
    st.sidebar.markdown('- **Upload** images of ingredients or **type** them in.')
    st.sidebar.markdown('- Enter the **culinary style** you desire.')
    st.sidebar.markdown('- Specify the **language** for the menu.')
    st.sidebar.markdown('- Click "Generate Recipe" for results, a recipe will be displayed; otherwise, warning messages will guide the user.')
    st.sidebar.markdown('- Watch the **demo video** for a visual guide.')

    st.sidebar.title('Limitations')
    st.sidebar.markdown('- The accuracy of the ingredient prediction is dependent on the Clarifai model being used..')
    st.sidebar.markdown('- Recipe generation is based on the provided template and might not always result in a fully detailed or traditional recipe.')
