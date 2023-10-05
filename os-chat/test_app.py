from app import main
import pytest


def test_main():
    result = main()
    assert result is None
