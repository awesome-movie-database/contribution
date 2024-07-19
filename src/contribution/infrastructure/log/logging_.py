import sys
import logging

from .json_formatter import JsonFormatter


def setup_logging() -> None:
    loggers: list[logging.Logger] = []
    for logger_name in logging.root.manager.loggerDict:
        if _is_command_processor_logger(
            logger_name,
        ) or _is_operation_id_factory_logger(logger_name):
            logger = logging.getLogger(logger_name)
            loggers.append(logger)

    for logger in loggers:
        logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(JsonFormatter())

        logger.addHandler(stream_handler)


def _is_command_processor_logger(logger_name: str) -> bool:
    return logger_name.startswith(
        "contribution.application.command_processors.",
    )


def _is_operation_id_factory_logger(logger_name: str) -> bool:
    return logger_name.startswith(
        "contribution.infrastructure.operation_id.",
    )
