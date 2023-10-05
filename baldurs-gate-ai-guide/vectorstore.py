import os

import faiss
import openai
from dotenv import load_dotenv
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index import (Document, ServiceContext, StorageContext,
                         VectorStoreIndex, load_index_from_storage)
from llama_index.embeddings import LangchainEmbedding, OpenAIEmbedding
from llama_index.llms import OpenAI
from llama_index.node_parser import SimpleNodeParser
from llama_index.schema import MetadataMode
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores.faiss import FaissVectorStore

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

# dimensions of text-ada-embedding-002
d = 1536
faiss_index = faiss.IndexFlatL2(d)

node_parser = SimpleNodeParser.from_defaults(chunk_size=1300, chunk_overlap=200)

embed_model = OpenAIEmbedding(embed_batch_size=10)

BALDURS_GATE_3_ALL_ACTS_METADATA = [
  {
    "act": 1,
    "documents_path": "./documents/knowledge_base/act_1",
    "description": "Tips and guides for Baldur's Gate 3's Act 1.",
    "type": "quest"
  },
  {
    "act": 2,
    "documents_path": "./documents/knowledge_base/act_2",
    "description": "Tips and guides for Baldur's Gate 3's Act 2.",
    "type": "quest"
  },
  {
    "act": 3,
    "documents_path": "./documents/knowledge_base/act_3",
    "description": "Tips and guides for Baldur's Gate 3's Act 3.",
    "type": "quest"
  },
  {
    "act": 0,
    "documents_path": "./documents/knowledge_base/characters",
    "description": "Tips and guides for Baldur's Gate 3's player companions and NPCs.",
    "type": "character"
  },
]


# Create a new Chroma Database and save to disk
print("Loading or Creating Chroma Database")
# db = chromadb.PersistentClient(path="./chroma_db") # ToDo: Maybe change this to Chroma Reader?
# quests_guide_collection = db.get_or_create_collection("baldurs_gate_3_quests_guide")
# vector_store = ChromaVectorStore(chroma_collection=quests_guide_collection)

vector_store = FaissVectorStore(faiss_index=faiss_index)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(embed_model=embed_model, node_parser=node_parser)
service_context_query_engine = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4", temperature=0))

index = None

# If the vectorstore doesn't have any documents, create a new index
if not os.path.isdir("./storage"): # This means the Chroma collection (or index) is brand new
  print("Started loading documents using Llama Index")
  
  documents = []

  for metadata in BALDURS_GATE_3_ALL_ACTS_METADATA:
    file_names_in_directory = []
    
    if "documents_path" in metadata:
          try:
              filenames = os.listdir(metadata["documents_path"]) # Using os.listdir to get a list of all files in the directory
              for filename in filenames:
                  file_names_in_directory.append(filename)
          except FileNotFoundError:
              print(f"Directory '{metadata['documents_path']}' not found.")
              
    for filename in file_names_in_directory:
      with open(metadata["documents_path"] + "/" + filename, 'r') as f:
            text_content = f.read()
            
      document = Document(
        text=text_content,
        metadata={
            "act": metadata["act"],
            "description": metadata["description"],
            "name": os.path.splitext(filename)[0],
            "document_path": metadata["documents_path"] + "/" + filename,
            "category": "quest",
        },
        excluded_llm_metadata_keys=['document_path'],
        metadata_seperator="::",
        metadata_template="{key}=>{value}",
        text_template="Metadata: {metadata_str}\n-----\nContent: {content}")
      
      documents.append(document)
  print("Finished loading documents using Llama Index")
      
  print("Adding documents to vectorstore")
  index = VectorStoreIndex.from_documents(
      documents, storage_context=storage_context, service_context=service_context
  )
  
  # print("The LLM sees this: \n", documents[0].get_content(metadata_mode=MetadataMode.LLM))
  # print("The Embedding model sees this: \n", documents[0].get_content(metadata_mode=MetadataMode.EMBED))
  
  # save index to disk
  index.storage_context.persist()

# If the vectorstore has documents, load the existing index
else:
  print("Started loading vectorstore using Llama Index")
  vector_store = FaissVectorStore.from_persist_dir("./storage")
  storage_context = StorageContext.from_defaults(
      vector_store=vector_store, persist_dir="./storage"
  )
  index = load_index_from_storage(storage_context=storage_context)

# Query Data
print("Initialize query engine")
query_engine = index.as_query_engine(verbose=True, streaming=False, service_context=service_context_query_engine, similarity_top_k=6)


if __name__ == "__main__":
  while True:
    user_query = input("\nEnter your query: ")
    response = query_engine.query(user_query)
    retrieved_nodes = response.source_nodes
    print(response)
    
    # response.print_response_stream()
    
    # Citing sources (nodes)
    # for i, source_node in enumerate(response.source_nodes):
    #   print(f"Source node {i+1}: {source_node.node.get_content()}")
  
  