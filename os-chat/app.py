import streamlit as st
from icecream import ic
from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
from langchain.vectorstores import Pinecone

import public
from config import open_ai, pinecone
from config.constants import INDEX_NAME, MODE, PRODUCTION
from config.log import setup_log
from utils.ai.open_ai import create_or_get_conversation_chain
from views.home import home

st.set_page_config(
    page_title='OpenSource Chat',
    page_icon=':books:',
)  # TODO: release
st.write(public.css_index, unsafe_allow_html=True)


def main():
    if MODE == PRODUCTION:
        ic.disable()

    setup_log()

    open_ai.setup()
    pinecone.setup()

    embeddings = OpenAIEmbeddings()
    vectorstore = Pinecone.from_existing_index(
        index_name=INDEX_NAME, embedding=embeddings,
    )

    st.session_state.conversation = create_or_get_conversation_chain(
        vectorstore,
    )

    home()


# to run this application, you need to run "streamlit run app.py"
if __name__ == '__main__':
    main()
