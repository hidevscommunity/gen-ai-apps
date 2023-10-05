"""
Streamlit app for GitHub Semantic Search with Weaviate.
It supports the following search modes:
- Near Text
- BM25
- Hybrid
The user's OpenAI API key is used to generate vector embeddings for the search query.

Author:
    @dcarpintero : https://github.com/dcarpintero
"""
import streamlit as st
import pandas as pd
import weaviate
import logging
import os

from dotenv import load_dotenv
from datetime import datetime
from typing import Optional


def load_environment_vars() -> dict:
    """Load required environment variables. Raise an exception if any are missing."""

    load_dotenv()
    openapi_key = os.getenv("OPENAI_API_KEY")
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_api_key = os.getenv("WEAVIATE_API_KEY")

    if not openapi_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

    if not weaviate_url:
        raise EnvironmentError("WEAVIATE_URL environment variable not set.")

    if not weaviate_api_key:
        raise EnvironmentError(
            "WEAVIATE_API_KEY environment variable not set.")

    logging.info("Environment variables loaded.")
    return {"OPENAI_API_KEY": openapi_key, "WEAVIATE_URL": weaviate_url, "WEAVIATE_API_KEY": weaviate_api_key}


@st.cache_resource(show_spinner=False)
def weaviate_client(openai_key: str, weaviate_url: str, weaviate_api_key: str):

    logging.info(f"Initializing Weaviate Client: '{weaviate_url}'")
    client = weaviate.Client(
        url=weaviate_url,
        auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_api_key),
        additional_headers={"X-OpenAI-Api-Key": openai_key})

    return client


@st.cache_data
def query_with_near_text(_w_client: weaviate.Client, query, max_results=10) -> pd.DataFrame:
    """
    Search GitHub Issues in Weaviate with Near Text.
    Weaviate converts the input query into a vector through the inference API (OpenAI) and uses that vector as the basis for a vector search.
    """

    response = (
        _w_client.query
        .get("GitHubIssue", ["title", "url", "labels", "description", "created_at", "state"])
        .with_near_text({"concepts": [query]})
        .with_limit(max_results)
        .do()
    )

    data = response["data"]["Get"]["GitHubIssue"]
    return pd.DataFrame.from_dict(data, orient='columns')


@st.cache_data
def query_with_bm25(_w_client: weaviate.Client, query, max_results=10) -> pd.DataFrame:
    """
    Search GitHub Issues in Weaviate with BM25.
    Keyword (also called a sparse vector search) search that looks for objects that contain the search terms in their properties according to 
    the selected tokenization. The results are scored according to the BM25F function. It is .
    """

    response = (
        _w_client.query
        .get("GitHubIssue", ["title", "url", "labels", "description", "created_at", "state"])
        .with_bm25(query=query)
        .with_limit(max_results)
        .with_additional("score")
        .do()
    )

    data = response["data"]["Get"]["GitHubIssue"]
    return pd.DataFrame.from_dict(data, orient='columns')


@st.cache_data
def query_with_hybrid(_w_client: weaviate.Client, query, max_results=10) -> pd.DataFrame:
    """
    Search GitHub Issues in Weaviate with BM25.
    Keyword (also called a sparse vector search) search that looks for objects that contain the search terms in their properties according to 
    the selected tokenization. The results are scored according to the BM25F function. It is .
    """

    response = (
        _w_client.query
        .get("GitHubIssue", ["title", "url", "labels", "description", "created_at", "state"])
        .with_hybrid(query=query)
        .with_limit(max_results)
        .with_additional(["score"])
        .do()
    )

    data = response["data"]["Get"]["GitHubIssue"]
    return pd.DataFrame.from_dict(data, orient='columns')


def onchange_with_near_text():
    if st.session_state.with_near_text:
        st.session_state.with_bm25 = False
        st.session_state.with_hybrid = False


def onchange_with_bm25():
    if st.session_state.with_bm25:
        st.session_state.with_near_text = False
        st.session_state.with_hybrid = False


def onchange_with_hybrid():
    if st.session_state.with_hybrid:
        st.session_state.with_near_text = False
        st.session_state.with_bm25 = False


def format_date(date_string: str) -> Optional[str]:
    try:
        date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    except:
        return None
    return date.strftime('%d %B %Y')


env_vars = load_environment_vars()
w_client = weaviate_client(
    env_vars["OPENAI_API_KEY"], env_vars["WEAVIATE_URL"], env_vars["WEAVIATE_API_KEY"])

st.header("🦜 Semantic Search on Langchain Issues 🔍")

with st.sidebar.expander("🐙 GITHUB-REPOSITORY", expanded=True):
    st.text_input(label='GITHUB-REPOSITORY', key='github_repo',
                  label_visibility='hidden', value='langchain-ai/langchain', disabled=True)

with st.sidebar.expander("🔧 WEAVIATE-SETTINGS", expanded=True):
    st.toggle('Near Text Search', key="with_near_text",
              on_change=onchange_with_near_text)
    st.toggle('BM25 Search', key="with_bm25", on_change=onchange_with_bm25)
    st.toggle('Hybrid Search',  key="with_hybrid",
              on_change=onchange_with_hybrid)

with st.sidebar.expander("🔍 SEARCH-RESULTS", expanded=True):
    bm25_score = st.slider('BM25 Score', min_value=1.0,
                           max_value=4.0, value=1.9, step=0.1)
    hybrid_score = st.slider('Hybrid Score (Scaled)',
                             min_value=1.0, max_value=3.0, value=1.1, step=0.05)
    max_results = st.slider('Max Results', min_value=0,
                            max_value=100, value=10, step=1)

with st.sidebar:
    "[![Weaviate Docs](https://img.shields.io/badge/Weaviate%20Docs-gray)](https://weaviate.io/developers/weaviate)"

query = st.text_input("Search in 'langchain-ai/langchain'", '')

if query:
    if st.session_state.with_near_text:
        st.subheader("Near Text Search")
        df = query_with_near_text(w_client, query, max_results)
    elif st.session_state.with_bm25:
        st.subheader("BM25 Search")
        df = query_with_bm25(w_client, query, max_results)
    elif st.session_state.with_hybrid:
        st.subheader("Hybrid Search")
        df = query_with_hybrid(w_client, query, max_results)
    else:
        st.info("ℹ️ Select your preferred Search Mode (Near Text, BM25 or Hybrid)!")
        st.stop()

    tab_list, tab_raw = st.tabs(
        [f'Issues with "{query}"', "Raw"])

    with tab_list:
        if df is None:
            st.info("No GitHub Issues found.")
        else:
            for i in range(1, len(df)):
                issue = df.iloc[i]

                if st.session_state.with_bm25:
                    score = issue["_additional"]["score"]
                    if float(score) < bm25_score:
                        break
                elif st.session_state.with_hybrid:
                    score = issue["_additional"]["score"]
                    if float(score) * 100 < hybrid_score:
                        break

                title = issue["title"]
                url = issue["url"]
                createdAt = format_date(issue["created_at"])

                st.markdown(f'[{title}]({url}) ({createdAt})')

    with tab_raw:
        if df is None:
            st.info("No GitHub Issues found.")
        else:
            st.dataframe(df, hide_index=True)
