"""Pytest configuration file."""

import os
import tempfile
from pathlib import Path

import pytest
import toml


@pytest.fixture
def temp_file(request):
    temp = tempfile.NamedTemporaryFile(delete=False)

    def fin():
        os.remove(temp.name)

    request.addfinalizer(fin)

    return temp


@pytest.fixture(scope="session")
def config():
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    config_path = parent_dir / "conf/conf.toml"

    with open(config_path, "r") as file:
        config = toml.load(file)

    return config
