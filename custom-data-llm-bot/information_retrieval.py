import time
from langchain.vectorstores import FAISS  # Change the vector store to Faiss
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.chains import RetrievalQA

# Load the pre-trained T5 model and tokenizer for LLM
tokenizer = AutoTokenizer.from_pretrained("lmsys/fastchat-t5-3b-v1.0")
model = AutoModelForSeq2SeqLM.from_pretrained("lmsys/fastchat-t5-3b-v1.0")

pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=256, trust_remote_code=True)
local_llm = HuggingFacePipeline(pipeline=pipe)

start = time.time()
instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
end = time.time()
print("Instructor Embedding model loading time", (end - start))


def retrieve_info(embedding_path, input_query):
    embeddings = instructor_embeddings
    start = time.time()
    print("loading.....")
    # Load the instructor embedding model
    db = FAISS.load_local(embedding_path, embeddings)
    end = time.time()
    print("Embeddings from db time", (end - start))

    # Create the retriever from the vector store
    retriever = db.as_retriever()

    # Create the chain to answer questions using the RetrievalQA
    qa_chain = RetrievalQA.from_chain_type(llm=local_llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
    print("retrieval defined")
    start = time.time()
    query = input_query
    print("The query is:", query)
    result = qa_chain({"query": query}) # Query result with source documents and content
    result_value = result['result'] # result value alone
    end = time.time()
    print("Query answering time", (end - start))
    print("Answer is:", result_value)
    return result_value
