import base64
import io
from pathlib import Path
from typing import Generator

import openai
import pypdf
from streamlit.runtime.uploaded_file_manager import UploadedFile
import tiktoken
import weaviate
from weaviate.util import generate_uuid5

from hamilton.htypes import Collect, Parallelizable


def pdf_file(
    local_pdfs: list[str | UploadedFile],
) -> Parallelizable[str | UploadedFile]:
    """Iterate over local PDF files, either string paths or in-memory files (on the Streamlit server)"""
    for pdf_file in local_pdfs:
        yield pdf_file


def pdf_content(pdf_file: str | UploadedFile) -> io.BytesIO:
    """Read the content of the PDF file as a bytes buffer that will be passed to a PDF reader;
    The implementation differs if the file is passed as path or in-memory
    """
    if isinstance(pdf_file, str):
        return io.BytesIO(Path(pdf_file).read_bytes())
    elif isinstance(pdf_file, UploadedFile):
        return io.BytesIO(pdf_file.read())
    else:
        raise TypeError


def file_name(pdf_file: str | UploadedFile) -> str:
    """Read the content of the PDF file as a bytes buffer that will be passed to a PDF reader;
    The implementation differs if the file is passed as path or in-memory
    """
    if isinstance(pdf_file, str):
        file_path = Path(pdf_file)
    elif isinstance(pdf_file, UploadedFile):
        file_path = Path(pdf_file.name)
    else:
        raise TypeError

    return file_path.stem


def raw_text(pdf_content: io.BytesIO) -> str:
    """Read local PDF files and return the raw text as string;
    Throw exception if unable to read PDF
    """
    reader = pypdf.PdfReader(pdf_content)
    pdf_text = " ".join((page.extract_text() for page in reader.pages))
    return pdf_text


def tokenizer(tokenizer_encoding: str = "cl100k_base") -> tiktoken.core.Encoding:
    """Get OpenAI tokenizer"""
    return tiktoken.get_encoding(tokenizer_encoding)


def _create_chunks(
    text: str, tokenizer: tiktoken.core.Encoding, max_length: int
) -> Generator[str, None, None]:
    """Return successive chunks of size `max_length` tokens from provided text.
    Split a text into smaller chunks of size n, preferably ending at the end of a sentence
    """
    tokens = tokenizer.encode(text)
    i = 0
    while i < len(tokens):
        # Find the nearest end of sentence within a range of 0.5 * n and 1.5 * n tokens
        j = min(i + int(1.5 * max_length), len(tokens))
        while j > i + int(0.5 * max_length):
            # Decode the tokens and check for full stop or newline
            chunk = tokenizer.decode(tokens[i:j])
            if chunk.endswith(".") or chunk.endswith("\n"):
                break
            j -= 1
        # If no end of sentence found, use n tokens as the chunk size
        if j == i + int(0.5 * max_length):
            j = min(i + max_length, len(tokens))
        yield tokens[i:j]
        i = j


def chunked_text(
    raw_text: str, tokenizer: tiktoken.core.Encoding, max_token_length: int = 500
) -> list[str]:
    """Tokenize text; create chunks of size `max_token_length`;
    for each chunk, convert tokens back to text string
    """
    _encoded_chunks = _create_chunks(raw_text, tokenizer, max_token_length)
    _decoded_chunks = [tokenizer.decode(chunk) for chunk in _encoded_chunks]
    return _decoded_chunks


def _get_embeddings__openai(texts: list[str], embedding_model_name: str) -> list[list[float]]:
    """Get the OpenAI embeddings for each text in texts"""
    response = openai.Embedding.create(input=texts, model=embedding_model_name)
    return [item["embedding"] for item in response["data"]]


def chunked_embeddings(chunked_text: list[str], embedding_model_name: str) -> list[list[float]]:
    """Convert each chunk of the arxiv article as an embedding vector"""
    return _get_embeddings__openai(texts=chunked_text, embedding_model_name=embedding_model_name)


def pdf_embedded(
    pdf_content: io.BytesIO,
    file_name: str,
    chunked_text: list[str],
    chunked_embeddings: list[list[float]],
) -> dict:
    """Gather information about each arxiv into a single object"""
    return dict(
        pdf_blob=base64.b64encode(pdf_content.getvalue()).decode("utf-8"),
        file_name=file_name,
        chunked_text=chunked_text,
        chunked_embeddings=chunked_embeddings,
    )


def pdf_collection(pdf_embedded: Collect[dict]) -> list[dict]:
    """Collect arxiv objects"""
    return list(pdf_embedded)


def store_documents(
    weaviate_client: weaviate.Client,
    pdf_collection: list[dict],
    batch_size: int = 50,
) -> None:
    """Store arxiv objects in Weaviate in batches.
    The vector and references between Document and Chunk are specified manually
    """
    weaviate_client.batch.configure(batch_size=batch_size, dynamic=True)

    with weaviate_client.batch as batch:
        for pdf_obj in pdf_collection:
            document_object = dict(
                pdf_blob=pdf_obj["pdf_blob"],
                file_name=pdf_obj["file_name"],
            )
            document_uuid = generate_uuid5(document_object, "Document")

            batch.add_data_object(
                class_name="Document",
                data_object=document_object,
                uuid=document_uuid,
            )

            chunk_iterator = zip(pdf_obj["chunked_text"], pdf_obj["chunked_embeddings"])
            for chunk_idx, (chunk_text, chunk_embedding) in enumerate(chunk_iterator):
                chunk_object = dict(content=chunk_text, chunk_index=chunk_idx)
                chunk_uuid = generate_uuid5(chunk_object, "Chunk")

                batch.add_data_object(
                    class_name="Chunk",
                    data_object=chunk_object,
                    uuid=chunk_uuid,
                    vector=chunk_embedding,
                )

                batch.add_reference(
                    from_object_class_name="Document",
                    from_property_name="containsChunk",
                    from_object_uuid=document_uuid,
                    to_object_class_name="Chunk",
                    to_object_uuid=chunk_uuid,
                )

                batch.add_reference(
                    from_object_class_name="Chunk",
                    from_property_name="fromDocument",
                    from_object_uuid=chunk_uuid,
                    to_object_class_name="Document",
                    to_object_uuid=document_uuid,
                )
