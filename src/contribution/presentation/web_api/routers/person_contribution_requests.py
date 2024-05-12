from typing import Annotated, Optional, cast
from datetime import date

from fastapi import APIRouter, File
from dishka.integrations.fastapi import FromDishka, inject

from contribution.domain.constants import Sex
from contribution.domain.value_objects import (
    PersonId,
    AddPersonContributionId,
    EditPersonContributionId,
)
from contribution.application.common.command_processors import (
    CommandProcessor,
)
from contribution.application.commands import (
    AddPersonCommand,
    EditPersonCommand,
)
from contribution.presentation.web_api.schemas import (
    AddPersonSchema,
    EditPersonSchema,
)
from contribution.presentation.web_api.maybe_value_from_mapping import (
    maybe_value_from_mapping,
)


AddPersonCommandProcessor = CommandProcessor[
    AddPersonCommand,
    AddPersonContributionId,
]
EditPersonCommandProcessor = CommandProcessor[
    EditPersonCommand,
    EditPersonContributionId,
]


router = APIRouter(
    prefix="/person-contribution-requests",
    tags=["Person Contribution Requests"],
)


@router.post("/to-add")
@inject
async def add_person(
    *,
    command_processor: FromDishka[AddPersonCommandProcessor],
    schema: AddPersonSchema,
    photos: Annotated[list[bytes], File()],
) -> AddPersonContributionId:
    """
    Create request to add person on **amdb** and returns
    its id.
    """
    command = AddPersonCommand(
        first_name=schema.first_name,
        last_name=schema.last_name,
        sex=schema.sex,
        birth_date=schema.birth_date,
        death_date=schema.death_date,
        photos=photos,
    )
    return await command_processor.process(command)


@router.post("/to-edit")
@inject
async def edit_person(
    *,
    command_processor: FromDishka[EditPersonCommandProcessor],
    schema: EditPersonSchema,
    add_photos: Annotated[list[bytes], File()],
) -> EditPersonContributionId:
    """
    Create request to edit person on **amdb** and returns
    its id.
    """
    first_name = maybe_value_from_mapping[str](schema, "first_name")
    last_name = maybe_value_from_mapping[str](schema, "last_name")
    sex = maybe_value_from_mapping[Sex](schema, "sex")
    birth_date = maybe_value_from_mapping[date](schema, "birth_date")
    death_date = maybe_value_from_mapping[Optional[date]](schema, "death_date")

    command = EditPersonCommand(
        person_id=cast(PersonId, schema.get("person_id")),
        first_name=first_name,
        last_name=last_name,
        sex=sex,
        birth_date=birth_date,
        death_date=death_date,
        add_photos=add_photos,
    )
    return await command_processor.process(command)
