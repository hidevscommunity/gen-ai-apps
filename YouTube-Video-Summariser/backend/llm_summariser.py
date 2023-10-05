import assemblyai as aai
import toml
import random
from itertools import cycle
import streamlit as st

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_apikey(connector, item):
    logger = logging.getLogger(f"{__name__}.get_apikey")
    logger.info(f"Getting API key from secrets.toml [{connector}][{item}]")
    secrets = toml.load(".streamlit/secrets.toml")
    result = secrets[connector][item]
    logger.debug(f"result: {result}")
    return result


def cycled_apikey(connector, num_keys):
    logger = logging.getLogger(f"{__name__}.cycled_apikey")
    logger.setLevel(logging.INFO)
    logger.debug(f"connector: {connector}")
    logger.debug(f"num_keys: {num_keys}")
    key_indexes = list(range(1, num_keys + 1))
    logger.debug(f"key_indexes: {key_indexes}")
    all_api_keys = [
        get_apikey(connector, f"api_key_{key_index}") for key_index in key_indexes
    ]
    logger.debug(f"all_api_keys: {all_api_keys}")
    api_key_genertor = cycle(all_api_keys)
    logger.info(f"api_key_genertor: {api_key_genertor}")
    return api_key_genertor


def analyse_audio(FILE_URL):
    logger = logging.getLogger(f"{__name__}.analyse_audio")
    logger.setLevel(logging.INFO)
    logger.info("Running AI Assembly LLM model")

    # replace with your API token
    api_keygen = cycled_apikey("ai-assembly", 2)

    def transcribe(api_keygen=api_keygen):
        logger.debug("transcribing...")
        api_key = next(api_keygen)
        aai.settings.api_key = api_key

        # URL of the file to transcribe
        config = aai.TranscriptionConfig(
            iab_categories=True,
            summarization=True,
            summary_model=aai.SummarizationModel.informative,  # optional
            # summary_type=aai.SummarizationType.gist,  # does not work out of the box
            # summary_type=aai.SummarizationType.headline,  # works
            # summary_type=aai.SummarizationType.paragraph,  # optional
            summary_type=aai.SummarizationType.bullets,  # works
            # summary_type=aai.SummarizationType.bullets_verbose,
        )

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(FILE_URL, config=config)

        try:
            response = {
                "summary": transcript.summary,
                "label_relevance": transcript.iab_categories.summary,
                "results": transcript.iab_categories.results,
            }
        except AttributeError:
            logger.debug("Attribute error - repsonse returned None")
            response = None

        return response

    response = transcribe()
    attempt_cutoff = 10
    attempts = 0
    while response is None:
        logger.debug(f"connection attempts: {attempts}")
        attempts += 1
        try:
            logger.debug(f"attempts > attempt_cutoff: {attempts > attempt_cutoff}")
            if attempts > attempt_cutoff:
                st.error("API connection failed. Please try again later.")
                break
            else:
                logger.debug("while loop - pass")
                pass
            response = transcribe()
        except:
            st.error("API Key is not working. Please try again later.")

    return response


if __name__ == "__main__":

    def get_apikey(connector, item):
        logger = logging.getLogger(f"{__name__}.get_apikey")
        logger.info(f"Getting API key from secrets.toml [{connector}][{item}]")
        secrets = toml.load(".streamlit/secrets.toml")
        result = secrets[connector][item]
        logger.debug(f"result: {result}")
        return result

    api_key_pool = cycled_apikey("ai-assembly", 2)
    logger.debug(next(api_key_pool))
