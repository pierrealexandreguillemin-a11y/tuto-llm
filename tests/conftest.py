"""Shared fixtures for tuto-llm tests."""

from pathlib import Path

import pytest


@pytest.fixture()
def notebooks_dir() -> Path:
    """Return the path to the notebooks directory."""
    return Path(__file__).resolve().parent.parent / "notebooks"
