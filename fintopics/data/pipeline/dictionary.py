# -*- coding: utf-8 -*-

"""A pipeline for generating a dictionary from a corpus."""
import logging
import os
from typing import Any, AsyncGenerator, Optional

from gensim.corpora import Dictionary
from tqdm import tqdm

from fintopics import config
from fintopics.data import get_file_list
from fintopics.data.pipeline import Pipeline, document, lemma
from fintopics.data.pipeline import read as read_pipeline
from fintopics.data.pipeline import word

logger = logging.getLogger(__name__)


def load_gensim_dictionary() -> Optional[Dictionary]:
    """Loads a gensim dict from file."""
    gdpath = config['gensim_dictionary_path']
    if not os.path.isfile(gdpath):
        return None

    return Dictionary.load(gdpath)


def get_input_stream(schema=None) -> AsyncGenerator[Any, None]:
    """This function is used to get a pipeline to feed into a dictionary.

    Args:
        schema(:obj:`dict`): The schema for the file pipeline

    Returns:
        An iterable containing lists of words to train a dictionary with.
    """
    # Build the pipeline
    files = read_pipeline.get_input_stream()
    file_stream = read_pipeline.ReadFilePipeline(
        input_stream=files,
        schema=schema,
    ).output_stream()
    doc_stream = document.DocumentPipeline(input_stream=file_stream).output_stream()
    word_stream = word.WordPipeline(input_stream=doc_stream).output_stream()
    return lemma.LemmaPipeline(input_stream=word_stream).output_stream()


class DictionaryPipeline(Pipeline):
    """Pipeline for creating and updating a gensim dictionary.

    This Pipeline converts the corpus into a Bag of Words Representation.
    """

    def __init__(self, *args, **kwargs):
        """Loads a dictionary for updating."""
        super().__init__(*args, **kwargs)

        # This is only for lazy loading. Use get_dict() unless you are sure you
        # need this.
        self._dictionary: Optional[Dictionary] = load_gensim_dictionary()

    async def train_dictionary(self) -> None:
        """This function trains a new gensim dictionary from the corpus."""
        input_stream = get_input_stream()
        # Train the dictionary

        pbar = tqdm(total=len(get_file_list()))
        async for data_stream in input_stream:
            await self.run(data_stream)
            pbar.update(1)
        pbar.close()
        self.save_dict()

    async def get_dictionary(self) -> Dictionary:
        """This function is used to get an instance of a gensim dictionary.

        It will load a dictionary from file if one has not already been loaded. If
        no previous dictionary has been loaded and no dictionary has been saved
        to file it will train a new one.

        Returns:
            :obj:`gensim.corpora.dictionary.Dictionary`: The dictionary found
            in ucla_topic_analysis/model/dictionary.gensim or None if there was
            no dictionary.
        """
        if self._dictionary is None:
            logger.info('Did not find a saved dictionary. Training one now.')
            self._dictionary = Dictionary()
            await self.train_dictionary()
        return self._dictionary

    def save_dict(self) -> None:
        """Saves the updated dictionary to file."""
        if self._dictionary:
            self._dictionary.save(config['gensim_dictionary_path'])

    async def coroutine(self, data_stream):
        """Converts the documents in the data to bags of words.

        Args:
            data_stream (:obj:`dict`): A dict with the key "text" containing a list of
                lists with tokenised words that need to be changed to a bag of
                words format.

        Returns:
            :obj:`dict`: The data dict with the value associated with "text"
            replaced with a list containing a bag of words representation for
            each document.
        """
        dictionary = await self.get_dictionary()
        data_stream['text'] = [
            dictionary.doc2bow(document, allow_update=True) for document in data_stream['text']
        ]
        self.save_dict()
        return data_stream
