import logging

from fastapi import Request

from contribution.application import OperationId
from .default import default_operation_id_factory


logger = logging.getLogger(__name__)


def web_api_operation_id_factory(request: Request) -> OperationId:
    operation_id_as_str = request.headers.get("X-Operation-Id")
    if not operation_id_as_str:
        default_operation_id = default_operation_id_factory()
        logger.warning(
            "Request has no operation id header. "
            "Default operation id will be used instead.",
            extra={
                "request_headers": request.headers,
                "default_operation_id": default_operation_id,
            },
        )
        return default_operation_id

    return OperationId(operation_id_as_str)
