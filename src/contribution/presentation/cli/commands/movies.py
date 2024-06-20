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
    jsons_to_crew,
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
        Parameter("--budget", converter=json_to_money),
    ] = None,
    revenue: Annotated[
        Optional[Money],
        Parameter("--budget", converter=json_to_money),
    ] = None,
    roles: Annotated[
        list[MovieRole],
        Parameter("--roles", converter=jsons_to_movie_roles),
    ] = [],
    writers: Annotated[
        list[MovieWriter],
        Parameter("--writers", converter=jsons_to_movie_writers),
    ] = [],
    crew: Annotated[
        list[MovieCrewMember],
        Parameter("--crew", converter=jsons_to_crew),
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
