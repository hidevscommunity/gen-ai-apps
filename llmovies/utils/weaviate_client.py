import os

import weaviate
from dotenv import load_dotenv

load_dotenv()

WEAVIATE_URL = os.environ["WEAVIATE_URL"]
WEAVIATE_KEY = os.environ["WEAVIATE_KEY"]
OPENAI_KEY = os.environ["OPENAI_API_KEY"]


client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=weaviate.AuthApiKey(WEAVIATE_KEY),
    additional_headers={"X-OpenAI-Api-Key": OPENAI_KEY},
)
