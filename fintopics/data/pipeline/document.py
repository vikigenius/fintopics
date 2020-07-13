# -*- coding: utf-8 -*-

from fintopics.data.pipeline import Pipeline
from fintopics import config
import re
import string

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
                if line.strip() != "" and all(ch in string.punctuation or ch.isdigit() or ch.isupper() or ch == " " or ch == "\t" for ch in line):
                    current_label = line.replace(",", " ")
                    current_label = current_label.strip()

                    # handling "ITEM" headers
                    if current_label.startswith("ITEM"):
                        label_ls = current_label.split(" ")
                        if label_ls[1].endswith("."):
                            newlb = ""
                            for i in range(0, len(label_ls)):
                                if i != 1:
                                    newlb += label_ls[i] + " "
                            current_label = newlb

                        current_label = current_label.replace("ITEM", "")

                    current_label = (re.sub(r'\d+', '', current_label)).lower()
                    current_label = current_label.translate(str.maketrans('', '', string.punctuation))
                    current_label = current_label.strip()
                    if current_label == "":
                        current_label = "none"

                    # handling "part" headers
                    if current_label.startswith("part"):
                        label_ls = current_label.split(" ")
                        if len(label_ls) == 2:
                            current_label = "none"
                    # handle "F-" cases
                    if current_label == "f":
                        current_label = "none"

                data_stream["label"].append(current_label)

        return data_stream
