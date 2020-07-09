# -*- coding: utf-8 -*-

from fintopics.data.pipeline import Pipeline
from fintopics import config
import re

class DocumentPipeline(Pipeline):
    """Pipeline that cleans documents using regex."""

    async def coroutine(self, data_stream):
        """Tokenises the given data into a list of sentences.

        Args:
            data_stream (:obj:`dict`): A dictionary containing the key "text" which is
                to be tokenised into sentences.

        Returns:
            :obj:`dict`: The data dict with the value associated with the key
            "text" replaced with a list strings containing the tokenised
            sentences. All other data in the dict is left untouched.
        """
        data_stream['text'] = data_stream['text'].split('\n\n')
        data_stream['text'] = [doc.replace('\n', '') for doc in data_stream['text']]

        if config['data']['label'].lower() == "true":
            current_label = "none"
            data_stream["label"] = []
            for line in data_stream["text"]:
                if line.strip() != "" and all(ch.isdigit() or ch.isupper() or ch == " " or ch == "\t" for ch in line):
                    current_label = (re.sub(r'\d+', '', line)).lower()
                    if current_label.strip() == "":
                        current_label = "none"
                data_stream["label"].append(current_label)

        return data_stream
