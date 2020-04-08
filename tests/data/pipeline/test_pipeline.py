# -*- coding: utf-8 -*-

import asyncio

import pytest

from fintopics.data.pipeline import Pipeline

# TODO: Write tests for Output Stream


class TestPipeline(Pipeline):
    """A test pipeline."""

    async def coroutine(self, data_stream):
        """Simple Implementation of a coroutine."""
        await asyncio.sleep(0.01)
        return '{0}some test data'.format(data_stream)


@pytest.fixture()
def pipeline():
    """A pipline fixture."""
    return TestPipeline()


@pytest.mark.asyncio
async def test_result_is_set(pipeline):
    """Tests that the pipeline._result variable is properly set."""
    expected = 'some test data'
    await pipeline.run('')
    assert expected == pipeline.result_stream


@pytest.mark.asyncio
async def test_downstream_is_run(pipeline):
    """Tests that the downstream pipeline is run."""
    expected = 'some test datasome test data'
    nested_pipeline = TestPipeline([pipeline])
    await nested_pipeline.run('')
    assert expected == pipeline.result_stream


@pytest.mark.asyncio
async def test_data_is_passed(pipeline):
    """Tests that the data is passed to the coroutine."""
    expected = 'some other test data some test data'
    await pipeline.run('some other test data ')
    assert expected == pipeline.result_stream
