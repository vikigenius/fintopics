# -*- coding: utf-8 -*-

"""A pipeline for saving the corpus."""
from pathlib import Path
from typing import Any, AsyncGenerator

from tqdm import tqdm

from fintopics import config
from fintopics.data import get_file_list
from fintopics.data.pipeline import Pipeline, document, lemma
from fintopics.data.pipeline import read as read_pipeline
from fintopics.data.pipeline import regex, word


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
    data_stream = regex.RegexExtractionPipeline(input_stream=file_stream).output_stream()
    doc_stream = document.DocumentPipeline(input_stream=data_stream).output_stream()
    word_stream = word.WordPipeline(input_stream=doc_stream).output_stream()
    return lemma.LemmaPipeline(input_stream=word_stream).output_stream()


class TextCorpusPipeline(Pipeline):
    """Pipeline for saving corpus as txt files."""

    def __init__(self, min_length=5, *args, **kwargs):
        """Initializes the pipeline.

        Args:
            min_length (int): Minimum number of words to be considered
                as a document.
            *args: Variable length arguments that should be passed on to
                the super class.
            **kwargs: Variable length arguments that should be passed on to
                the super class.

        """
        super().__init__(*args, **kwargs)
        self.min_length = min_length

        # We use this to ensure that files are overwritten if encountered
        # for the first time and appended otherwise

        self.splits = set()

    @classmethod
    async def prepare_data(cls) -> None:
        """Runs a pipeline to save corpus as text."""
        # Build the pipeline
        tokenized_stream = get_input_stream(schema=config['data']['split'])
        lda_corpus_pipeline = cls()

        pbar = tqdm(total=len(get_file_list()))

        async for data_stream in tokenized_stream:
            await lda_corpus_pipeline.run(data_stream)
            pbar.update(1)

    async def coroutine(self, data_stream):
        """Tokenises the given data into a list of words.

        Args:
            data_stream (:obj:`dict`): A dict with the key "text" containing a list of
                lists with tokenised words that need to be processed
        """
        data_texts = filter(
            lambda doc_words: len(doc_words) > self.min_length,
            data_stream['text'],
        )
        data_text = '\n'.join(' '.join(doc_words) for doc_words in data_texts)
        split = data_stream['split']
        save_path = Path(config['data']['save_path']) / '{0}.txt'.format(split)
        mode = 'a' if split in self.splits else 'w'
        save_path.open(mode=mode).write('{0}\n'.format(data_text))
        self.splits.add(split)
