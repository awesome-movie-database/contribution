from typing import Annotated, Iterable, Optional
from datetime import date

from cyclopts import Parameter

from contribution.domain import (
    MPAA,
    Genre,
    Country,
    Money,
    MovieId,
)
from contribution.application import (
    CommandProcessor,
    MovieRole,
    MovieWriter,
    MovieCrewMember,
    CreateMovieCommand,
)
from contribution.infrastructure import cli_ioc_container_factory
from contribution.presentation.cli.converters import (
    str_to_uuid,
    str_to_date,
    json_to_money,
    jsons_to_movie_roles,
    jsons_to_movie_writers,
    jsons_to_movie_crew,
)


async def create_movie(
    id: Annotated[
        MovieId,
        Parameter("--id", converter=str_to_uuid),
    ],
    eng_title: Annotated[str, Parameter("--eng-title")],
    original_title: Annotated[str, Parameter("--original-title")],
    release_date: Annotated[
        date,
        Parameter("--release-date", converter=str_to_date),
    ],
    countries: Annotated[Iterable[Country], Parameter("--countries")],
    genres: Annotated[Iterable[Genre], Parameter("--genres")],
    mpaa: Annotated[MPAA, Parameter("--mpaa")],
    duration: Annotated[int, Parameter("--duration")],
    budget: Annotated[
        Optional[Money],
        Parameter(
            "--budget",
            converter=json_to_money,
            show_default=True,
            help=(
                "Budget in [bright_red]json[/bright_red] format.\n\n"
                "Example:\n"
                "[bright_red]{\n"
                '    "amount": "100",\n'
                '    "currency": "USD"\n'
                "}[/bright_red]"
            ),
        ),
    ] = None,
    revenue: Annotated[
        Optional[Money],
        Parameter(
            "--revenue",
            converter=json_to_money,
            show_default=True,
            help=(
                "Revenue in [bright_red]json[/bright_red] format.\n\n"
                "Example:\n"
                "[bright_red]{\n"
                '    "amount": "100",\n'
                '    "currency": "USD"\n'
                "}[/bright_red]"
            ),
        ),
    ] = None,
    roles: Annotated[
        Optional[Iterable[MovieRole]],
        Parameter(
            "--roles",
            converter=jsons_to_movie_roles,
            help=(
                "List of roles in [bright_red]json[/bright_red] format "
                "(Each role must be in [bright_red]json[/bright_red] "
                "format).\n\n"
                "Example of a role:\n"
                "[bright_red]{\n"
                '    "id": "066746d0-a236-7f1d-8000-1711de4b4e03",\n'
                '    "person_id": "066746c5-fda5-7985-8000-d16c225a8b17",\n'
                '    "character": "Captain Jack Sparrow",\n'
                '    "importance": 1,\n'
                '    "is_spoiler": false\n'
                "}[/bright_red]"
            ),
        ),
    ] = None,
    writers: Annotated[
        Optional[Iterable[MovieWriter]],
        Parameter(
            "--writers",
            converter=jsons_to_movie_writers,
            help=(
                "List of writers in [bright_red]json[/bright_red] format "
                "(Each writer must be in [bright_red]json[/bright_red] "
                "format).\n\n"
                "Example of a writer:\n"
                "[bright_red]{\n"
                '    "id": "066746e6-b9b3-7b13-8000-120c5b23f268",\n'
                '    "person_id": "066746e5-71e3-73e5-8000-d9bdd5ead582",\n'
                '    "writing": "Origin"\n'
                "}[/bright_red]"
            ),
        ),
    ] = None,
    crew: Annotated[
        Optional[Iterable[MovieCrewMember]],
        Parameter(
            "--crew",
            converter=jsons_to_movie_crew,
            help=(
                "List of crew members in [bright_red]json[/bright_red] format "
                "(Each crew member must be in [bright_red]json[/bright_red] "
                "format).\n\n"
                "Example of a crew member:\n"
                "[bright_red]{\n"
                '   "id": "066746ff-367e-721f-8000-655eca7fdf18",\n'
                '   "person_id": "066746fe-49a6-7e8d-8000-d780471a81f9",\n'
                '   "membership": "Director"\n'
                "}[/bright_red]"
            ),
        ),
    ] = None,
) -> None:
    """
    Creates new movie. Does not notify other services about a new movie.
    """
    ioc_container = cli_ioc_container_factory()

    command = CreateMovieCommand(
        id=id,
        eng_title=eng_title,
        original_title=original_title,
        release_date=release_date,
        countries=countries,
        genres=genres,
        mpaa=mpaa,
        duration=duration,
        budget=budget,
        revenue=revenue,
        roles=roles or [],
        writers=writers or [],
        crew=crew or [],
    )
    async with ioc_container() as request_ioc_contanier:
        command_processor = await request_ioc_contanier.get(
            CommandProcessor[CreateMovieCommand, None],
        )
        try:
            await command_processor.process(command)
        except:
            return

    print("Movie has been added successfully")
