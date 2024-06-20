import logging

from .json_formatter import JsonFormatter


def setup_logging() -> None:
    root_logger = logging.getLogger()

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(JsonFormatter())

    root_logger.addHandler(stream_handler)
