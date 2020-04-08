# -*- coding: utf-8 -*-

"""Contains the ReadFilePipeline class for reading text files."""

import re
from dataclasses import dataclass
from typing import Callable, Match

from fintopics.data.pipeline import Pipeline


@dataclass
class Replace(object):
    """Dataclass that stores info about replacement protocol."""

    replstr: str = ''
    predicate: Callable[[str], bool] = lambda string: True

    def __call__(self, match: Match[str]) -> str:
        """Callable that takes returns the replacement given a match."""
        matched: str = match.group(0)
        should_replace = self.predicate(matched)  # type: ignore
        return match.expand(self.replstr) if should_replace else matched  # okay


class RegexExtractionPipeline(Pipeline):
    """Pipeline that cleans documents using regex."""

    def __init__(self, *args, **kwargs) -> None:
        r"""Initialise the pipeline.

        Args:
            *args: Variable length arguments that should be passed on to
                the super class.
            **kwargs: Variable length arguments that should be passed on to
                the super class.

        """
        # Initialise parent class
        super().__init__(*args, **kwargs)
        self.replobjs = [
            (re.compile(r'<Header>.*<\/Header>', re.DOTALL), Replace()),
            (re.compile(r'<EX-\d+\.\d>(\n.+){3}'), Replace()),
            (re.compile(r'<\/EX-\d+\.\d>'), Replace()),
        ]

    async def coroutine(self, data_stream):
        """Extracts text from the given data file and attaches a split label.

        Args:
            data_stream (:obj:`dict`): A dictionary containing the key "text" which is
                to be processed by regex.

        Returns:
            :obj:`dict`: A dictionary of the form::
                {
                    'text': The text in the file pointed to by the data,
                    'split': The split associated with this document,
                    'path': The relative path to the file

                }
        """
        result_stream = data_stream
        for search_pattern, replacer in self.replobjs:
            result_stream['text'] = re.sub(search_pattern, replacer, result_stream['text'])
        return result_stream
