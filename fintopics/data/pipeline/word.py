# -*- coding: utf-8 -*-

"""A pipeline for breaking text into words."""

import nltk

from fintopics.data.pipeline import Pipeline


class WordPipeline(Pipeline):
    """Pipeline that generates a list of words from string."""

    async def coroutine(self, data_stream):
        """Tokenises the text in the given list of documents into a lists of words.

        Args:
            data_stream (:obj:`dict`): A dictionary containng the key "text" which is
                an :obj:`list` of :obj:`str` containing the list of strings to
                be tokenised.

        Returns:
            :obj:`dict`: The data dict with the value associated with the key
            `text` replaced with a list of lists containing tokenised
            words. Any other data in the data dict is left untouched.
        """
        data_stream['text'] = [nltk.word_tokenize(document) for document in data_stream['text']]
        return data_stream
