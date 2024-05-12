from typing import Annotated, Sequence, Optional, cast
from datetime import date

from fastapi import APIRouter, File
from dishka.integrations.fastapi import FromDishka, inject

from contribution.domain.constants import (
    Genre,
    MPAA,
)
from contribution.domain.value_objects import (
    MovieId,
    AddMovieContributionId,
    EditMovieContributionId,
    Country,
    Money,
)
from contribution.application.common.command_processors import (
    CommandProcessor,
)
from contribution.application.commands import (
    AddMovieCommand,
    EditMovieCommand,
)
from contribution.presentation.web_api.schemas import (
    AddMovieSchema,
    EditMovieSchema,
)
from contribution.presentation.web_api.maybe_value_from_mapping import (
    maybe_value_from_mapping,
)


AddMovieCommandProcessor = CommandProcessor[
    AddMovieCommand,
    AddMovieContributionId,
]
EditMovieCommandProcessor = CommandProcessor[
    EditMovieCommand,
    EditMovieContributionId,
]


router = APIRouter(
    prefix="/movie-contribution-requests",
    tags=["Movie Contribution Requests"],
)


@router.post("/to-add")
@inject
async def add_movie(
    *,
    command_processor: FromDishka[AddMovieCommandProcessor],
    schema: AddMovieSchema,
    photos: Annotated[list[bytes], File()],
) -> AddMovieContributionId:
    """
    Creates request to add movie on **amdb** and returns
    its id.
    """
    command = AddMovieCommand(
        eng_title=schema.eng_title,
        original_title=schema.original_title,
        release_date=schema.release_date,
        countries=schema.countries,
        genres=schema.genres,
        mpaa=schema.mpaa,
        duration=schema.duration,
        budget=schema.budget,
        revenue=schema.revenue,
        roles=schema.roles,
        writers=schema.writers,
        crew=schema.crew,
        photos=photos,
    )
    return await command_processor.process(command)


@router.post("/to-edit")
@inject
async def edit_movie(
    *,
    command_processor: FromDishka[EditMovieCommandProcessor],
    schema: EditMovieSchema,
    add_photos: Annotated[list[bytes], File()],
) -> EditMovieContributionId:
    """
    Creates request to edit movie on **amdb** and returns
    its id.
    """
    eng_title = maybe_value_from_mapping[str](schema, "eng_title")
    original_title = maybe_value_from_mapping[str](schema, "original_title")
    release_date = maybe_value_from_mapping[date](schema, "release_date")
    countries = maybe_value_from_mapping[Sequence[Country]](
        mapping=schema,
        key="countries",
    )
    genres = maybe_value_from_mapping[Sequence[Genre]](schema, "genres")
    mpaa = maybe_value_from_mapping[MPAA](schema, "mpaa")
    duration = maybe_value_from_mapping[int](schema, "duration")
    budget = maybe_value_from_mapping[Optional[Money]](schema, "budget")
    revenue = maybe_value_from_mapping[Optional[Money]](schema, "revenue")

    command = EditMovieCommand(
        movie_id=cast(MovieId, schema.get("movie_id")),
        eng_title=eng_title,
        original_title=original_title,
        release_date=release_date,
        countries=countries,
        genres=genres,
        mpaa=mpaa,
        duration=duration,
        budget=budget,
        revenue=revenue,
        add_roles=schema.get("add_roles", []),
        remove_roles=schema.get("remove_roles", []),
        add_writers=schema.get("add_writers", []),
        remove_writers=schema.get("remove_writers", []),
        add_crew=schema.get("add_crew", []),
        remove_crew=schema.get("remove_crew", []),
        add_photos=add_photos,
    )
    return await command_processor.process(command)
