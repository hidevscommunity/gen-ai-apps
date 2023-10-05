from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.document_loaders import PyPDFLoader
import tempfile
import os
# Create the "embeddings" folder if it doesn't exist
EMBEDDINGS_FOLDER = "embeddings"
os.makedirs(EMBEDDINGS_FOLDER, exist_ok=True)

# Define a function to load PDF documents from uploaded files
def pdf_loader(uploaded_files):
    loaders = [PyPDFLoader(pdf_path) for pdf_path in uploaded_files]
    return loaders

# Define a function to train the model and save embeddings
def train_and_save_embeddings(uploaded_files):
    temp_dir = tempfile.TemporaryDirectory()
    temp_paths = []

    try:
        for uploaded_file in uploaded_files:
            # Save the uploaded file to a temporary directory
            with open(os.path.join(temp_dir.name, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.read())
            temp_paths.append(os.path.join(temp_dir.name, uploaded_file.name))

        loaders = pdf_loader(temp_paths)
        documents = []
        for loader in loaders:
            documents.extend(loader.load())

        embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        texts = text_splitter.split_documents(documents)
        db = FAISS.from_documents(texts, embeddings)

        # Save embeddings to the "embeddings" folder
        embeddings_folder = os.path.join(EMBEDDINGS_FOLDER, "")
        os.makedirs(embeddings_folder, exist_ok=True)
        db.save_local(embeddings_folder)

    finally:
        temp_dir.cleanup()