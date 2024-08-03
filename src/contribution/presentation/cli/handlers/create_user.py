from typing import Annotated, Optional

import rich
import rich.prompt
import rich.table
from cyclopts import Parameter

from contribution.domain import UserId
from contribution.application import (
    CommandProcessor,
    CreateUserCommand,
)
from contribution.infrastructure import cli_ioc_container_factory
from contribution.presentation.cli.converters import str_to_uuid


async def create_user(
    id: Annotated[
        UserId,
        Parameter(
            "--id",
            converter=str_to_uuid,
            help="Id in [bright_yellow]UUID[/bright_yellow] format.",
        ),
    ],
    name: Annotated[str, Parameter("--name")],
    email: Annotated[Optional[str], Parameter("--email")] = None,
    telegram: Annotated[Optional[str], Parameter("--telegram")] = None,
    is_active: Annotated[bool, Parameter("--active")] = False,
) -> None:
    """
    Creates a new user. Does not notify other services about it.
    Asks confirmation before execting.
    """
    continue_ = rich.prompt.Confirm.ask(
        "You are going to create a user.\n"
        "This action does not notify other services about a new user.\n"
        "Would you like to continue?",
    )
    if not continue_:
        return

    ioc_container = cli_ioc_container_factory()

    command = CreateUserCommand(
        id=id,
        name=name,
        email=email,
        telegram=telegram,
        is_active=is_active,
    )
    async with ioc_container() as ioc_container_request:
        command_processor = await ioc_container_request.get(
            CommandProcessor[CreateUserCommand, None],
        )
        await command_processor.process(command)

    user_table = _user_table_factory(
        id=id,
        name=name,
        email=email,
        telegram=telegram,
        is_active=is_active,
    )

    rich.print("User has been created successfully")
    rich.print(user_table)


def _user_table_factory(
    id: UserId,
    name: str,
    email: Optional[str],
    telegram: Optional[str],
    is_active: bool,
) -> rich.table.Table:
    user_table = rich.table.Table(
        "id",
        "name",
        "email",
        "telegram",
        "is_active",
        title="User",
    )
    user_table.add_row(
        str(id),
        name,
        email or "None",
        telegram or "None",
        str(is_active),
    )
    return user_table
