import asyncio

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

import streamlit as st
#import requests_html 
import re
import streamlit.components.v1 as components
from requests_html import HTMLSession, HTML

URL1="https://org-clarifai.streamlit.app/?embed=true"

# Get the URL of the app to run from the query parameter or use a default value
url = st.experimental_get_query_params().get("url", URL1)[0]

# Display a text input to let the user enter a new URL
new_url = st.text_input("Enter a new URL of a Streamlit app", value=url)


session = HTMLSession()

data = session.get(new_url)

#html =  data.html

html = data.html.render()

#html1 = HTML(session=session,
#            url=new_url,
#            html=html)

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

#Once the iframe is embedded, you can access the data from the embedded app using the `st.session_state` object. For example, if the embedded app has a variable called `data`, you can access it in your app as follows:

for d in st.session_state:
    data = st.session_state[d]
    st.write(d,data)
st.write(new_url)


st.experimental_set_query_params(
    url =new_url)
