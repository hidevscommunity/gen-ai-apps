
from hamilton import driver
from streamlit.runtime.uploaded_file_manager import UploadedFile
import weaviate

from backend import ingestion, retrieval, vector_db, arxiv_module


def instantiate_driver() -> driver.Driver:
    """Instantiate a Hamilton Driver"""
    return (
        driver.Builder()
        .enable_dynamic_execution(allow_experimental_mode=True)
        .with_modules(arxiv_module, ingestion, retrieval, vector_db)
        .build()
    )


def initialize(dr: driver.Driver, weaviate_client: weaviate.Client) -> None:
    """Initialize the Weaviate instance by creating classes"""
    dr.execute(
        ["initialize_weaviate_instance"],
        overrides=dict(weaviate_client=weaviate_client)
    )


def store_arxiv(dr: driver.Driver, weaviate_client: weaviate.Client, arxiv_ids: list[str]) -> None:
    """Retrieve PDF files of arxiv articles for arxiv_ids
    Read the PDF as text, create chunks, and embed them using OpenAI API
    Store chunks with embeddings in Weaviate.
    """
    dr.execute(
        ["store_documents"],
        inputs=dict(
            arxiv_ids=arxiv_ids,
            embedding_model_name="text-embedding-ada-002",
            data_dir="./data",
        ),
        overrides=dict(weaviate_client=weaviate_client)
    )


def store_pdfs(dr: driver.Driver, weaviate_client: weaviate.Client, pdf_files: list[UploadedFile]) -> None:
    """For each PDF file, read as text, create chunks, and embed them using OpenAI API
    Store chunks with embeddings in Weaviate.
    """
    dr.execute(
        ["store_documents"],
        inputs=dict(
            arxiv_ids=[],
            embedding_model_name="text-embedding-ada-002",
            data_dir="",
        ),
        overrides=dict(local_pdfs=pdf_files, weaviate_client=weaviate_client)
    )


def rag_summary(
    dr: driver.Driver,
    weaviate_client: weaviate.Client,
    rag_query: str,
    hybrid_search_alpha: float,
    retrieve_top_k: int,
):
    """Retrieve most relevant chunks stored in Weaviate using hybrid search
    Generate text summaries using ChatGPT for each chunk
    Concatenate all chunk summaries into a single query, and reduce into a
    final summary
    """
    return dr.execute(
        ["rag_summary", "all_chunks"],
        inputs=dict(
            rag_query=rag_query,
            hybrid_search_alpha=hybrid_search_alpha,
            retrieve_top_k=retrieve_top_k,
            embedding_model_name="text-embedding-ada-002",
            summarize_model_name="gpt-3.5-turbo-0613",
        ),
        overrides=dict(weaviate_client=weaviate_client)
    )


def all_documents(dr: driver.Driver, weaviate_client: weaviate.Client):
    """Retrieve the file names of all stored PDFs in the Weaviate instance"""
    return dr.execute(
        ["all_documents_file_name"],
        overrides=dict(weaviate_client=weaviate_client)
    )


def get_document_by_id(dr: driver.Driver, weaviate_client: weaviate.Client, document_id: str):
    """Retrieve a document stored in Weaviate based on its id"""
    return dr.execute(
        ["get_document_by_id"],
        inputs=dict(document_id=document_id),
        overrides=dict(weaviate_client=weaviate_client)
    )
