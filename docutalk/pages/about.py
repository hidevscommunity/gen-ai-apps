import streamlit as st

st.set_page_config(
    page_title="DocuTalk - About",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

st.title("💬 DocuTalk")


'''
DocuTalk is a LLM-based Streamlit app that can talk about Clarifai's documentation.
This app is designed for [LLM Hackaton](https://streamlit.io/community/llm-hackathon-2023) submission.
'''

st.subheader("Features")
'''
DocuTalk also address common LLM pain like:
- **Transparency** - DocuTalk use document retrieval as a source of knowledge so helps users understand the basis for the LLM's responses.
- **Trust** - Beside that, users are more likely to trust the information when they know it comes from reliable in this case are Clarifai's documentation.
- **Accuracy** - DocuTalk has access up-to-date, factual information from documentation, which can improve the accuracy of responses.
'''

st.subheader("Tech Stack")
'''
Tech stack used in this app are:
'''
tech1, tech2, tech3, tech4 = st.columns(4)
with tech1:
    st.image("https://github.com/streamlit.png", width=100)
    st.write("[Streamlit](https://streamlit.io/)")
with tech2:
    st.image("https://github.com/langchain-ai.png", width=100)
    st.write("[LangChain](https://www.langchain.com/)")
with tech3:
    st.image("https://github.com/clarifai.png", width=100)
    st.write("[Clarifai](https://www.llamaindex.ai/)")
with tech4:
    st.image("https://aeiljuispo.cloudimg.io/v7/https://cdn-uploads.huggingface.co/production/uploads/6424f01ea4f3051f54dbbd85/oqVQ04b5KiGt5WOWJmYt8.png?w=200&h=200", width=100)
    st.write("[LlamaIndex](https://www.llamaindex.ai/)")

st.subheader("")

st.subheader("Source Code")
st.markdown(
    "More detail about the source code available on GitHub: [![Open in GitHub](https://img.shields.io/badge/Open_in_GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/putuwaw/docutalk)")
