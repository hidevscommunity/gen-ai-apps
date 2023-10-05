import os
from llama_index import GPTVectorStoreIndex
from llama_index import StorageContext, load_index_from_storage
# from llama_index import download_loader
# https://llamahub.ai/l/youtube_transcript
from llama_hub.youtube_transcript.base import YoutubeTranscriptReader


import logging
import sys

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logging.basicConfig(stream=sys.stdout, level=logging.CRITICAL)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# There are five standard levels for logging in Python, listed here in increasing order of severity:
# DEBUG: Detailed information, typically of interest only when diagnosing problems.
# INFO: Confirmation that things are working as expected.
# WARNING: An indication that something unexpected happened or indicative of some problem in the near future (e.g., ‘disk space low’). The software is still working as expected.
# ERROR: Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL: A very serious error, indicating that the program itself may be unable to continue running.


class LlamaContext:
    def __init__(self, ytb_link, path=None, ):
        self.path = path if path is not None else None
        #
        # if path!=None:
        #     self.path = path
        # else:
        #     self.path = ''

        persist_sub_dir = "storage"
        self.persist_dir = os.path.join(self.path, persist_sub_dir)
        if not os.path.exists(self.persist_dir):
            os.makedirs(self.persist_dir)
        data_sub_dir = "data"
        self.data_dir = os.path.join(self.path, data_sub_dir)

        self.ytb_link = ytb_link

        self.cost_model_ada = "ada"  # https://openai.com/pricing
        self.cost_model_davinci = "davinci"  # https://openai.com/pricing
        self.price_ada_1k_tokens = 0.0004
        self.price_davinci_1k_tokens = 0.03

        self.documents = None
        self.ytb_content = None
        self.ytb_content_valid = False
        self.index = None
        # self.index_size = 0
        self.query_engine = None
        self.sleep = None
        self.response_cls = None
        self.response = None
        self.total_tokens = None
        self.total_cost_ada = None
        self.total_cost_davinci = None

    def extract_ytb(self):
        # youtube_transcript_reader = download_loader("YoutubeTranscriptReader")
        # loader = youtube_transcript_reader()
        loader = YoutubeTranscriptReader()
        try:
            self.documents = loader.load_data(ytlinks=[self.ytb_link])
            self.ytb_content = self.documents[0].text
            if self.documents is not None:
                self.ytb_content_valid = True
            else:
                self.ytb_content_valid = False
        except:
            self.ytb_content = "Can't extract text from link!"
            self.ytb_content_valid = False

    def create_vector_store(self):
        if self.documents is not None:
            self.index = GPTVectorStoreIndex.from_documents(self.documents)
            # self.index_size = sys.getsizeof(self.index.vector_store.to_dict())
            # print("GPTVectorStoreIndex complete.")

    def save_index(self):
        self.index.storage_context.persist(persist_dir=self.persist_dir)
        print(f"Index saved in path {self.persist_dir}.")

    def load_index(self):
        storage_context = StorageContext.from_defaults(persist_dir=self.persist_dir)
        self.index = load_index_from_storage(storage_context)

    def start_query_engine(self):
        self.query_engine = self.index.as_query_engine()
        print("Query_engine started.")

    def post_question(self, question, sleep=None):
        if sleep is None:
            self.sleep = 0  # trial 20s
        self.response_cls = self.query_engine.query(question)
        self.response = self.response_cls.response

    def estimate_tokens(self, text):
        words = text.split()

        num_words = int(len(words))
        tokens = int((num_words / 0.75))
        tokens_1k = tokens / 1000
        cost_ada = tokens_1k * self.price_ada_1k_tokens
        cost_davinci = tokens_1k * self.price_davinci_1k_tokens
        return tokens, cost_ada, cost_davinci

    def estimate_cost(self):
        total_tokens = 0
        total_cost_ada = 0
        total_cost_davinci = 0
        costs_rounding = 8
        if self.ytb_content_valid:
            for doc in self.documents:
                text = doc.get_text()
                tokens, cost_ada, cost_davinci = self.estimate_tokens(text)
                total_tokens += tokens

                total_cost_ada += cost_ada
                total_cost_ada = round(total_cost_ada, costs_rounding)

                total_cost_davinci += cost_davinci
                total_cost_davinci = round(total_cost_davinci, costs_rounding)

        self.total_tokens = total_tokens
        self.total_cost_ada = total_cost_ada
        self.total_cost_davinci = total_cost_davinci
