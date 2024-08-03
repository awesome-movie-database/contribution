from typing import Annotated, Iterable, Optional
from datetime import date

import rich
import rich.prompt
import rich.table
from cyclopts import Parameter

from contribution.domain import (
    MPAA,
    Genre,
    MovieId,
    MovieRole,
    MovieWriter,
    MovieCrewMember,
    Country,
    Money,
)
from contribution.application import (
    CommandProcessor,
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
        Parameter(
            "--id",
            converter=str_to_uuid,
            help="Id in [bright_yellow]UUID[/bright_yellow] format.",
        ),
    ],
    eng_title: Annotated[str, Parameter("--eng-title")],
    original_title: Annotated[str, Parameter("--original-title")],
    release_date: Annotated[
        date,
        Parameter(
            "--release-date",
            converter=str_to_date,
            help=(
                "Release date in [bright_green]ISO 8601[/bright_green] format."
            ),
        ),
    ],
    countries: Annotated[
        Iterable[Country],
        Parameter(
            "--countries",
            help=(
                "Countries in [bright_green]ISO 3166 alpha 2"
                "[/bright_green] format."
            ),
        ),
    ],
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
                "Roles in [bright_red]json[/bright_red] format "
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
                "Writers in [bright_red]json[/bright_red] format "
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
                "Crew members in [bright_red]json[/bright_red] format "
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
    Creates a new movie. Does not notify other services about it.
    Asks confirmation before execting.
    """
    continue_ = rich.prompt.Confirm.ask(
        "You are going to create a movie.\n"
        "This action does not notify other services about a new movie.\n"
        "Would you like to continue?",
    )
    if not continue_:
        return

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
    async with ioc_container() as ioc_container_request:
        command_processor = await ioc_container_request.get(
            CommandProcessor[CreateMovieCommand, None],
        )
        await command_processor.process(command)

    movie_table = _movie_table_factory(
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
        roles=roles,
        writers=writers,
        crew=crew,
    )

    rich.print("Movie has been added successfully")
    rich.print(movie_table)


def _movie_table_factory(
    id: MovieId,
    eng_title: str,
    original_title: str,
    release_date: date,
    countries: Iterable[Country],
    genres: Iterable[Genre],
    mpaa: MPAA,
    duration: int,
    budget: Optional[Money],
    revenue: Optional[Money],
    roles: Optional[Iterable[MovieRole]],
    writers: Optional[Iterable[MovieWriter]],
    crew: Optional[Iterable[MovieCrewMember]],
) -> rich.table.Table:
    movie_table = rich.table.Table(
        "id",
        "eng_title",
        "original_title",
        "release_date",
        "countries",
        "genres",
        "mpaa",
        "duration",
        "budget",
        "revenue",
        "roles",
        "writers",
        "crew",
        title="Movie",
    )
    movie_table.add_row(
        str(id),
        eng_title,
        original_title,
        release_date.isoformat(),
        str(countries),
        str(genres),
        mpaa,
        str(duration),
        str(budget) if budget else "None",
        str(revenue) if revenue else "None",
        str(roles) if roles else "None",
        str(writers) if writers else "None",
        str(crew) if crew else "None",
    )
    return movie_table
