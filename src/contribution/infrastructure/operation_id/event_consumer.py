import logging
from typing import Any, cast

from faststream.broker.message import StreamMessage
from faststream.types import DecodedMessage

from contribution.application import OperationId


logger = logging.getLogger(__name__)


def event_consumer_operation_id_factory(message: StreamMessage) -> OperationId:
    message_as_dict = _ensure_dict(message)

    operation_id_as_str = message_as_dict.get("operation_id")
    if not operation_id_as_str:
        logger.error(
            "Unexpected error occurred: "
            "Message receieved from message broker has no operation id",
            extra={"received_message": message},
        )
        raise ValueError()

    return OperationId(operation_id_as_str)


def _ensure_dict(decoded_message: DecodedMessage) -> dict[str, Any]:
    if not isinstance(decoded_message, dict):
        logger.error(
            "Unexpected error occurred: "
            "Message received from message broker cannot be converted to dict",
            extra={"received_message": decoded_message},
        )
        raise ValueError()
    return cast(dict, decoded_message)
