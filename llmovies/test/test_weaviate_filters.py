import sys

sys.path.append("/Users/joselondono/Documents/projects/llmovies/utils")

from utils.simple_chat import query_weaviate
from utils.weaviate_client import client


def test_query_with_genre():
    q = query_weaviate("Thieves", ["8"], "Action", 10, client)
    assert all(["Action" in x["genres"] for x in q])


def test_query_with_multiple_genres():
    q = query_weaviate("Thieves", ["8"], ["Action", "Comedy"], 10, client)
    assert all([("Action" in x["genres"]) or ("Comedy" in x["genres"]) for x in q])
    
    
def test_query_with_no_genres():
    max_results = 10
    q = query_weaviate("Thieves", ["8"], None, max_results, client)
    assert len(q)  == max_results