# -*- coding: utf-8 -*-

import os
import random
from typing import List

from fintopics import config


def _dir_walk_txt(path: str):
    for dir_path, _, file_names in os.walk(path):
        for file_name in file_names:
            if file_name[-4:] == '.txt':
                yield os.path.join(dir_path, file_name)

def _dir_walk_json(path: str):
    for dir_path, _, file_names in os.walk(path):
        for file_name in file_names:
            if file_name[-5:] == '.json':
                yield os.path.join(dir_path, file_name)

def get_file_list() -> List[str]:
    """Returns the files to be used.

    Returns:
        list: A list of absolute paths
    """
    generator = random.Random()
    seed = 1037
    generator.seed(seed)
    file_type = config['data']['file_type']
    if file_type == 'json':
        files = _dir_walk_json(config['data']['doc_path'])
    else:
        files = _dir_walk_txt(config['data']['doc_path'])

    files = list(
        filter(lambda fpath: config['data']['req_str'] in fpath, files),
    )

    file_limit = config['data']['file_limit']
    return generator.sample(files, file_limit) if len(files) > file_limit else files
