from typing import Annotated, Optional

import rich
import rich.prompt
import rich.table
from cyclopts import Parameter

from contribution.domain import UserId, Maybe
from contribution.application import (
    CommandProcessor,
    UpdateUserCommand,
)
from contribution.infrastructure.di.cli import cli_ioc_container_factory
from contribution.presentation.cli.converters import (
    str_to_uuid,
    bool_to_maybe_bool,
    str_to_maybe_str,
    str_to_maybe_optional_str,
)


async def update_user(
    id: Annotated[
        UserId,
        Parameter(
            "--id",
            converter=str_to_uuid,
            help="Id in [bright_yellow]UUID[/bright_yellow] format.",
        ),
    ],
    name: Annotated[
        Maybe[str],
        Parameter("--name", converter=str_to_maybe_str),
    ] = Maybe[str].without_value(),
    email: Annotated[
        Maybe[Optional[str]],
        Parameter("--email", converter=str_to_maybe_optional_str),
    ] = Maybe[Optional[str]].without_value(),
    telegram: Annotated[
        Maybe[Optional[str]],
        Parameter("--telegram", converter=str_to_maybe_optional_str),
    ] = Maybe[Optional[str]].without_value(),
    is_active: Annotated[
        Maybe[bool],
        Parameter("--active", converter=bool_to_maybe_bool),
    ] = Maybe[bool].without_value(),
) -> None:
    """
    Updates a user. Does not notify other services about it.
    Asks confirmation before execting.
    """
    executing_is_confirmed = rich.prompt.Confirm.ask(
        "You are going to update a user.\n"
        "This action does not notify other services about updates.\n"
        "Would you like to continue?",
    )
    if not executing_is_confirmed:
        return

    ioc_container = cli_ioc_container_factory()

    command = UpdateUserCommand(
        user_id=id,
        name=name,
        email=email,
        telegram=telegram,
        is_active=is_active,
    )
    async with ioc_container() as ioc_container_request:
        command_processor = await ioc_container_request.get(
            CommandProcessor[UpdateUserCommand, None],
        )
        await command_processor.process(command)

    updated_user_fields_table = _updated_user_fields_table_factory(
        id=id,
        name=name,
        email=email,
        telegram=telegram,
        is_active=is_active,
    )

    rich.print("User has been updated successfully")
    rich.print(updated_user_fields_table)


def _updated_user_fields_table_factory(
    *,
    id: UserId,
    name: Maybe[str],
    email: Maybe[Optional[str]],
    telegram: Maybe[Optional[str]],
    is_active: Maybe[bool],
) -> rich.table.Table:
    updated_user_fields_table = rich.table.Table(
        "id",
        title="Updated user fields",
    )
    updated_user_field_values = [str(id)]

    if name.is_set:
        updated_user_fields_table.add_column("name")
        updated_user_field_values.append(name.value)
    if email.is_set:
        updated_user_fields_table.add_column("email")
        updated_user_field_values.append(email.value or "None")
    if telegram.is_set:
        updated_user_fields_table.add_column("telegram")
        updated_user_field_values.append(telegram.value or "None")
    if is_active.is_set:
        updated_user_fields_table.add_column("is_active")
        updated_user_field_values.append(str(is_active.value))

    updated_user_fields_table.add_row(*updated_user_field_values)

    return updated_user_fields_table
