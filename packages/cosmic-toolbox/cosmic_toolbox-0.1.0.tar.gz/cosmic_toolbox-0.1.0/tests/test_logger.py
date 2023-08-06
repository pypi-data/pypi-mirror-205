import os
import logging
from cosmic_toolbox.logger import (
    get_logger,
    set_logger_level,
    set_all_loggers_level,
)


def test_get_logger():
    logger = get_logger("test.py")
    assert isinstance(logger, logging.Logger)


def test_set_logger_level():
    logger = logging.getLogger("test_logger")
    set_logger_level(logger, "info")
    assert logger.level == logging.INFO


def test_set_all_loggers_level():
    set_all_loggers_level("debug")
    assert os.environ["PYTHON_LOGGER_LEVEL"] == "debug"
