from datetime import date
from typing import Annotated, Optional

import rich
import rich.prompt
import rich.table
from cyclopts import Parameter

from contribution.domain import Sex, PersonId, Maybe
from contribution.application import (
    CommandProcessor,
    UpdatePersonCommand,
)
from contribution.infrastructure import cli_ioc_container_factory
from contribution.presentation.cli.converters import (
    str_to_uuid,
    str_to_maybe_str,
    str_to_maybe_date,
    str_to_maybe_optional_date,
    str_to_maybe_sex,
)


async def update_person(
    id: Annotated[
        PersonId,
        Parameter(
            "--id",
            converter=str_to_uuid,
            help="Id in [bright_yellow]UUID[/bright_yellow] format.",
        ),
    ],
    first_name: Annotated[
        Maybe[str],
        Parameter("--first-name", converter=str_to_maybe_str),
    ] = Maybe[str].without_value(),
    last_name: Annotated[
        Maybe[str],
        Parameter("--last-name", converter=str_to_maybe_str),
    ] = Maybe[str].without_value(),
    sex: Annotated[
        Maybe[Sex],
        Parameter("--sex", converter=str_to_maybe_sex),
    ] = Maybe[Sex].without_value(),
    birth_date: Annotated[
        Maybe[date],
        Parameter(
            "--birth-date",
            converter=str_to_maybe_date,
            help="Birth date in [bright_green]ISO 8601[/bright_green] format.",
        ),
    ] = Maybe[date].without_value(),
    death_date: Annotated[
        Maybe[Optional[date]],
        Parameter(
            "--death-date",
            converter=str_to_maybe_optional_date,
            help="Death date in [bright_green]ISO 8601[/bright_green] format.",
        ),
    ] = Maybe[Optional[date]].without_value(),
) -> None:
    """
    Updates a person. Does not notify other services about it.
    Asks confirmation before execting.
    """
    continue_ = rich.prompt.Confirm.ask(
        "You are going to update a person.\n"
        "This action does not notify other services about updates.\n"
        "Would you like to continue?",
    )
    if not continue_:
        return

    ioc_container = cli_ioc_container_factory()

    command = UpdatePersonCommand(
        person_id=id,
        first_name=first_name,
        last_name=last_name,
        sex=sex,
        birth_date=birth_date,
        death_date=death_date,
    )
    async with ioc_container() as ioc_container_request:
        command_processor = await ioc_container_request.get(
            CommandProcessor[UpdatePersonCommand, None],
        )
        await command_processor.process(command)

    updated_person_fields_table = _updated_person_fields_table_factory(
        id=id,
        first_name=first_name,
        last_name=last_name,
        sex=sex,
        birth_date=birth_date,
        death_date=death_date,
    )

    rich.print("Person has been updated successfully")
    rich.print(updated_person_fields_table)


def _updated_person_fields_table_factory(
    id: PersonId,
    first_name: Maybe[str],
    last_name: Maybe[str],
    sex: Maybe[Sex],
    birth_date: Maybe[date],
    death_date: Maybe[Optional[date]],
) -> rich.table.Table:
    updated_person_fields_table = rich.table.Table(
        "id",
        title="Updated person fields",
    )
    updated_person_field_values = []

    if first_name.is_set:
        updated_person_fields_table.add_column("first_name")
        updated_person_field_values.append(first_name.value)
    if last_name.is_set:
        updated_person_fields_table.add_column("last_name")
        updated_person_field_values.append(last_name.value)
    if sex.is_set:
        updated_person_fields_table.add_column("sex")
        updated_person_field_values.append(sex.value)
    if birth_date.is_set:
        updated_person_fields_table.add_column("birth_date")
        updated_person_field_values.append(birth_date.value.isoformat())
    if death_date.is_set:
        updated_person_fields_table.add_column("death_date")

        birth_date_ = birth_date.value
        if birth_date_:
            updated_person_field_values.append(birth_date_.isoformat())
        else:
            updated_person_field_values.append("None")

    updated_person_fields_table.add_row(
        str(id),
        *updated_person_field_values,
    )

    return updated_person_fields_table
