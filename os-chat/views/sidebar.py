import streamlit as st
from icecream import ic

from database.pinecone_db import need_text_embedding
from utils.ai.open_ai import get_text_chunk, upsert


def sidebar_spinner():
    with st.spinner('Processing'):

        if need_text_embedding():
            # index not created and need run text embedding
            # Use loader and data splitter to make a document list
            st.write("Index didn't found. Will process Embeding for you.")
            doc = get_text_chunk()
            ic(f'text_chunks are generated and the total chucks are {len(doc)}')

            # Upsert data to the VectorStore
            print('Doc is ready for upsert!')
            upsert(doc)
            st.write(
                'Text embedding finished successfully. You can ask question now.',
            )
        else:
            st.write(
                'Index existed in Pinecone database. Skip text embedding. You can ask question directly.',
            )


def sidebar():
    with st.sidebar:
        st.subheader('Process the docs from github')
        st.write(
            'For brand new vector database, press Process to do text embedding first.:tada:',
        )
        st.write(
            'For now we only support :globe_with_meridians:https://dvc.org/. More sites will coming soon...',
        )

        # if the button is pressed
        if st.button('Text Embedding'):
            sidebar_spinner()
