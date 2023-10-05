import io
from pathlib import Path
import tempfile
import pytest

from .html import extract


def test_extract_string_input(benchmark):
    html_string = '<html><head><title>Test Title</title></head><body><p>Test paragraph.</p></body></html>'
    result = benchmark(extract, html_string)
    assert result == html_string


def test_extract_path_input(benchmark):
    def setup():
        nonlocal temp_file_path
        args = (temp_file_path,)
        kwargs = {}
        return args, kwargs

    html_string = '<html><head><title>Test Title</title></head><body><p>Test paragraph.</p></body></html>'
    with tempfile.NamedTemporaryFile('w', delete=False) as temp_file:
        temp_file.write(html_string)
        temp_file_path = Path(temp_file.name)
    result = benchmark.pedantic(extract, setup=setup, rounds=1000)
    temp_file_path.unlink()
    assert result == html_string


def test_extract_io_input(benchmark):
    html_string = '<html><head><title>Test Title</title></head><body><p>Test paragraph.</p></body></html>'
    with io.StringIO(html_string) as html_io:
        result = benchmark(extract, html_src=html_io)
    assert result == html_string


def test_extract_invalid_input(benchmark):
    invalid_input = 12345
    with pytest.raises(ValueError, match="Invalid input type. Expected str, IO, or Path."):
        benchmark(extract, html_src=invalid_input)
