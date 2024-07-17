from typing import Callable

from fastapi import FastAPI, Request, Response

from .exception_handlers import on_unknown_error


def setup_middleware(app: FastAPI, suppress_exceptions: bool) -> None:
    handle_unknown_exception = _handle_unknown_exception_factory(
        suppress_exceptions=suppress_exceptions,
    )
    app.middleware("http")(handle_unknown_exception)


def _handle_unknown_exception_factory(
    suppress_exceptions: bool,
) -> Callable[[Request, Callable[[Request], Response]], Response]:
    async def suppress_exceptions_middleware(
        request: Request,
        call_next: Callable[[Request], Response],
    ) -> Response:
        if not suppress_exceptions:
            return await call_next(request)

        try:
            return await call_next(request)
        except:
            return on_unknown_error()

    return suppress_exceptions_middleware
