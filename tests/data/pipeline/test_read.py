# -*- coding: utf-8 -*-

import pytest

from fintopics.data.pipeline.read import ReadFilePipeline


@pytest.fixture()
def read_file_pipeline() -> ReadFilePipeline:
    """Creates a ReadFilePipeline Fixture."""
    return ReadFilePipeline({'train': 0.8, 'val': 0.1, 'test': 0.1})


@pytest.fixture()
def schemaless_pipeline() -> ReadFilePipeline:
    """Creates a ReadFilePipeline Fixture."""
    return ReadFilePipeline()


@pytest.mark.asyncio
async def test_empty_file(read_file_pipeline, tmp_path):
    """Tests working for empty file."""
    efile = tmp_path / 'efile.txt'
    expected_contents = ''
    efile.write_text(expected_contents)
    actual_contents = await read_file_pipeline.coroutine(efile)
    assert expected_contents == actual_contents['text']


@pytest.mark.asyncio
async def test_content_file(read_file_pipeline, tmp_path):
    """Tests working for empty file."""
    cfile = tmp_path / 'cfile.txt'
    expected_contents = 'I am a moron\nThis is interesting'
    cfile.write_text(expected_contents)
    actual_contents = await read_file_pipeline.coroutine(cfile)
    assert expected_contents == actual_contents['text']


@pytest.mark.asyncio
async def test_split(read_file_pipeline, tmp_path):
    """Tests working for empty file."""
    cfile = tmp_path / 'cfile.txt'
    expected_contents = 'I am a moron\nThis is interesting'
    cfile.write_text(expected_contents)
    actual_contents = await read_file_pipeline.coroutine(cfile)
    assert actual_contents['split'] in {'train', 'test', 'val'}


@pytest.mark.asyncio
async def test_no_schema(schemaless_pipeline, tmp_path):
    """Tests working for a pipeline with no schema."""
    cfile = tmp_path / 'cfile.txt'
    expected_contents = 'I am a moron\nThis is interesting'
    cfile.write_text(expected_contents)
    actual_contents = await schemaless_pipeline.coroutine(cfile)
    assert actual_contents['split'] is None


def test_wrong_schema():
    """Tests exceptions raised by the Pipeline."""
    with pytest.raises(ValueError, match=r'.* add .*'):
        ReadFilePipeline({'train': 0.9, 'test': 0.3})

    with pytest.raises(ValueError, match='.* range .*'):
        ReadFilePipeline({'train': 1.3, 'test': -0.3})
