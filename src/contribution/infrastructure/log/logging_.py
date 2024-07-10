import logging

from .json_formatter import JsonFormatter


def setup_logging() -> None:
    loggers = [
        logging.getLogger(logger_name)
        for logger_name in logging.root.manager.loggerDict
        if logger_name.startswith(
            "contribution.application.command_processors.",
        )
    ]
    for logger in loggers:
        logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(JsonFormatter())

        logger.addHandler(stream_handler)
