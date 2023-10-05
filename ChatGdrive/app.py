"""This is a public module. It should have a docstring."""
import os
import pickle
import webbrowser
from typing import List, Tuple

import gdown
import streamlit as st
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import (
    AgentTokenBufferMemory,
)
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import MessagesPlaceholder
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

st.set_page_config(page_title="ChatGdrive", page_icon="📚")

starter_message = "Ask me anything about your Gdrive folder!"


@st.cache_resource
def create_prompt(openai_api_key: str) -> Tuple[SystemMessage, ChatOpenAI]:
    """Create prompt."""
    # Make your OpenAI API request here
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        streaming=True,
        openai_api_key=openai_api_key,
    )

    message = SystemMessage(
        content=(
            "You are a helpful chatbot who is tasked with answering questions about context given the chunk of files content."  # noqa: E501 comment
            "Unless otherwise explicitly stated, it is probably fair to assume that questions are about the context given provided."  # noqa: E501 comment
            "If there is any ambiguity, you probably assume they are about that."  # noqa: E501 comment
        )
    )

    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name="history")],
    )

    return prompt, llm


@st.cache_data
def list_files_recursive(dir_path: str) -> List[str]:
    """List all files in a directory recursively."""
    all_files = []

    # Walk through directory, including subdirectories
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # Construct the full path to the file
            full_path = os.path.join(root, file)
            all_files.append(full_path)

    return all_files


@st.cache_data
def load_docs2(dir_path: str) -> str:
    """Load and process the uploaded PDF files."""
    documents = []
    # get list of files from dir_path
    list_of_files = list_files_recursive(dir_path)
    print(f"found {len(list_of_files)} files")
    for file in list_of_files:
        if file.endswith(".pdf"):
            pages = PyPDFLoader(file)
            documents.extend(pages.load())
        else:
            print(f"skipping {file}")

    return ",".join([doc.page_content for doc in documents])


@st.cache_data
def generate_embeddings() -> HuggingFaceEmbeddings:
    """Generate embeddings for given model."""
    embeddings = HuggingFaceEmbeddings(
        cache_folder="hf_model"
    )  # https://github.com/UKPLab/sentence-transformers/issues/1828
    return embeddings


@st.cache_resource
def process_corpus(corpus: str, chunk_size: int = 1000, overlap: int = 50) -> List:
    """Process text for Semantic Search."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap
    )

    texts = text_splitter.split_text(corpus)

    # Display the number of text chunks
    num_chunks = len(texts)
    st.write(f"Number of text chunks: {num_chunks}")

    # select embedding model
    embeddings = generate_embeddings()

    # create vectorstore
    vectorstore = FAISS.from_texts(texts, embeddings).as_retriever(
        search_kwargs={"k": 2}
    )

    # create retriever tool
    tool = create_retriever_tool(
        vectorstore,
        "search_docs",
        "Searches and returns documents using the context provided as a source, relevant to the user input question.",  # noqa: E501 comment
    )

    tools = [tool]
    return tools


@st.cache_data
def generate_agent_executer(text: str) -> List[AgentExecutor]:
    """Generate the memory functionality."""
    tools = process_corpus(text)
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
    # Synthwave

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True,
    )
    return agent_executor


@st.cache_resource
def create_temp_folder(temp_dir: str = "./temp_dir") -> None:
    """Create a temp folder."""
    if not os.path.exists(temp_dir):
        # Create the temporary directory if it does not exist
        os.makedirs(temp_dir)
    else:
        # Cleanup
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))


@st.cache_resource
def extract_gdrive_directory(gdrive_dir_link: str, temp_dir: str) -> None:
    """Extract the Google Drive directory to the temporary directory."""
    # gdrive_dir_link = 'https://drive.google.com/drive/folders/1rrLTxL8K4TUVSsQHx2bgLiLqGKsp7yU2' -O temp_dir --folder # noqa: E501 comment
    # temp_dir = "./temp_dir"
    status = gdown.download_folder(url=gdrive_dir_link, output=temp_dir)
    if status is None:
        st.error(
            "Cannot retrieve the folder information from the link. You may need to\nchange the permission to 'Anyone with the link!",  # noqa: E501 comment
            icon="🚨",
        )


# Add custom CSS
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;
    # }
        footer {visibility: hidden;
        }
        .css-card {
            border-radius: 0px;
            padding: 30px 10px 10px 10px;
            background-color: black;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 10px;
            font-family: "IBM Plex Sans", sans-serif;
        }
        .card-tag {
            border-radius: 0px;
            padding: 1px 5px 1px 5px;
            margin-bottom: 10px;
            position: absolute;
            left: 0px;
            top: 0px;
            font-size: 0.6rem;
            font-family: "IBM Plex Sans", sans-serif;
            color: white;
            background-color: green;
            }
        .css-zt5igj {left:0;
        }
        span.css-10trblm {margin-left:0;
        }
        div.css-1kyxreq {margin-top: -40px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.write(
    """
