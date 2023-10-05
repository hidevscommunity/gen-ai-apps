from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import toml
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def api_keygen():
    secrets = toml.load(".streamlit/secrets.toml")
    api_key = secrets["open-ai"]["api_key"]
    return api_key


def analyse_reviews(reviews, openai_api_key):
    logger = logging.getLogger(f"{__name__}.analyse_reviews")
    logger.setLevel(logging.DEBUG)
    logger.debug(openai_api_key)
    llm = OpenAI(openai_api_key=openai_api_key)

    prompt = """
    Reviews:
    {reviews}

    Provide a paragraph summarising the key themes and sentiments in the Amazon product reviews.
    Provide short bullet point summmaries highlighting the key positive and negative points made about the product.
    Include some specific details from the customer reviews about the product itself.
    Also provide the average rating in the form of 'Average rating: X out of 5 stars' where X is the average rating.

    Your answer should follow this format:

    [average rating]

    [pararaph summary]

    Positives:
    - xxxxxx
    - xxxxxx

    Negatives:
    - xxxxxx
    - xxxxxx
    
    """

    prompt.format(reviews=str(reviews))

    result = llm(prompt)
    logger.debug(result)
    return result


if __name__ == "__main__":
    reviews = {
        "Review 1": {
            "title": "Lid was broken before even used it",
            "body-text": "Lid broken before I could use it I ordered a couple and they all came the same",
            "rating": "1.0 out of 5 stars",
        },
        "Review 2": {
            "title": "Smells nice",
            "body-text": "Good smells lovely and gets rid of unwanted smells would stick to this brand",
            "rating": "5.0 out of 5 stars",
        },
        "Review 3": {
            "title": "Best spray on the market",
            "body-text": "Smells very nice...lasts a long time",
            "rating": "5.0 out of 5 stars",
        },
        "Review 4": {
            "title": "Works",
            "body-text": "Clears unwanted smells quickly leaving the air smelling lovely.",
            "rating": "4.0 out of 5 stars",
        },
    }

    api_key = api_keygen()

    analyse_reviews(reviews=reviews, openai_api_key=api_key)
