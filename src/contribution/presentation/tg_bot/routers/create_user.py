from uuid import UUID

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from dishka.integrations.aiogram import FromDishka, inject

from contribution.domain import UserId
from contribution.application import CommandProcessor, CreateUserCommand
from contribution.presentation.tg_bot.exceptions import InvalidCommandError


STRING_REPRESENTING_NONE = "_"

create_user_router = Router()

CreateUserCommandProcessor = CommandProcessor[
    CreateUserCommand,
    None,
]


@create_user_router.message(Command("create_user"))
@inject
async def create_user(
    message: Message,
    command_processor: FromDishka[CreateUserCommandProcessor],
) -> None:
    command = _create_user_command_from_message(message)
    await command_processor.process(command)
    await message.answer("User has been created successfully")


def _create_user_command_from_message(message: Message) -> CreateUserCommand:
    split_message = message.text.split()
    split_message_length = len(split_message)

    if split_message_length < 6:
        message = (
            "Command has too few arguments. Expected 6 arguments, "
            f"but given {split_message_length}."
        )
        raise InvalidCommandError(message)
    elif split_message_length > 6:
        message = (
            "Command has too many arguments. Expected 6 arguments, "
            f"but given {split_message_length}."
        )
        raise InvalidCommandError(message)

    (
        _,
        id_from_message,
        name_from_message,
        email_from_message,
        telegram_from_message,
        is_active_from_message,
    ) = split_message

    id = UserId(UUID(id_from_message))
    name = name_from_message

    if email_from_message == STRING_REPRESENTING_NONE:
        email = None
    else:
        email = email_from_message

    if telegram_from_message == STRING_REPRESENTING_NONE:
        telegram = None
    else:
        telegram = telegram_from_message

    if is_active_from_message == "active":
        is_active = True
    elif is_active_from_message == "not_active":
        is_active = False
    else:
        message = (
            "Invalid 'is_active' param value. Param can only be "
            f"'active' or 'not_active', but {is_active_from_message} "
            "was given."
        )
        raise InvalidCommandError(message)

    return CreateUserCommand(
        id=id,
        name=name,
        email=email,
        telegram=telegram,
        is_active=is_active,
    )
