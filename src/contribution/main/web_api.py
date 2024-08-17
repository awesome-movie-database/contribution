from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from contribution.infrastructure import setup_logging
from contribution.infrastructure.di.web_api import (
    web_api_ioc_container_factory,
)
from contribution.presentation.web_api import (
    setup_routes,
    setup_exception_handlers,
)


DESCRIPTION = """
## Error codes: \n
    * 10 - User is not active.
    * 20 - Not enough permissions.
    * 200 - Movie does not exist.
    * 220 - Invalid movie eng. title.
    * 230 - Invalid movie original title.
    * 240 - Invalid movie summary.
    * 250 - Invalid movie description.
    * 260 - Invalid movie duration.
    * 300 - Person does not exist.
    * 310 - Persons do not exist.
    * 320 - Invalid person first name.
    * 330 - Invalid person last name.
    * 340 - Invalid person birth or death date.
    * 410 - Roles do not exist.
    * 420 - Invalid role character.
    * 430 - Invalid role importance.
    * 510 - Writers do not exist.
    * 610 - Crew members do not exist.

## Headers:
    * [Required] X-Current-User-Id
    * [Optional] X-Operation-Id
"""


def create_web_api_app() -> FastAPI:
    app = FastAPI(
        title="Contribution",
        description=DESCRIPTION,
        version="0.1.0",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )
    ioc_container = web_api_ioc_container_factory()

    setup_logging()
    setup_dishka(ioc_container, app)
    setup_routes(app)
    setup_exception_handlers(app)

    return app
