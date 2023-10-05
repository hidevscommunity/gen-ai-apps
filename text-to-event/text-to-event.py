import streamlit as st
from io import StringIO
import ics
import re
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from prompt_template import PROMPT_TEMPLATE

st.set_page_config(page_title="text-to-event", layout="wide")
st.title("text-to-event")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    st.write("You can find your Secret API key in your [OpenAI User settings](https://beta.openai.com/account/api-keys).")

left, right = st.columns([3, 2])
with left:
    st.subheader('Enter text below:')
    st.text_area("", key="text", height=120)
with right:
    st.subheader('Or upload .txt file here:')
    file = st.file_uploader("", accept_multiple_files=False)

user_input = ""
if st.button("Submit"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    if st.session_state.text:
        user_input = st.session_state.text
    elif file:
        try:
            stringio = StringIO(file.getvalue().decode("utf-8"))
            user_input = stringio.read()
        except:
            st.info(":red[ERROR:] File format not accepted. Provide a file in .txt format.")
    else:
        st.info("No input.")

if user_input:
    prompt = PromptTemplate(input_variables=["user_input"], template=PROMPT_TEMPLATE)
    llm = OpenAI(model_name="text-davinci-003", openai_api_key=openai_api_key)
    answer = llm(prompt.format(user_input=user_input))

    cleaned_answer = answer.replace("\n", "")
    pattern = r"^NAME: ([\w\s'-]+)LOCATION: ([\w\s'-]+)START: ([\w\s'-:]+)END: ([\w\s'-:]+)DESCRIPTION: ([\w\s'-]+)"
    regex = re.compile(pattern)
    parsed_answer = regex.match(cleaned_answer).groups()

    c = ics.Calendar()
    e = ics.Event()
    e.name = parsed_answer[0]
    e.location = parsed_answer[1]
    e.begin = parsed_answer[2]
    e.end = parsed_answer[3]
    e.description = parsed_answer[4]
    c.events.add(e)

    result = "NAME: " + e.name + "  \n LOCATION: " + e.location + \
             "  \n START: " + str(e.begin) + "  \n END: " + str(e.end) + "  \n DESCRIPTION: " + str(e.description)

    st.write("# Event Summary:\n", result)
    with open('event.ics', 'w') as f:
        f.writelines(c.serialize_iter())

    st.download_button('Downloads .ics file', open('event.ics'), file_name='event.ics')
