# Import os to set API key
import os
# fitz to read in PDF files,
import fitz
# Bring in streamlit for UI/app interface
import streamlit as st
# Import the llama library to query LLMs
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, set_global_service_context
from llama_index.llms import ChatMessage, OpenAI
from llama_index.callbacks import CallbackManager, TokenCountingHandler
import openai
import tiktoken


def save_uploadedfile(uploadedfile):
    """
    function to save a file to data folder.
    """
    with open(os.path.join("data", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())


def display_pdf(file):
    """
    function to display the PDF of a given file
    """

    # read in pdf file to text
    doc = fitz.open(file)
    text = ""
    for page in doc:  # iterate the document pages
        text = text + page.get_text()  # get plain text encoded as UTF-8

    # Displaying the text
    st.text(text)


def create_job_profile(t, c):
    """
    function to create job profile for a given job title
    """
    # load from cache if the job description already existed
    if os.path.exists('data/' + t + '-' + c):
        with open('data/' + t + '-' + c, "r") as f:
            return f.read()
    else:
        # Generate Job Description from LLM
        messages = [
            ChatMessage(role="system",
                        content="You are a professtional recruiter"),
            ChatMessage(role="user",
                        content=f"Write a job description of {t} at {c}"),
        ]
        job_description = OpenAI().chat(messages)

        # Write Job Description to File to cache it
        with open(os.path.join("data", t + '-' + c), "w") as f:
            f.write(job_description.dict()["message"]['content'])
        return job_description.dict()["message"]['content']


# Set APIkey for OpenAI Service (Can sub this out for other LLM providers)
os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set Token Counter to calculate estimated cost. Here I used text-davinci-003, that's the default model of Llama Index
token_counter = TokenCountingHandler(
    tokenizer=tiktoken.encoding_for_model("text-davinci-003").encode
)
callback_manager = CallbackManager([token_counter])
service_context = ServiceContext.from_defaults(
    callback_manager=callback_manager)
set_global_service_context(service_context)
if 'count' not in st.session_state:
    st.session_state.count = 0

# Start building the UI
st.set_page_config(layout='wide')
st.title('Candidate Match')

# Create file uploader
uploaded_file = st.file_uploader(
    label="Upload Candidate Resume", type=['pdf'], accept_multiple_files=False)

if uploaded_file:
    # Save the upload file to data folder.
    save_uploadedfile(uploaded_file)
    col1, col2 = st.columns([1, 1])
    with col1:
        display_pdf("data/"+uploaded_file.name)
    with col2:
        title = st.text_input('Enter the job title')
        company = st.text_input('Enter the name of the company')

        if st.button('Match'):
            with st.spinner("Thinking..."):
                # Load the job profile based on the title-company, create from LLM if not already existed
                job_description = create_job_profile(title, company)

                # Load the resume + job profile to index
                documents = SimpleDirectoryReader(input_files=[
                    "data/"+uploaded_file.name]).load_data()
                index = VectorStoreIndex.from_documents(documents)
                query_engine = index.as_query_engine(streaming=True)

                # Pass to LLM
                streaming_response = query_engine.query(
                    "For the job profile: " + job_description + "\n If the resume doesn't match the job requirement or doesn't have relevant information, then output 'I think it's not a good fit' and stop. Otherwise, output 'I think it's a good fit' and provide a confident score with 3 rationales")
                # ...and write it out to the screen
                element = st.empty()
                streaming_text = ""
                for text in streaming_response.response_gen:
                    streaming_text += text
                    element.write(streaming_text)
                # Display the job profile
                job_expander = st.expander(
                    "See the job profile we are matching")
                job_expander.write(job_description)
                # Display the cost
                st.session_state.count += token_counter.total_llm_token_count
                COST = st.session_state.count / 1000 * 0.02
                st.write(f"Current Total Cost is ${COST}")
