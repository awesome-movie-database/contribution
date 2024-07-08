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
from contribution.presentation.web_api.requests import EditPersonRequest


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
    command: AddPersonCommand,
    command_processor: FromDishka[AddPersonCommandProcessor],
) -> AddPersonContributionId:
    """
    Creates request to add person on **amdb** and returns
    its id.
    """
    return await command_processor.process(command)


@router.post("/edit-person-contribution-requests")
@inject
async def edit_person(
    *,
    request: EditPersonRequest,
    command_processor: FromDishka[EditPersonCommandProcessor],
) -> EditPersonContributionId:
    """
    Creates request to edit person on **amdb** and returns
    its id.
    """
    command = request.to_command()
    return await command_processor.process(command)
