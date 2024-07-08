from fastapi import Request

from contribution.application import OperationId


def web_api_operation_id_factory(request: Request) -> OperationId:
    operation_id_as_str = request.headers.get("X-Operation-Id", None)
    if not operation_id_as_str:
        message = "Got no operation id for web api"
        raise ValueError(message)

    return OperationId(operation_id_as_str)
