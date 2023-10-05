[![Open_inStreamlit](https://img.shields.io/badge/Open%20In-Streamlit-red?logo=Streamlit)](https://gh-semantic-search.streamlit.app/)
[![Python](https://img.shields.io/badge/python-%203.8-blue.svg)](https://www.python.org/)
[![CodeFactor](https://www.codefactor.io/repository/github/dcarpintero/github-semantic-search/badge)](https://www.codefactor.io/repository/github/dcarpintero/github-semantic-search)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://github.com/dcarpintero/st-newsapi-connector/blob/main/LICENSE)

# 🦜 Semantic Search on Langchain Github Issues with Weaviate 🔍

<p align="center">
  <img src="./static/github-semantic-search.png">
</p>

##  🔍 What's Semantic Search?

> *Semantic search refers to search algorithms that consider the intent and contextual meaning of search phrases when generating results, rather than solely focusing on keyword matching. The goal is to provide more accurate and relevant results by understanding the semantics, or meaning, behind the query.*

## 📋 How does it work?

- **Ingesting Github Issues**: We use the [Langchain Github Loader](https://js.langchain.com/docs/modules/data_connection/document_loaders/integrations/web_loaders/github)  to connect to the [Langchain Repository](http://github.com/langchain-ai/langchain) and fetch the GitHub issues (nearly 2.000), which are then converted to a pandas dataframe and stored in a pickle file. See [./data-pipeline/ingest.py](./data-pipeline/ingest.py).

- **Generate and Index Vector Embeddings with Weaviate**: Weaviate generates vector embeddings at the object level (rather than for individual properties), it includes by default properties that use the text data type, in our case we skip the 'url' field (which will be also not filterable and not searchable) and set up the 'text2vec-openai' vectorizer. Given that our use case values fast queries over loading time, we have opted for the [HNSW](https://arxiv.org/abs/1603.09320) vector index type, which incrementally builds a multi-layer structure consisting from hierarchical set of proximity graphs (layers).

```python
class_obj = {
        "class": "GitHubIssue",
        "description": "This class contains GitHub Issues from the langchain repository.",
        "vectorIndexType": "hnsw",
        "vectorizer": "text2vec-openai",
        "moduleConfig": {
            "text2vec-openai": {
                "model": "ada",
                "modelVersion": "002",
                "type": "text"
            }
        },
        "properties": [
            {
                "name": "title",
                "dataType": ["text"]
            },
            {
                "name": "url",
                "dataType": ["text"],
                "indexFilterable": False,  
                "indexSearchable": False,
                "vectorizePropertyName": False
            },
            {
                "name": "description",
                "dataType": ["text"]
            },
            {
                "name": "creator",
                "dataType": ["text"],
            },
            {
                "name": "created_at",
                "dataType": ["date"]
            },
            {
                "name": "state",
                "dataType": ["text"],
            },
        ]
    }
```

The ingestion follows in batches of 100 records:

```python
with client.batch as batch: 
    batch.batch_size = 100
    for item in df.itertuples():
        properties = {
            "title": item.title,
            "url": item.url,
            "labels": item.labels,
            "description": item.description,
            "creator": item.creator,
            "created_at": item.created_at,
            "state": item.state,
        }

        batch.add_data_object(
            data_object=properties, 
            class_name="GitHubIssue")
```

- **Searching with Weaviate**: Our App supports:

[Near-Text-Vector-Search](https://weaviate.io/developers/weaviate/search/similarity):

```python
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
    return  pd.DataFrame.from_dict(data, orient='columns')
```

[BM25-Search](https://weaviate.io/developers/weaviate/search/bm25):

```python
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
    return  pd.DataFrame.from_dict(data, orient='columns')
```

[Hybrid-Search](https://weaviate.io/developers/weaviate/search/hybrid):

```python
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
```

## 🚀 Quickstart

1. Clone the repository:
```
git@github.com:dcarpintero/github-semantic-search.git
```

2. Create and Activate a Virtual Environment:

```
Windows:

py -m venv .venv
.venv\scripts\activate

macOS/Linux

python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Ingest Data
```
python ./data-pipeline/ingest.py
```

5. Index Data
```
python ./data-pipeline/index.py
```

6. Launch Web Application

```
streamlit run ./app.py
```

## 👩‍💻 Streamlit Web App

Demo Web App deployed to [Streamlit Cloud](https://streamlit.io/cloud) and available at https://gh-semantic-search.streamlit.app/ 

## 📚 References

- [Langchain Document Loaders - Github](https://js.langchain.com/docs/modules/data_connection/document_loaders/integrations/web_loaders/github)
- [Weaviate Vector Search](https://weaviate.io/developers/weaviate/search/similarity)
- [Weaviate BM25 Search](https://weaviate.io/developers/weaviate/search/bm25)
- [Weaviate Hybrid Search](https://weaviate.io/developers/weaviate/search/hybrid)
- [Weaviate Schema Configuration](https://weaviate.io/developers/weaviate/configuration/schema-configuration)
- [Weaviate - How to efficiently add data objects and cross-references to Weaviate](https://weaviate.io/developers/weaviate/manage-data/import)
- [Get Started with Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud/get-started)