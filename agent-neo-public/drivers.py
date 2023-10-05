import streamlit as st
from neo4j import GraphDatabase

def init_driver(uri, username, password):
    """
        Initiate the Neo4j Driver
    """
    d = GraphDatabase.driver(uri, auth=(username, password))
    d.verify_connectivity()
    print('driver created')
    return d

def get_driver():
    """
    Get the instance of the Neo4j Driver created in the `initDriver` function
    """

    return st.session_state.driver

def close_driver():
    """
    If the driver has been instantiated, close it and all remaining open sessions
    """

    if st.session_state.driver != None:
        st.session_state.driver.close()
        st.session_state.driver = None

        return st.session_state.driver
