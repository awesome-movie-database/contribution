import sys
from typing import Annotated

from cyclopts import App, Parameter
from gunicorn.app.wsgiapp import run as run_gunicorn
from faststream.cli.main import cli as run_faststream

from contribution.infrastructure import setup_logging
from contribution.presentation.cli import (
    create_movie,
    create_person,
    update_person,
)


def main() -> None:
    setup_logging()
    app = create_cli_app()
    app()


def create_cli_app() -> App:
    app = App(
        name="Contribution",
        version="0.1.0",
        help_format="rich",
    )

    app.command(run_web_api)
    app.command(run_event_consumer)

    app.command(create_movie)
    app.command(create_person)
    app.command(update_person)

    return app


def run_web_api(
    address: Annotated[
        str,
        Parameter("--address", show_default=True),
    ] = "0.0.0.0:8000",
    workers: Annotated[
        str,
        Parameter("--workers", show_default=True),
    ] = "1",
) -> None:
    """Runs the server with web api at specified address."""
    sys.argv = [
        "gunicorn",
        "--bind",
        address,
        "--workers",
        workers,
        "--worker-class",
        "uvicorn.workers.UvicornWorker",
        "contribution.main.web_api:create_web_api_app()",
    ]
    run_gunicorn()


def run_event_consumer(
    workers: Annotated[
        str,
        Parameter("--workers", show_default=True),
    ] = "1",
) -> None:
    """Runs event consumer."""
    sys.argv = [
        "faststream",
        "run",
        "contribution.main.event_consumer:create_event_consumer_app",
        "--workers",
        workers,
        "--factory",
    ]
    run_faststream()
