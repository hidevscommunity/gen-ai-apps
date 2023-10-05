import streamlit as st
import re
import requests
import streamlit.components.v1 as components
URL1="https://org-clarifai.streamlit.app/?embed=true"
url = st.experimental_get_query_params().get("url", URL1)[0]
new_url = st.text_input(
    "Enter a new URL of a Streamlit app", value=url)

data = requests.get(new_url)
html = data.text
st.write(html1)

#render = html1.render()

#st.write(render)

#browser = session.browser()
#st.write(browser)

#st.write(data)
#st.write(dir(data))
#st.write(data.__dict__)

#st.write(session)
#st.write(dir(session))
#st.write(session.__dict__)

# embed streamlit docs in a streamlit app
#data = requests.get(
#st.write(data.text)
#st.write(data.encoding)
#st.write(data.content)

st.write(new_url)


st.experimental_set_query_params(
    url =new_url)
