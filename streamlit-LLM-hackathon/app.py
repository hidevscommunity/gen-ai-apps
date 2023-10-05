import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader

openai.api_key = st.secrets.openai_key

"# WDI Historian Chatbot 💬👷‍♀️✨"

"""
This app is an example of an openai-powered chatbot using
llama index.

View the full app code
[here](https://github.com/aaronarcade/streamlit-LLM-hackathon).
Disney information sources: [D23 - Disney Archives](https://d23.com/walt-disney-archives/).
"""

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about WED or Imagineering!"},
        {"role": "assistant", "content": "Examples: What is WDI? Who is John Hench? What are Mickey's Ten Commandments? - or ask me what I can talk about!"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading publicly available WDI docs – please excuse our pixie dust, this will only take a moment."):
        reader = SimpleDirectoryReader(input_dir="data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on Walt Disney Imagineering and WED Enterprises and your job is to answer questions about WDI and WED history. Assume that all questions are related to the Disney and Imagineering. Keep your answers technical or based on historic facts – do not hallucinate information. Give 2-3 sentences context with each response. You may discuss Aaron Brown."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history

