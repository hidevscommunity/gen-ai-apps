import os

import openai
import streamlit as st
from dotenv import load_dotenv
from utils.enums import Providers
from utils.exceptions import LLMoviesOutputError
from utils.input import get_best_docs
from utils.utils import load_css

st.set_page_config(
    page_title="LLMovies | Your go-to companion for movie nights",
    page_icon="🍿",
    layout="wide",
)


def show_trailer(video: str | None):
    if video:
        st.video(f"https://www.youtube.com/watch?v={video}")
    else:
        st.video(f"https://www.youtube.com/watch?v=dQw4w9WgXcQ")


def get_provider_name(provider_id: str):
    return Providers(provider_id).name


def unsafe_html(html: str) -> st._DeltaGenerator:
    return st.markdown(html, unsafe_allow_html=True)


def genre_tags(genres: list[str]) -> str:
    li = "".join(f"<span class='genre-tag'>{genre}</span>" for genre in genres)
    return f"""
    <div class="genre-tags">{li}</div>
    """


def format_runtime(runtime: int) -> str:
    hours = runtime // 60
    minutes = runtime % 60
    return f"{hours}h {minutes}m"


# -- APP --


def main():
    load_dotenv()
    # Initialize search_params and user_input
    docs = None
    button_input = None
    user_input = None
    load_css("assets/custom.css")
    unsafe_html(
        '<script src="https://kit.fontawesome.com/6a637d33a1.js" crossorigin="anonymous"></script>'
    )
    unsafe_html("<h1 id='title'>🍿 LLMovies</h1>")
    unsafe_html("<p id='subtitle''>Your go-to companion for movie nights</p>")
    with st.sidebar:
        # TODO: Remove default value in production
        st.subheader("LLMovies")
        st.write(
            "LLMovies is an user-friendly application that simplifies your movie selection process. Search for a topic, genre, or movie and LLMovies will return 3 tailored trailers."
        )

        st.subheader("Features")
        st.markdown(
            """
            - **AI-based Retrieval**:  Uses state of the art LangChain retrievers to transform natural language intro structured database queries.
            - **Weaviate integration**: Offers semantic search capabilities.
            - **Broad catalog**: Complies 25,000+ movies from The Movie Database.
            - **Trusted measures**: Employs IMDb's ratings and review.
            """
        )

        st.subheader("Get started 🚀")
        openai_key = st.text_input(
            "Insert your OpenAI API key 🔑",
            type="password",
            value=os.getenv("OPENAI_KEY"),
            help="Not required during evaluation phase for ease of use."
        )


        st.multiselect(
            "Select your streaming services 🎬",
            [p.value for p in Providers],
            format_func=get_provider_name,
            placeholder="Netflix, Hulu...",
            key="providers",
        )


        st.subheader("Try me out! 🤖", help="Examples do not use the streaming service filter.")
        q1 = "I'd like to watch a movie about friendship with a rating higher than 7.0."
        if st.button(q1):
            button_input = q1

        q2 = "Can you recommend a comedy located in Italy released after 2015.0?"
        if st.button(q2):
            button_input = q2

        q3 = "Do you know any thrillers with a rating higher than 8.0 and more than 1000.0 reviews?"
        if st.button(q3):
            button_input = q3

        st.caption(
            "This product uses the TMDB API but is not endorsed or certified by TMDB."
        )

    if openai_key is None:
        st.warning("Hey! 🌟 Pop in your API key, and let's kick things off!")
        st.stop()
    openai.api_key = openai_key
    
    if st.session_state.providers == []:
        st.warning("👈 Ready to roll? Select your streaming services!")
        st.stop()
    
    default_user_input = button_input if button_input is not None else ""
    user_input = st.text_input(
        "Search", value=default_user_input, placeholder="Serch for a topic, a genre ..."
    )
    if user_input != "" or button_input is not None:
        input = button_input if button_input is not None else user_input
        try:
            docs = get_best_docs(input, providers=st.session_state.providers)    
        except openai.error.AuthenticationError:
            st.error(
                "Oops! It seems like your API key took a little detour. 🙃 Double-check and make sure it's the right one, will ya?"
            )
            st.stop()
        except ValueError:
            st.error(
                "Oops! 🎈 Let's keep things floaty. Please use floating point numbers (e.g., 10.5) instead of whole integers."
            )
            st.stop()

    if docs is not None:
        try:
            # Renders final recommendations
            cols = st.columns(3)

            for idx, movie in enumerate(docs):
                meta = movie.metadata
                with cols[idx]:
                    unsafe_html(f"<h3 class='movie-title'>{meta['title']} </h3>")
                    unsafe_html(
                        f"""
                        <ul class="list-inline">
                        <li>{meta['release_year']}</li>
                        <li>{format_runtime(meta['runtime'])}</li>
                        <li><i class="fa-solid fa-star"></i>{meta['imdb_vote_average'] or 0:.1f}/10</li>
                        </ul>
                        """
                    )
                    show_trailer(meta["trailer_url"])
                    unsafe_html(genre_tags(meta["genres"]))
                    unsafe_html(
                        f"""
                        <a href="{meta['watch']}" target="_blank" class="rounded-button-link">
                            <button class="rounded-button">Watch now</button>
                        </a>
                        """
                    )
                    unsafe_html(f"<div class='truncate'>{movie.page_content}</div>")

        except LLMoviesOutputError:
            st.write(
                "I wasn't able to find any movies for you. Try modifying your query."
            )


if __name__ == "__main__":
    main()
