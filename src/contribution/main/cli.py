import sys

from cyclopts import App
from gunicorn.app.wsgiapp import run

from contribution.presentation.cli import create_movie


def run_web_api() -> None:
    """
    Runs the server with web api at 0.0.0.0:8000.
    """
    sys.argv = [
        "gunicorn",
        "--bind",
        "0.0.0.0:8000",
        "--workers",
        "1",
        "--worker-class",
        "uvicorn.workers.UvicornWorker",
        "contribution.main.web_api:create_web_api_app()",
    ]
    run()


def create_cli_app() -> App:
    app = App(
        name="Contribution",
        version="0.1.0",
    )

    app.command(run_web_api)
    app.command(create_movie)

    return app


def main() -> None:
    app = create_cli_app()
    app()
