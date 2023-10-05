import os
from llama_index import download_loader, SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.node_parser import SimpleNodeParser
from llama_index.vector_stores import WeaviateVectorStore
from pathlib import Path


def parse_doc(doc_path):
    if doc_path[-3:] == "txt":
        documents = SimpleDirectoryReader(input_files=[doc_path]).load_data()
    else:
        if doc_path[-3:] == "pdf":
            pdf_reader = download_loader("PDFReader")
            loader = pdf_reader() 
        else:
            docx_reader = download_loader("DocxReader")
            loader = docx_reader()
        documents = loader.load_data(file=Path(doc_path))

    parser = SimpleNodeParser.from_defaults(chunk_size=512, chunk_overlap=20)
    nodes = parser.get_nodes_from_documents(documents)

    return nodes


def create_index(doc_list, w_client, index_name):
    node_list = []
    for doc in doc_list:
        doc_path = os.path.join("cache", doc.name)
        with open(doc_path, "wb") as f:
            f.write(doc.getvalue()) 
        nodes = parse_doc(doc_path)
        node_list += nodes
        os.remove(doc_path)
   
    vector_store = WeaviateVectorStore(weaviate_client=w_client, index_name=index_name, text_key="content")
    storage_context = StorageContext.from_defaults(vector_store = vector_store)
    index = VectorStoreIndex(node_list, storage_context=storage_context)
    return index


def retrieve_context(index, query_text):
    print(query_text)
    retriever = index.as_retriever(similarity_top_k=4)
    response = retriever.retrieve(query_text)
    print(len(response))
    # print(response)

    response_text = "\n\n".join(map(lambda x: x.text, response))
    return response_text