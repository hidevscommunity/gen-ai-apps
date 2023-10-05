from pathlib import Path
from typing import IO, List

from langchain.schema import Document
from pypdf import PdfReader


def extract(pdf_docs: str | IO | Path | List[Document]) -> str:
    if isinstance(pdf_docs, str):
        pdf_docs = [pdf_docs]

    text = ''
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
