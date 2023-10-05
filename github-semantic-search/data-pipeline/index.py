import pandas as pd
import weaviate
import logging
import os

from dotenv import load_dotenv


def load_environment_vars() -> dict:
    """Load required environment variables. Raise an exception if any are missing."""

    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_api_key = os.getenv("WEAVIATE_API_KEY")

    if not openai_api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

    if not weaviate_url:
        raise EnvironmentError("WEAVIATE_URL environment variable not set.")

    if not weaviate_api_key:
        raise EnvironmentError(
            "WEAVIATE_API_KEY environment variable not set.")

    logging.info("Environment variables loaded.")
    return {"OPENAI_API_KEY": openai_api_key, "WEAVIATE_URL": weaviate_url, "WEAVIATE_API_KEY": weaviate_api_key}


def index_data(openai_api_key: str, weaviate_url: str, weaviate_api_key: str):
    """Index Data into Weaviate"""
    file_name = "./data-pipeline/langchain-github-issues-2023-09-18.pkl"

    logging.info(f"Loading data from '{file_name}'")
    df = pd.read_pickle(file_name)

    logging.info(f"Initializing Weaviate Client: '{weaviate_url}'")
    client = weaviate.Client(
        url=weaviate_url,
        auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_api_key),
        additional_headers={"X-OpenAI-Api-Key": openai_api_key})

    logging.info(
        f"Creating 'GituHubIssue' schema in Weaviate: '{weaviate_url}'")
    client.schema.delete_class("GitHubIssue")

    """
    Weaviate generates vector embeddings at the object level (rather than for individual properties).
    text2vec-* modules  generate vectors from text objects. 
    It vectorizes only properties that use the text data type (unless skipped)

    See: https://weaviate.io/developers/weaviate/config-refs/schema#vectorizer 
    """

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
    client.schema.create_class(class_obj)

    logging.info(f"Importing data to Weaviate: '{weaviate_url}'")

    try:
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
    except Exception as ex:
        logging.error(f"Unexpected Error: {ex}")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")

    try:
        env_vars = load_environment_vars()
        index_data(env_vars["OPENAI_API_KEY"],
                   env_vars["WEAVIATE_URL"], env_vars["WEAVIATE_API_KEY"])
    except EnvironmentError as ee:
        logging.error(f"Environment Error: {ee}")
        raise
    except Exception as ex:
        logging.error(f"Unexpected Error: {ex}")
        raise
