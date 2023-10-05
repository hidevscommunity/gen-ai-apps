import streamlit as st
from dotenv import load_dotenv
import pickle
from PyPDF2 import PdfReader
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os

os.environ['OPENAI_API_KEY'] = ''

# Sidebar contents
with st.sidebar:
    st.title('PDF Interactor')
    st.markdown('''
    ## About
    This is an LLM that enables you to interact with your PDF files, and seamlessly interact
                 with PDF documents, allowing for real-time discussions, annotations, and 
                sharing of insights. Whether you're collaborating with colleagues, reviewing 
                reports, or providing feedback on documents, This simplifies the process by
                transforming your PDFs into dynamic, interactive communication hubs. 
                Say goodbye to static PDFs and hello to LLM enhaced PDF communication, where conversations and 
                collaboration come to life within your documents.
 
    ''')
    add_vertical_space(5)

load_dotenv()


def main():
    st.header("Interact with your \'PDF\' 🗂️")
    pdf = st.file_uploader("Upload your PDF", type='pdf')

    st.write(pdf)
    if pdf is not None:
        pdf_reader = PdfReader(pdf)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text=text)

        store_name = pdf.name[:-4]
        st.write(f'{store_name}')
        # st.write(chunks)

        if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)
            st.write('Embeddings Loaded from the Disk')
        else:
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(VectorStore, f)

        embeddings = OpenAIEmbeddings()
        VectorStore = FAISS.from_texts(chunks, embedding=embeddings)

        query = st.text_input("Ask questions about your PDF file:")
        # st.write(query)

        if query:
            docs = VectorStore.similarity_search(query=query, k=3)
            llm = OpenAI()
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=query)
                print(cb)
            st.write(response)


if __name__ == '__main__':
    main()
