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
from contribution.infrastructure import ioc_container_factory
from contribution.presentation.cli.converters import (
    json_to_money,
    jsons_to_movie_roles,
    jsons_to_movie_writers,
    jsons_to_movie_crew,
)


async def create_movie(
    id: Annotated[MovieId, Parameter("--id")],
    eng_title: Annotated[str, Parameter("--eng-title")],
    original_title: Annotated[str, Parameter("--original-title")],
    release_date: Annotated[date, Parameter("--release-date")],
    countries: Annotated[Iterable[Country], Parameter("--countries")],
    genres: Annotated[Iterable[Genre], Parameter("--genres")],
    mpaa: Annotated[MPAA, Parameter("--mpaa")],
    duration: Annotated[int, Parameter("--duration")],
    budget: Annotated[
        Optional[Money],
        Parameter(
            "--budget",
            converter=json_to_money,
            help=(
                "Budget in json format \n"
                'Example: {"amount": "100", "currency": "USD"}'
            ),
        ),
    ] = None,
    revenue: Annotated[
        Optional[Money],
        Parameter(
            "--budget",
            converter=json_to_money,
            help=(
                """
                Revenue in json format.

                Example: {"amount": "100", "currency": "USD"}
                """
            ),
        ),
    ] = None,
    roles: Annotated[
        Iterable[MovieRole],
        Parameter(
            "--roles",
            converter=jsons_to_movie_roles,
            help=(
                """
                List of roles in json format (Each role must be in json
                format).

                Example of a role:
                {
                    "id": "066746d0-a236-7f1d-8000-1711de4b4e03",
                    "person_id": "066746c5-fda5-7985-8000-d16c225a8b17",
                    "character": "Captain Jack Sparrow",
                    "importance": 1,
                    "is_spoiler": false
                }
                """
            ),
        ),
    ] = [],
    writers: Annotated[
        Iterable[MovieWriter],
        Parameter(
            "--writers",
            converter=jsons_to_movie_writers,
            help=(
                """
                List of writers in json format (Each writer must be in
                json format).

                Example of a writer:
                {
                    "id": "066746e6-b9b3-7b13-8000-120c5b23f268",
                    "person_id": "066746e5-71e3-73e5-8000-d9bdd5ead582",
                    "writing": "Origin"
                }
                """
            ),
        ),
    ] = [],
    crew: Annotated[
        Iterable[MovieCrewMember],
        Parameter(
            "--crew",
            converter=jsons_to_movie_crew,
            help=(
                """
                List of crew members in json format (Each crew member must be
                in json format).

                Example of a crew member:
                {
                    "id": "066746ff-367e-721f-8000-655eca7fdf18",
                    "person_id": "066746fe-49a6-7e8d-8000-d780471a81f9",
                    "membership": "Director"
                }
                """
            ),
        ),
    ] = [],
) -> None:
    ioc_container = ioc_container_factory()

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
        roles=roles,
        writers=writers,
        crew=crew,
    )
    command_processor = await ioc_container.get(
        CommandProcessor[CreateMovieCommand, None],
    )
    await command_processor.process(command)

    print("Movie has been added successfully")
