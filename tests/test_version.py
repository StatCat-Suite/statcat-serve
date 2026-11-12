"""The package imports, and `__version__` is the installed distribution's."""

import importlib.metadata
import re

import pytest

import statcat_serve

pytestmark = pytest.mark.unit


def test_version_matches_the_installed_metadata() -> None:
    assert statcat_serve.__version__ == importlib.metadata.version("statcat-serve")


def test_version_is_a_release_number() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+", statcat_serve.__version__)
