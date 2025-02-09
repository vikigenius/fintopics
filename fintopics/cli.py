# -*- coding: utf-8 -*-

import asyncio
import sys

import click
import toml

from fintopics import config
from fintopics.data.bow_matrix import prepare_bow_matrix
from fintopics.data.prepare_labels import prepare_labels
from fintopics.data.pipeline.corpus import TextCorpusPipeline
from fintopics.log import configure_logger


@click.option('-v', '--verbosity', count=True)
@click.group()
def main(verbosity: int):
    """Cli entry point for fintopics."""
    config.clear()
    config.update(toml.load('fintopics.toml'))
    configure_logger(dict(config['logging']), verbosity)


@click.argument('corpus', type=click.Choice(['text', 'scmat', 'labels']))
@click.option('--file_limit', default=10)
@click.option('--labeled', is_flag=True)
@click.option('--min_label_count', default=50)
@click.option('--no_map', is_flag=True)
@main.command()
def prepare(corpus, file_limit, labeled, min_label_count, no_map):
    """
    Command to preprocess the data.

    Args:
        corpus (str): corpus type to prepare
        file_limit (str): The number of files to limit the pipeline
    """
    config['data']['file_limit'] = file_limit
    if corpus == 'text':
        asyncio.run(TextCorpusPipeline.prepare_data())
    elif corpus == 'scmat':
        prepare_bow_matrix(labeled)
    elif corpus == 'labels':
        prepare_labels(min_label_count, no_map)


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