<div style="display: flex; align-items: center; margin-left: 0;">
    <h1 style="display: inline-block;">InQuest</h1>
    <sup style="margin-left:5px;font-size:small; color: green;">beta</sup>
</div>
""",
    unsafe_allow_html=True,
)

# Build sidebar
with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", key="api_key_openai", type="password"
    )
    if openai_api_key and openai_api_key.startswith("sk-"):
        prompt, llm = create_prompt(openai_api_key)
        memory = AgentTokenBufferMemory(llm=llm)
        "[here OpenAI API key](https://platform.openai.com/account/api-keys)"
    else:
        st.info("Please add your correct OpenAI API key in the sidebar.")

# If there's no OpenAI API key, show a message and stop the app for rendering further
if not openai_api_key:
    st.info("Please add your OpenAI API key in the sidebar.")
    st.stop()

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [AIMessage(content=starter_message)]

for msg in st.session_state.messages:
    if isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)
    elif isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    memory.chat_memory.add_message(msg)


@st.cache_resource
def generate_response(_retriever, _llm, query_text: str) -> str:
    """Generate response."""
    qa = RetrievalQA.from_chain_type(_llm, chain_type="stuff", retriever=_retriever)
    return qa.run(query_text)


tab1, tab2 = st.tabs(["embed", "search & chat"])

with tab1:
    if st.button("Coonect to Grive"):
        webbrowser.open_new_tab("https://drive.google.com")

    gdrive_dir_link = st.text_input("Enter the Google Drive Directory URL:")

    # Add a placeholder for the user input
    if st.button("Embedd folder"):
        with st.spinner("Embedding folder..."):
            # name the temp folder
            temp_dir = "./temp_dir"

            # create a temporary folder
            create_temp_folder()
            st.success("Temporary folder created")

            # Download the Google Drive directory to the temporary directory
            # The Google Drive directory must have the required permissions
            extract_gdrive_directory(gdrive_dir_link, temp_dir)
            st.success("Documents downloaded")

            raw_pdf_text = load_docs2(temp_dir)
            st.success("Documents processed")

            chunk_size = 1000
            overlap = 50

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=overlap
            )

            texts = text_splitter.split_text(raw_pdf_text)

            # select embedding model
            embeddings = generate_embeddings()

            # create vectorstore
            vectorstore = FAISS.from_texts(texts, embeddings).as_retriever(
                search_kwargs={"k": 2, "search_type": "similarity_score"}
            )

            # save vectorstore into pickle
            with open("my_variable.pkl", "wb") as f:
                pickle.dump(vectorstore, f)

        st.success("Embeddings generated.")


# Initialize session_state if it hasn't been initialized
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None


@st.cache_data
def load_vdb():
    """Load vectorstore."""
    with open("my_variable.pkl", "rb") as f:
        vectorstore = pickle.load(f)
    return vectorstore


with tab2:
    st.header("Search and Chat")
    if st.button("Load folder", key="load_folder_tab2"):
        st.session_state.vectorstore = load_vdb()

        prompt, llm = create_prompt(openai_api_key)

        tool = create_retriever_tool(
            st.session_state.vectorstore,
            "search_docs",
            "Searches and returns documents using the context provided as a source, relevant to the user input question.",  # noqa: E501 comment
        )

        agent = OpenAIFunctionsAgent(llm=llm, tools=[tool], prompt=prompt)
        # Synthwave

        agent_executor = AgentExecutor(
            agent=agent,
            tools=[tool],
            verbose=True,
            return_intermediate_steps=True,
        )

        st.session_state["agent_executor"] = agent_executor
        st.success("Loaded Embeddings.")

    query_text = st.text_input(
        "Enter your question:", placeholder="Please provide a short summary."
    )  # , disabled=not st.button("Load folder"

    # Form input and query
    result = []
    with st.form("myform", clear_on_submit=True):
        submitted = st.form_submit_button("Submit", disabled=not (query_text))
        if submitted and st.session_state.vectorstore is not None:
            with st.spinner("Calculating..."):
                response = st.session_state.vectorstore.get_relevant_documents(
                    query_text
                )
                result.append(response)

    if len(result):
        st.info(response)

st.subheader("Chat with the bot")
if user_question := st.chat_input(
    placeholder=starter_message,
    key="chat_input_tab3",
    disabled=st.session_state.vectorstore == None,
):
    st.chat_message("user").write(user_question)

    # added this because of the error
    if st.session_state["agent_executor"] is not None:
        agent_executor = st.session_state["agent_executor"]

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(
            st.container(),
            expand_new_thoughts=True,
            collapse_completed_thoughts=True,
            thought_labeler=None,
        )

        response = agent_executor(
            {"input": user_question, "history": st.session_state.messages},
            callbacks=[st_callback],
            include_run_info=True,
        )
        st.session_state.messages.append(AIMessage(content=response["output"]))

        st.write(response["output"])

        memory.save_context({"input": user_question}, response)

        st.session_state["messages"] = memory.buffer

        run_id = response["__run"].run_id

        col_blank, col_text, col1, col2 = st.columns([10, 2, 1, 1])
