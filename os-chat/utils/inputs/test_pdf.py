import os

import requests
import pytest
from .pdf import extract

url = "https://www.golang-book.com/public/pdf/gobook.pdf"
filename = os.path.join("testdata", "gobook.pdf")


def download_file(url: str, destination: str) -> None:
    response = requests.get(url, stream=True)
    chunk_size = 1024
    with open(destination, "wb") as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)


def test_extract_pdf(benchmark):
    text = benchmark(extract, filename)
    testcases = (
        "Go",
        "An Introduction to Programming in Go",
        "Copyright © 2012 by Caleb Doxsey",
        "package main",
        "1 Getting Started ",
        "true || true",
    )

    assert len(text) > 0

    for i in testcases:
        assert i in text


@pytest.fixture(scope='session', autouse=True)
def cleanup():
    print("Performing cleanup tasks before running tests")
    if not os.path.exists(filename):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname): os.mkdir(dirname)
        download_file(url, filename)

    yield
    temp_files = [filename]
    print("Performing cleanup tasks after running tests")
    # for temp_file in temp_files:
    #     if os.path.exists(temp_file):
    #         os.remove(temp_file)
