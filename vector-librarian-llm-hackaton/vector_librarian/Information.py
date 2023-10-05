import streamlit as st

import client
from authentication import (
    default_auth_weaviate,
    user_auth_weaviate,
    user_auth_openai,
    openai_connection_status,
    weaviate_connection_status,
)


def app() -> None:
    st.set_page_config(
        page_title="Vector Librarian",
        page_icon="📚",
        layout="centered",
        menu_items={"Get help": None, "Report a bug": None},
    )

    st.title("📚 Vector Librarian")

    dr = client.instantiate_driver()

    st.markdown("""
    Vector Librarian is a retrieval augmented generative (RAG) application built with Streamlit, Weaviate, OpenAI, and
    Hamilton.
    """)

    st.header("🔑Credentials")

    left, right = st.columns(2)

    with left:
        st.subheader("OpenAI")
        st.markdown("""
            This application uses OpenAI for text embeddings and generative answers.
            Enter your API key below.
                    
            [Get started with OpenAI](https://platform.openai.com/account/api-keys)
        """)
        st.warning("Your OpenAI account will be charged for your usage.")
        user_auth_openai()

    with right:
        st.subheader("Weaviate")
        st.markdown("""
            The demo connects to a default Weaviate instance.
            Enter your credentials to connect to your instance.
                    
            [Get started with Weaviate](https://console.weaviate.cloud/)
        """)
        default_auth_weaviate()
        user_auth_weaviate()

    
    with st.sidebar:
        openai_connection_status()
        weaviate_connection_status()

        if st.session_state.get("WEAVIATE_DEFAULT_INSTANCE") is False:
            client.initialize(
                dr=dr,
                weaviate_client=st.session_state.get("WEAVIATE_CLIENT")
            )


if __name__ == "__main__":
    # run as a script to test streamlit app locally
    app()
