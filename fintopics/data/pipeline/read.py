# -*- coding: utf-8 -*-

"""Contains the ReadFilePipeline class for reading text files."""

import random
from typing import Dict, Generator, Optional

from fintopics.data import get_file_list
from fintopics.data.pipeline import Pipeline


def get_input_stream() -> Generator[str, None, None]:
    """An input stream for the pipeline."""
    yield from sorted(get_file_list())


class ReadFilePipeline(Pipeline):
    """Pipeline that generates a list of file text."""

    def __init__(self, schema: Optional[Dict[str, float]] = None, *args, **kwargs):
        r"""Initialise the pipeline.

        Args:
            schema (:obj:`dict`. optional): A dict where the keys are the
                categories and the values are the proportion of documents
                in that category. The values must be in the range [0, 1]
                and must add up to 1. If this is `None` (default) then
                every document will be labelled `None`.
            *args: Variable length arguments that should be passed on to
                the super class.
            **kwargs: Variable length arguments that should be passed on to
                the super class.

        Raises:
            ValueError: If schema is incorrect
        """
        # Sanity tests
        if schema and sum(schema.values()) != 1:
            raise ValueError('Values in schema must add up to 1')
        if schema and not all(0 <= schema[key] <= 1 for key in schema):  # noqa: WPS221
            raise ValueError('Values in schema must be in the range [0, 1]')

        # Set the instance variables
        self._schema = schema
        self._seed = 0

        # Initialise parent class
        super().__init__(*args, **kwargs)

    async def coroutine(self, data_stream):
        """Extracts text from the given data file and attaches a split label.

        Args:
            data_stream (str): Path to the file that is to be read

        Returns:
            :obj:`dict`: A dictionary of the form::
                {
                    'text': The text in the file pointed to by the data,
                    'split': The split associated with this document,
                    'path': The relative path to the file

                }
        """
        result_stream = {'split': self._sort_document(), 'path': data_stream}
        with open(data_stream, encoding='utf-8', mode='r') as data_file:
            result_stream['text'] = data_file.read()
        self._seed += 1
        return result_stream

    def _sort_document(self, seed=None) -> Optional[str]:
        """Used to pick a document for the current mode.

        Args:
            seed: The seed to use for the random number generator. If this is
                not set then self._seed will be used.

        Returns:
            str: the split to attach to the document

        Raises:
            IndexError: If split proportions do not sum to 1
        """
        generator = random.Random()

        # Generate a random number
        generator.seed(seed or self._seed)
        random_number = generator.random()

        # If no mode or split mechanic is set then pick every document
        if not self._schema:
            return None

        # Check if we should pick the document
        start = 0.0
        for key in sorted(self._schema.keys()):
            end = start + self._schema[key]
            if start <= random_number < end:
                return key
            start += self._schema[key]
        raise IndexError('Error with `split` proportions')  # pragma: no cover
