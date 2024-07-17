from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from contribution.infrastructure import (
    setup_logging,
    web_api_ioc_container_factory,
)
from contribution.presentation.web_api import (
    setup_routes,
    setup_middleware,
    setup_exception_handlers,
)


def create_web_api_app(suppress_exceptions: bool) -> FastAPI:
    app = FastAPI(
        title="Contribution",
        version="0.1.0",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )
    ioc_container = web_api_ioc_container_factory()

    setup_logging()
    setup_dishka(ioc_container, app)
    setup_routes(app)
    setup_middleware(app, suppress_exceptions)
    setup_exception_handlers(app)

    return app
