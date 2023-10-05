from typing import Optional
from langchain.tools import BaseTool
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS


from utils.callback import CustomHandler


class SummarizeDocumentsTool(BaseTool):
    name = "Summarize Documents"

    description = "This tool should be used immediately if a file path is not given"\
                  "Use this tool to summarize the content of documents"\
                  "The input to this tool must be a single element representing what to search for"
    vectorstore:FAISS
    paths = []

    def _run(self,input):
        
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k",streaming=True)
        chain = load_summarize_chain(llm, chain_type="stuff")
        retriever= self.vectorstore.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={'k':100000,'score_threshold': 0.7}
        )

        all_documents = retriever.get_relevant_documents(input)
        if(len(all_documents) == 0):
            return "No information found"
        return "Hello World"
    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")

