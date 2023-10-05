import openai

from config.constants import OPENAI_API_KEY, OPENAI_ORGANIZATION_ID


def setup():
    openai.api_key = OPENAI_API_KEY
    openai.organization = OPENAI_ORGANIZATION_ID
