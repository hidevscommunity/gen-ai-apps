import os
from langsmith import Client
from pprint import pprint
import logging


def send_comment(run_id,
                 comment,
                 score,
                 correction):
    client = Client(api_url="https://api.smith.langchain.com",
                    api_key=os.environ['LANGCHAIN_API_KEY'])
    feedback = client.create_feedback(
        run_id=run_id,
        key="left_comment",
        comment=comment,
        score=score,
        correction=correction
    )
    logging.info(feedback)

# if __name__ == "__main__":
#     send_comment(
#         run_id="1b4c62ee-a79c-426d-8467-78eb075facf5",
#         comment="Excellent hint generation",
#         score=0.7,
#         correction={"additional_explanation" : "The code runs in O(n) time"}
#     )