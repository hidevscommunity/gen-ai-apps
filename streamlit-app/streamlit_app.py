import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.llms import OpenAI
import openai
from llama_index import download_loader
# from llama_hub.pdf_table.base import PDFTableReader
from pydantic import BaseModel, Field
from pathlib import Path

# Define your desired data structure.
class Food(BaseModel):
    time_limits: str = Field(description="time limits of storing the food")

@st.cache_resource(show_spinner=False)
def load_data(openai_api_key):
    # target_path_1 = os.path.join(os.path.dirname(__file__), 'target_1.txt')
    with st.spinner(text="Loading and indexing the docs about food safety - hang tight! This should take 1-2 minutes."):
        docs = []
        # pdf_table_reader = PDFTableReader()
        # pdf_table_path1 = Path('E:\streamlit\streamlit-app\data\Cold Food Storage Chart.pdf')
        # path = Path('./data/Cold Food Storage Chart.pdf').resolve()
        # print("absolute path: ", path.__str__)
        # documents = pdf_table_reader.load_data(file=pdf_table_path1, pages='all')
        # docs = docs + documents

        # pdf_table_path2 = Path('E:\streamlit\streamlit-app\data\Food Safety During Power Outage.pdf')
        # documents = pdf_table_reader.load_data(file=pdf_table_path2, pages='all')
        # docs = docs + documents

        pdf_reader = download_loader("PDFReader", custom_path="./local")
        pdf_path = Path('./data/steps_to_food_safety.pdf')
        loader = pdf_reader()
        documents = loader.load_data(file=pdf_path)
        docs = docs + documents

        pdf_path = Path('./data/Cutting Boards.pdf')
        documents = loader.load_data(file=pdf_path)
        docs = docs + documents

        pdf_path = Path('./data/Food Storage Guide.pdf')
        documents = loader.load_data(file=pdf_path)
        docs = docs + documents

        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", api_key=openai_api_key, temperature=0.5, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

def main():
    with st.sidebar:
        openai_api_key = st.text_input('OpenAI API Key')
    
    st.header("Chat about food storage 💬 📚")

    tab_chat, tab_storage = st.tabs(["💬 Chat", "🍛 Storage tips"])
    
    if prompt := st.chat_input("Sample question: How long can fresh broccoli be stored in a refrigerator?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
        st.stop()

    if "messages" not in st.session_state.keys(): # Initialize the chat message history
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question about food storage!"}
        ]

    # Load data from documents
    index = load_data(openai_api_key)
    chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
    
    with tab_storage:
        st.subheader('Check the time limits for home-refrigerated foods')

        food = st.text_input(label='Food', value='broccoli')
        place = st.radio(label="where to put the food", options=["refrigerator", "freezer"], index=0)
        
        if st.button("Search", type="primary"):
            storage_prompt = "How long do you suggest that I keep {food} in a {place}?".format(food=food.lower(), place=place)
            storage_response = chat_engine.chat(storage_prompt)
            st.write(storage_response.response)

    with tab_chat:
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

if __name__ == '__main__':
    main()

# import streamlit as st
# from langchain.llms import OpenAI

# st.title('🦜🔗 Quickstart App')

# openai_api_key = st.sidebar.text_input('OpenAI API Key')

# def generate_response(input_text):
#   llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
#   st.info(llm(input_text))

# with st.form('my_form'):
#   text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
#   submitted = st.form_submit_button('Submit')
#   if not openai_api_key.startswith('sk-'):
#     st.warning('Please enter your OpenAI API key!', icon='⚠')
#   if submitted and openai_api_key.startswith('sk-'):
#     generate_response(text)
