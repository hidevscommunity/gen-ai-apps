import streamlit as st
import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader


st.set_page_config(page_title="💬Chat with the ChinaStartupInsight" , page_icon="💬", layout="centered", initial_sidebar_state="auto", menu_items=None)
# openai.api_key = st.secrets.openai_key
## hide
openai.api_key = st.secrets["openapi_key"]
##

st.title("Chat with the ChinaStartupInsight 💬")
st.info("ChinaStartupInsight is your gateway to exploring the dynamic landscape of the Chinese startup market. With this service, you can ask ChatGPT-style questions to gather comprehensive information and insights about entering the Chinese startup ecosystem.Discover the latest trends, regulations, investment opportunities, and cultural nuances that are crucial for success in the Chinese startup scene. Whether you're an entrepreneur looking to expand your business into China or an investor seeking to tap into this burgeoning market, ChinaStartupInsight provides you with the knowledge and guidance you need to navigate the complexities of the Chinese startup ecosystem.", icon="📃")
         
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Startup ecosystem in China"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading our Data – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the startup ecosystem in china and your job is to answer questions about it. Assume that all questions are related to the startup and Investment ecosystem in China. Keep your answers based on facts – do not hallucinate features."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index
        

index = load_data()
# chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features.")
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
