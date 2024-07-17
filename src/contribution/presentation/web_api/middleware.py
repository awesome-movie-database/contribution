from typing import Callable

from fastapi import FastAPI, Request, Response


def suppress_exceptions_middleware_factory(
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
            return Response(status_code=500)

    return suppress_exceptions_middleware


def setup_middleware(app: FastAPI, suppress_exceptions: bool) -> None:
    supress_exceptions_middleware = suppress_exceptions_middleware_factory(
        suppress_exceptions=suppress_exceptions,
    )
    app.middleware("http")(supress_exceptions_middleware)
