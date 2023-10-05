import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from typing import List

SYSTEM_PROMT = """You are an expert on responding questions your job is to answer technical questions. 
                Keep your answers technical and based on facts, do not hallucinate features.
                If the topic is not ethical or is illegal respond "I can not give my opinion on this topic"
                """
TEMPERATURE = 0.5
OPENAI_MODEL = "gpt-3.5-turbo"


def texts2index(docs: List[str]) -> VectorStoreIndex:
    """ 
    From a list of text create a VectoreStoreIndex
    """

    temperature = st.slider("Temperature", min_value=0.1,
                            max_value=1.0, step=0.1, value=TEMPERATURE)

    # Initialize a Spinner widget to show indexing progress
    with st.spinner(text="Indexing the docs – hang tight! This should take minutes."):
        # Create a service context for the OpenAI model
        service_context = ServiceContext.from_defaults(llm=OpenAI(
            model=OPENAI_MODEL, temperature=temperature, system_prompt=SYSTEM_PROMT))
        # Create a VectorStoreIndex from the Document objects
        index = VectorStoreIndex.from_documents(
            docs, service_context=service_context)

    return index


def load_data() -> List[str]:
    """
    Load txt files from a computer, return a List[str]
    """
    text_list = []

    # Use Streamlit's file_uploader widget to allow users to upload multiple TXT files
    uploaded_files = st.file_uploader(
        "Choose TXT files (one or more)", accept_multiple_files=True)

    for uploaded_file in uploaded_files:

        # Check if the file has a ".txt" extension
        if uploaded_file.name.endswith(".txt"):
            # Read the content of the text file
            bytes_data = uploaded_file.read()
            st.write("Loaded:", uploaded_file.name)

            # Append the decoded text to the text_list
            text_list.append(bytes_data.decode())  # Assuming it's a text file
        else:
            # Display a message for skipped files that are not TXT files
            st.write(f"Skipped file: {uploaded_file.name} (Not a TXT file)")

    # Create a list of Document objects using the extracted text
    docs = [Document(text=t) for t in text_list]

    return docs


def chat(index: VectorStoreIndex):
    """
    Chat with a LLM based on an Index
    """

    chat_engine = index.as_chat_engine(
        chat_mode="condense_question", verbose=True)
    # Prompt for user input and save to chat history
    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append(
            {"role": "user", "content": prompt})

    for message in st.session_state.messages:  # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant",
                           "content": response.response}
                # Add response to message history
                st.session_state.messages.append(message)


def main():

    index = None
    st.set_page_config(page_title="CHAT",
                       page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)

    st.title("Engage in a conversation with the documents you can provide in TXT format!, powered by LlamaIndex 💬🦙")

    api_key = st.secrets.openai_key  # Load API_KEY FROM secrets if there is defined

    if api_key == "":
        api_key = st.text_input(
            "Enter your API Key of OpenAI", type="password")

    st.info("Using " + OPENAI_MODEL +
            " with private keys, be careful it have a cost", icon="📃")

    if "messages" not in st.session_state.keys():  # Initialize the chat messages history
        st.session_state.messages = [
            {"role": "assistant",
                "content": "Ask me a question about the TXT files you have upload! :)"}
        ]

    texts = load_data()

    
    if not api_key:
        st.warning("Please enter the API Key")
    elif not texts:
        st.warning("Please upload the TXT files")
    else:

        openai.api_key = api_key # Set the API key to use OpenAI

        try:
            index = texts2index(texts)
            chat(index)
        except:
            st.warning("Problems creating a index")

if __name__ == "__main__":
    main()
