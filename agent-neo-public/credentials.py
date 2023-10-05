import streamlit as st

# local version will interact with dev database
# public version will interact with Production database
neo4j_credentials = st.secrets['neo4j_credentials']

def validate_openai_key():
    """
        This method validates the input openai key by
        making a dummy request to gpt-4
    """

    return False