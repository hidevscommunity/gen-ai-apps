import streamlit as st
import string
import random
import os
from information_retrieval import retrieve_info
from save_embeddings import train_and_save_embeddings

# Create the "embeddings" folder if it doesn't exist
EMBEDDINGS_FOLDER = "embeddings"
os.makedirs(EMBEDDINGS_FOLDER, exist_ok=True)

# Function to generate a random string (for the assistant's responses)
def random_string() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Function to perform chat actions
def chat_actions():
    user_input = st.session_state["chat_input"]
    
    # Append the user's message to the chat history
    st.session_state["chat_history"].append({"role": "user", "content": user_input})

    # Retrieve the assistant's response (you should replace this logic)
    assistant_response = retrieve_info(EMBEDDINGS_FOLDER, user_input)
    assistant_response = assistant_response.replace("<pad>", "")

    # Append the assistant's response to the chat history
    st.session_state["chat_history"].append({"role": "assistant", "content": assistant_response})

# Initialize chat history in session state if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Set page title and favicon
st.set_page_config(
    page_title="My Chat",
    page_icon=":robot_face:",  # You can change this to a URL of your favicon
)

# Create a Streamlit app
st.title("My Chat")

# Add tabs for Training and Chat Interface
tabs = st.sidebar.selectbox("Select a Tab", ["Training", "Chat"])

if tabs == "Training":
    st.write("This is the training tab where you can train the language model.")

    # Upload PDF files
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        st.write(f"{len(uploaded_files)} PDF files uploaded.")
        train_button = st.button("Train Model")
        
        if train_button:
            with st.spinner("Training in progress..."):
                train_and_save_embeddings(uploaded_files)
            st.success("Model trained and embeddings saved successfully!")

elif tabs == "Chat":
    # User input field
    user_input = st.chat_input("Enter your message")

    # Send button to trigger chat actions
    if user_input:
        st.session_state["chat_input"] = user_input
        chat_actions()

    # Display chat history
    for entry in st.session_state["chat_history"]:
        with st.chat_message(name=entry["role"]):
            st.write(entry["content"])
