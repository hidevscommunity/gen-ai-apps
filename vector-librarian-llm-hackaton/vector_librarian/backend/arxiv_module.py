from pathlib import Path

import arxiv
from streamlit.runtime.uploaded_file_manager import UploadedFile
from hamilton.htypes import Collect, Parallelizable


def arxiv_to_download(arxiv_ids: list[str], data_dir: str | Path) -> Parallelizable[arxiv.Result]:
    """Iterate over arxiv search resulsts for given arxiv ids"""
    for arxiv_result in arxiv.Search(id_list=arxiv_ids).results():
        yield arxiv_result


def created_data_dir(data_dir: str | Path) -> str:
    """Create the directory to download PDFs if it doesn't exist already;
    NOTE. if you try to create it in the Parallelizable threads, you could face race conditions
    """
    data_dir = Path(data_dir)
    if data_dir.exists():
        data_dir.mkdir(parents=True)

    return str(data_dir)


def download_arxiv_pdf(arxiv_to_download: arxiv.Result, created_data_dir: str) -> str:
    """Download the PDF for the arxiv resutl and return PDF path"""
    return arxiv_to_download.download_pdf()  # dirpath=created_data_dir)


def arxiv_pdf_path(download_arxiv_pdf: str) -> str:
    """Extend the PDF path to its full path"""
    return str(Path(download_arxiv_pdf).absolute())


def arxiv_pdf_path_collection(arxiv_pdf_path: Collect[str]) -> list[str]:
    """Collect local PDF files full path"""
    return arxiv_pdf_path


def local_pdfs(arxiv_pdf_path_collection: list[str]) -> list[str | UploadedFile]:
    """List of local PDF files, either string paths or in-memory files (on the FastAPI server)
    NOTE. This function is overriden by the driver to use arbitrary local PDFs and
    don't need to query arxiv. It is necessary because Parallelizable and Collect nodes
    cannot be overriden safely at the moment (sf-hamilton==1.26.0)
    """
    return arxiv_pdf_path_collection