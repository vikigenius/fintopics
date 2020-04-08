# -*- coding: utf-8 -*-

import pytest

from fintopics.data.pipeline.regex import RegexExtractionPipeline


@pytest.fixture()
def regex_pipeline():
    """Creates a RegexExtractionPipeline fixture."""
    return RegexExtractionPipeline()


@pytest.mark.asyncio
async def test_header_removal(datadir, regex_pipeline):
    """Tests removal of header."""
    header_file = datadir / 'header.txt'
    text = header_file.read_text()
    actual_text = await regex_pipeline.coroutine(text)
    assert actual_text['text'].strip() == ''


@pytest.mark.asyncio
async def test_exhibit_removal(datadir, regex_pipeline):
    """Tests removal of header."""
    exhibit_file = datadir / 'exhibit.txt'
    text = exhibit_file.read_text()
    actual_text = await regex_pipeline.coroutine(text)
    assert actual_text['text'].strip() == ''
