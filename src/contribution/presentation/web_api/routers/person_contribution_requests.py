from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from contribution.domain import (
    AddPersonContributionId,
    EditPersonContributionId,
)
from contribution.application import (
    CommandProcessor,
    AddPersonCommand,
    EditPersonCommand,
)


AddPersonCommandProcessor = CommandProcessor[
    AddPersonCommand,
    AddPersonContributionId,
]
EditPersonCommandProcessor = CommandProcessor[
    EditPersonCommand,
    EditPersonContributionId,
]


router = APIRouter(tags=["Person contribution requests"])


@router.post("/add-person-contribution-requests")
@inject
async def add_person(
    *,
    command: FromDishka[AddPersonCommand],
    command_processor: FromDishka[AddPersonCommandProcessor],
) -> AddPersonContributionId:
    """
    Create request to add person on **amdb** and returns
    its id.
    """
    return await command_processor.process(command)


@router.post("/edit-person-contribution-requests")
@inject
async def edit_person(
    *,
    command: FromDishka[EditPersonCommand],
    command_processor: FromDishka[EditPersonCommandProcessor],
) -> EditPersonContributionId:
    """
    Create request to edit person on **amdb** and returns
    its id.
    """
    return await command_processor.process(command)
