import os.path
import typing
from functools import cache
from io import StringIO
from pathlib import Path

from typing import IO


@cache
def extract(html_src: str | IO | Path | StringIO) -> typing.Text:
    isFile = False

    if isinstance(html_src, str):
        isFile = os.path.exists(html_src)
        if not isFile:
            return html_src

    if isinstance(html_src, Path) or isFile:
        with open(html_src, 'r') as file:
            return file.read()
    elif hasattr(html_src, 'read'):  # IO
        return html_src.read()
    else:
        raise ValueError("Invalid input type. Expected str, IO, or Path.")
