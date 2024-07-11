import logging

from fastapi import Request

from contribution.application import OperationId


logger = logging.getLogger(__name__)


def web_api_operation_id_factory(request: Request) -> OperationId:
    operation_id_as_str = request.headers.get("X-Operation-Id")
    if not operation_id_as_str:
        logger.error(
            "Unexpected error occurred: Request has no operation id header",
            extra={"request_headers": request.headers},
        )
        raise ValueError()

    return OperationId(operation_id_as_str)
