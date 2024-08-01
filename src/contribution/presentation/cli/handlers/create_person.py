from datetime import date
from typing import Annotated, Optional

import rich
import rich.prompt
import rich.table
from cyclopts import Parameter

from contribution.domain import Sex, PersonId
from contribution.application import (
    CommandProcessor,
    CreatePersonCommand,
)
from contribution.infrastructure import cli_ioc_container_factory
from contribution.presentation.cli.converters import (
    str_to_uuid,
    str_to_date,
)


async def create_person(
    id: Annotated[
        PersonId,
        Parameter(
            "--id",
            converter=str_to_uuid,
            help="Id in [bright_yellow]UUID[/bright_yellow] format.",
        ),
    ],
    first_name: Annotated[str, Parameter("--first-name")],
    last_name: Annotated[str, Parameter("--last-name")],
    sex: Annotated[Sex, Parameter("--sex")],
    birth_date: Annotated[
        date,
        Parameter(
            "--birth-date",
            converter=str_to_date,
            help="Birth date in [bright_green]ISO 8601[/bright_green] format.",
        ),
    ],
    death_date: Annotated[
        Optional[date],
        Parameter(
            "--death-date",
            converter=str_to_date,
            help="Death date in [bright_green]ISO 8601[/bright_green] format.",
        ),
    ] = None,
) -> None:
    """
    Creates a new person. Does not notify other services about it.
    Asks confirmation before it.
    """
    continue_ = rich.prompt.Confirm.ask(
        "You are going to create a person.\n"
        "This action does not notify other services about a new person.\n"
        "Would you like to continue?",
    )
    if not continue_:
        return

    ioc_container = cli_ioc_container_factory()

    command = CreatePersonCommand(
        id=id,
        first_name=first_name,
        last_name=last_name,
        sex=sex,
        birth_date=birth_date,
        death_date=death_date,
    )
    async with ioc_container() as ioc_container_request:
        command_processor = await ioc_container_request.get(
            CommandProcessor[CreatePersonCommand, None],
        )
        await command_processor.process(command)

    person_table = _person_table_factory(
        id=id,
        first_name=first_name,
        last_name=last_name,
        sex=sex,
        birth_date=birth_date,
        death_date=death_date,
    )

    rich.print("Person has been added successfully")
    rich.print(person_table)


def _person_table_factory(
    id: PersonId,
    first_name: str,
    last_name: str,
    sex: Sex,
    birth_date: date,
    death_date: Optional[date],
) -> rich.table.Table:
    person_table = rich.table.Table(
        "id",
        "first_name",
        "last_name",
        "sex",
        "birth_date",
        "death_date",
    )
    person_table.add_row(
        str(id),
        first_name,
        last_name,
        sex,
        birth_date.isoformat(),
        death_date.isoformat() if death_date else "None",
    )
    return person_table
