import streamlit as st
from PyPDF2 import PdfReader
from langchain.chains import LLMChain
from langchain.llms import OpenAI as LangchainOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import PromptTemplate
import time
import base64

st.set_page_config(page_title='UplAsk', page_icon ='🤖')

# Define a function to get image as base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set CSS style for the page
st.markdown("""
    <style>
    .centered {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Load and display header image
img_base64 = get_image_base64("images/header.png")
st.markdown(f'<p class="centered"><img src="data:image/png;base64,{img_base64}" style="max-width:200px; height:auto;"></p>', unsafe_allow_html=True)

# Page title and subtitle
st.markdown('<h1 class="centered">UplAsk</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="centered" style="font-size: smaller; font-style: italic;">Where Your Documents Find Answers</h2>', unsafe_allow_html=True)

# Add a rainbow divider
st.subheader('', divider='rainbow')

# How to Use UplAsk section
st.markdown("""
## How to Use UplAsk

⚠️ Important: In this app you can upload document and ask question on it. The documents you upload will be analyzed using OpenAI's services. This means the content of your documents will be shared with OpenAI for processing. Please be cautious when uploading sensitive or confidential information.

1. **Step 0: Enter Your OpenAI API Key:** Before using the app, please enter your OpenAI API key. The key is required to power the natural language processing features of this app.

2. **Step 1: Upload a Document:** Click the 'Upload a PDF' button to upload a document that you want summarized or from which you wish to retrieve information.

3. **Step 2: Wait for Processing:** UplAsk will read your document and provide a concise summary. This process uses advanced natural language understanding and can take a few seconds to a minute depending on the document's length.

4. **Step 3: Read the Summary:** Once the document has been processed, you can read the summary to get the gist of the document.

5. **Step 4: Ask Questions:** You can also ask questions related to the document in the chat interface. The AI has been trained to understand the context based on the document and the ongoing conversation.
""")

# Add a rainbow divider
st.subheader('', divider='rainbow')

# Initialize or get stored summaries from session state
if 'summaries' not in st.session_state:
    st.session_state.summaries = []

# Initialize message history and memory for chat
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs)
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

# Get OpenAI API Key
openai_api_key = st.secrets.get("openai_api_key")  
if not openai_api_key:
    openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Enter an OpenAI API Key to continue")
    st.stop()

st.subheader('', divider='rainbow')

# PDF Upload section
uploaded_file = st.file_uploader("Upload a PDF", type=['pdf'])

if uploaded_file:
    # Read the PDF
    reader = PdfReader(uploaded_file)
    num_pages = len(reader.pages)
    
    if not st.session_state.summaries:
        summaries = []
        summary_prompt_template = PromptTemplate(input_variables=["chunk"], template="Please summarize the following text:\n\n{chunk}")
        summary_llm_chain = LLMChain(llm=LangchainOpenAI(openai_api_key=openai_api_key), prompt=summary_prompt_template)

        for i, page in enumerate(reader.pages):
            chunk = page.extract_text()
            response = summary_llm_chain.run({"chunk": chunk})
            summaries.append(response.strip())
        
        st.session_state.summaries = summaries
    
    summaries_str = " ".join(st.session_state.summaries)

    # Add a rainbow divider
    st.subheader('', divider='rainbow')

    st.subheader("Document Summary")
    st.write(summaries_str)
    st.subheader('', divider='rainbow')
    
    # Chat interface
    chat_template = f"""You are an AI chatbot having a conversation with a human.

    {summaries_str}

    {{history}}
    Human: {{human_input}}
    AI: """
    chat_prompt = PromptTemplate(input_variables=["history", "human_input"], template=chat_template)
    chat_llm_chain = LLMChain(llm=LangchainOpenAI(openai_api_key=openai_api_key), prompt=chat_prompt, memory=memory)

    if prompt := st.chat_input(key="chat_input_key"):
        response = chat_llm_chain.run({"history": "", "human_input": prompt})

    # Display chat messages outside the expander
    for msg in msgs.messages:
        if msg.type == "human":
            st.chat_message("human").write(msg.content)
        elif msg.type == "ai":
            st.chat_message("ai").write(msg.content)

# Add a rainbow divider
st.subheader('', divider='rainbow')

# Add a footer with attribution
st.markdown('<p style="text-align:center;">Created with ❤️ by <a href="https://www.linkedin.com/in/mscherding/" target="_blank">Michaël</a></p>', unsafe_allow_html=True)
