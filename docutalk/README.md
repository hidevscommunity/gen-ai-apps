# docutalk

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Clarifai](https://img.shields.io/badge/Clarifai-1955FF.svg?style=for-the-badge&logo=Clarifai&logoColor=white)
![LICENSE](https://img.shields.io/github/license/putuwaw/docutalk?style=for-the-badge)
![BUILD](https://img.shields.io/github/actions/workflow/status/putuwaw/docutalk/streamlit.yml?style=for-the-badge)

LLM-powered ChatBot with Document Knowledge Base using Streamlit, Clarifai, LangChain, and LlamaIndex.

## Features 🚀

With this app you can talk to the chatbot and ask about the Clarifai's documentation. The chatbot will answer your question based on the documentation that are provided [here](data/).

The data above was taken from [Clarifai's docs repository](https://github.com/Clarifai/docs/tree/main/docs).

## Prerequisites 📋

- Python 3.10 or higher
- Streamlit 1.26.0 or higher
- LangChain 0.0.285 or higher
- Clarifai 9.8.1 or higher
- LlamaIndex 0.8.26 or higher

## Installation 🛠

- Clone the repository:

```bash
git clone https://github.com/putuwaw/docutalk.git
```

- Install the packages:

```bash
pip install -r requirements.txt
```

- Set up secret for Persoanl Access Token (PAT) and enviroment:

```bash
cp .streamlit/secret.example.toml .streamlit/secrets.toml
```

- Run the application:

```bash
streamlit run app.py
```

## License 📝

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
