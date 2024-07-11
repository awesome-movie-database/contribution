import logging

from faststream.broker.message import StreamMessage

from contribution.application import OperationId
from .default import default_operation_id_factory


logger = logging.getLogger(__name__)


def event_consumer_operation_id_factory(message: StreamMessage) -> OperationId:
    if not isinstance(message.decoded_body, dict):
        default_operation_id = default_operation_id_factory()
        logger.warning(
            "Message received from message broker cannot be converted to dict. "
            "Default operation id will be used instead.",
            extra={
                "received_message": message.decoded_body,
                "default_operation_id": default_operation_id,
            },
        )
        return default_operation_id

    operation_id_as_str = message.decoded_body.get("operation_id")
    if not operation_id_as_str:
        default_operation_id = default_operation_id_factory()
        logger.warning(
            "Message receieved from message broker has no operation id. "
            "Default operation id will be used instead.",
            extra={
                "received_message": message.decoded_body,
                "default_operation_id": default_operation_id,
            },
        )
        return default_operation_id

    return OperationId(operation_id_as_str)
