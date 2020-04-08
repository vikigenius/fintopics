# -*- coding: utf-8 -*-

"""A pipeline for getting the root of the word."""

from typing import Iterable, Optional, Set

import nltk
from nltk.corpus import wordnet as wn

from fintopics.data.pipeline import Pipeline


def get_lemma(word: str) -> str:
    """Get the root of the word.

    Args:
        word (str): The word we want to lemmatise

    Returns:
        str: The lemmatised version of the given word
    """
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    return lemma


class LemmaPipeline(Pipeline):
    """Pipeline that obtains the root of the word."""

    def __init__(self, stopwords: Optional[Set[str]] = None, *args, **kwargs):
        """Initialize the pipelinze."""
        super().__init__(*args, **kwargs)
        standard_stopwords: Set[str] = set(nltk.corpus.stopwords.words('english'))
        self.stopwords: Set[str] = standard_stopwords.union(stopwords or set())

    def filter_and_lemmatize(self, words: Iterable[str]):
        """Filter words with lemma and stopwords.

        Args:
            words (:obj:`list` of :obj:`str`): The list of words that need to
                be prepared

        Returns:
            :obj:`list` of :obj:`str`: The cleaned up list of words
        """
        tokens = []
        for word in words:
            if len(word) > 4 and word not in self.stopwords:
                tokens.append(get_lemma(word).lower())
        return tokens

    async def coroutine(self, data_stream):
        """Tokenises the given data into a list of words.

        Args:
            data_stream (:obj:`dict`): A dict with the key "text" containing a list of
                lists with tokenised words that need to be processed

        Returns:
            :obj:`dict`: The data dict with the value associated with the key
            "text" replaced with the lemmatised and filtered list of word lists.
            All other data in the dict is left untouched.
        """
        data_stream['text'] = [
            self.filter_and_lemmatize(sentence) for sentence in data_stream['text']
        ]
        return data_stream
