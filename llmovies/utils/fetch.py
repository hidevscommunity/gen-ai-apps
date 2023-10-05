import asyncio
import os
from typing import Any

import aiohttp
import pandas as pd
from dotenv import load_dotenv
from enums import Providers
from tqdm.asyncio import tqdm_asyncio

TMDB_MAX_PAGES = 500


def _get_ids(responses: list[dict[str, list[dict[str, Any]]]]) -> list[int]:
    id_collection = []
    for res in responses:
        for title in res["results"]:
            id_collection.append(title.get("id"))
    return list(set(id_collection))


def _build_headers(api_key: str) -> dict[str, str]:
    return {"accept": "application/json", "Authorization": f"Bearer {api_key}"}


async def discover_movies(
    session,
    page: int,
    provider: str,
    headers: dict[str, str],
    semaphore: asyncio.Semaphore,
):
    parameters = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": page,
        "watch_region": "US",
        "with_watch_providers": provider,
    }
    async with semaphore:
        url = "https://api.themoviedb.org/3/discover/movie"
        async with session.get(url, params=parameters, headers=headers) as response:
            return await response.json()


async def fetch_movie_details(
    session, movie_id: int, headers: dict[str, str], semaphore: asyncio.Semaphore
):
    async with semaphore:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {
            "append_to_response": "videos,watch/providers",
            "language": "en-US"
        }
        async with session.get(url, params=params, headers=headers) as response:
            return await response.json()


async def main_discover(
    provider: str, headers: dict[str, str], max_concurrent_requests: int
) -> list[dict[str, list[dict[str, Any]]]]:
    semaphore = asyncio.Semaphore(max_concurrent_requests)
    async with aiohttp.ClientSession() as session:
        first_page = await discover_movies(session, 1, provider, headers, semaphore)
        total_pages = min(first_page["total_pages"] + 1, TMDB_MAX_PAGES)
        tasks = [
            discover_movies(session, page, provider, headers, semaphore)
            for page in range(1, total_pages)
        ]
        responses = await tqdm_asyncio.gather(
            *tasks, desc=f"Discovering provider_id = '{provider}' movies"
        )
        return responses


async def main_details(
    movie_ids, headers: dict[str, str], max_concurrent_requests: int
):
    semaphore = asyncio.Semaphore(max_concurrent_requests)
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_movie_details(session, movie_id, headers, semaphore)
            for movie_id in movie_ids
        ]
        responses = await tqdm_asyncio.gather(*tasks, desc="Fetching movie details")
        return responses


# TODO: Improve this function
def _find_trailer(videos_results: list[dict]) -> str | None:
    for vid in videos_results:
        is_trailer = vid["type"] == "Trailer"
        is_official = vid["official"]

        if is_trailer and is_official:
            return vid["key"]
        elif is_trailer and not is_official:
            backup_trailer = vid.get("key")
    try:
        return backup_trailer
    except NameError:
        return None


def _find_provider_url(providers: dict) -> str | None:
    return providers["US"].get("link")


def _find_all_providers(providers: dict) -> list[str]:
    prov = providers["US"].get("flatrate")
    return [p["provider_id"] for p in prov] if prov else None


def _find_genre(genres: dict) -> str:
    gen = [g["name"] for g in genres]
    return ", ".join(gen)


def to_pandas(results: list[dict[str, Any]]) -> pd.DataFrame:
    return pd.json_normalize(results, max_level=1)


if __name__ == "__main__":
    load_dotenv()
    ACCESS_TOKEN = os.environ["TMDB_ACCESS_TOKEN"]

    PROVIDERS = [
        Providers.Netflix.value,
        Providers.DisenyPlus.value,
        Providers.Max.value,
        Providers.Hulu.value,
        Providers.AmazonPrimeVideo.value,
        Providers.AmazonVideo.value,
    ]
    MAX_CONCURRENCY = 3

    headers = _build_headers(ACCESS_TOKEN)
    search_results = []
    for provider in PROVIDERS:
        search_results += asyncio.run(main_discover(provider, headers, MAX_CONCURRENCY))
    movie_ids = _get_ids(search_results)

    details = asyncio.run(
        main_details(movie_ids, headers, max_concurrent_requests=MAX_CONCURRENCY)
    )
    movies = to_pandas(details)
    movies_with_trailers = movies.assign(
        trailer=lambda df: df["videos.results"].apply(_find_trailer),
        provider_url=lambda df: df["watch/providers.results"].apply(_find_provider_url),
        providers=lambda df: df["watch/providers.results"].apply(_find_all_providers),
        genres_list=lambda df: df["genres"].apply(_find_genre),
    )

    movies_with_trailers.dropna(subset=['providers'], inplace=True)
    if not os.path.exists("data"):
        os.makedirs("data")
    movies_with_trailers.to_parquet("data/final_movies.parquet")
