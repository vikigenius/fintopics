# -*- coding: utf-8 -*-

from pathlib import Path

import pytest


@pytest.fixture()
def datadir():
    """Fixture returning location of data."""
    return Path(__file__).parent / 'tests/fixtures'
