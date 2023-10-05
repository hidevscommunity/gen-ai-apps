import streamlit as st
import openai
import langchain

def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title(" 👼 Chat with God")
role = st.radio(
    "What's your Beliefs",
    ["***Christianity***", "***Iislam***", "***Hinduism***", "***Confucianism***"],
    captions = ["Laugh out loud.", "Get the popcorn.", "Never stop learning."])

content = ""
if role == '***Christianity***':
    content = "Hi! I'm an AI Bible Scholar. I'm able to answer any questions you have that might be answered in the Bible. Feel free to describe a current situation you're in, reference a Bible verse, or ask me a question."
elif role == '**Iislam***':
    content = "Hi! I'm an AI Quran Scholar. I'm able to answer any questions you have that might be answered in the Quran. Feel free to describe a current situation you're in, reference a Quran verse, or ask me a question."
elif role == '***Hinduism***':
    content = "Hi! I'm an AI Bhagavad Gita Scholar. I'm able to answer any questions you have that might be answered in the Bhagavad Gita. Feel free to describe a current situation you're in, reference a Bhagavad Gita verse, or ask me a question."
elif role == '***Confucianism***':
    content = "Hi! I'm an AI Confucianism Scholar. I'm able to answer any questions you have that might be answered in the Analects (more books coming soon). Feel free to describe a current situation you're in, reference a Analects verse, or ask me a question."

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": content}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Any questions?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)


