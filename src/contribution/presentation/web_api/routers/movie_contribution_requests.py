from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from contribution.domain import (
    AddMovieContributionId,
    EditMovieContributionId,
)
from contribution.application import (
    CommandProcessor,
    AddMovieCommand,
    EditMovieCommand,
)


AddMovieCommandProcessor = CommandProcessor[
    AddMovieCommand,
    AddMovieContributionId,
]
EditMovieCommandProcessor = CommandProcessor[
    EditMovieCommand,
    EditMovieContributionId,
]


router = APIRouter(tags=["Movie contribution requests"])


@router.post("/add-movie-contribution-requests")
@inject
async def add_movie(
    *,
    command: AddMovieCommand,
    command_processor: FromDishka[AddMovieCommandProcessor],
) -> AddMovieContributionId:
    """
    Creates request to add movie on **amdb** and returns
    its id.
    """
    return await command_processor.process(command)


@router.post("/edit-movie-contribution-requests")
@inject
async def edit_movie(
    *,
    command: EditMovieCommand,
    command_processor: FromDishka[EditMovieCommandProcessor],
) -> EditMovieContributionId:
    """
    Creates request to edit movie on **amdb** and returns
    its id.
    """
    return await command_processor.process(command)
