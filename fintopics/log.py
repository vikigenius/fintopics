# -*- coding: utf-8 -*-

"""Module for setting up logging."""

import logging
from logging import config as log_config
from typing import Any, Dict


def configure_logger(log_dict: Dict[str, Any], verbosity: int):
    """Configure logging for fintopics."""
    # Set up 'fintopics' logger
    if verbosity >= 1:
        log_dict['handlers']['default'] = 'verbose'
        log_dict['loggers']['fintopics']['level'] = 'DEBUG'
    log_config.dictConfig(log_dict)
    return logging.getLogger('fintopics')
