import logging

from uuid_extensions import uuid7

from contribution.domain.services import UpdateUser
from contribution.application.common.command_processors import (
    CommandProcessor,
    TransactionProcessor,
)
from contribution.application.common.exceptions import (
    UserNameIsAlreadyTakenError,
    UserEmailIsAlreadyTakenError,
    UserTelegramIsAlreadyTakenError,
    UserDoesNotExistError,
)
from contribution.application.common.gateways import UserGateway
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.commands import UpdateUserCommand


logger = logging.getLogger(__name__)


def update_user_factory(
    update_user: UpdateUser,
    user_gateway: UserGateway,
    unit_of_work: UnitOfWork,
) -> CommandProcessor[UpdateUserCommand, None]:
    update_user_processor = UpdateUserProcessor(
        update_user=update_user,
        user_gateway=user_gateway,
    )
    tx_processor = TransactionProcessor(
        processor=update_user_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = LoggingProcessor(
        processor=tx_processor,
    )

    return log_processor


class UpdateUserProcessor:
    def __init__(
        self,
        *,
        update_user: UpdateUser,
        user_gateway: UserGateway,
    ):
        self._update_user = update_user
        self._user_gateway = user_gateway

    async def process(self, command: UpdateUserCommand) -> None:
        user = await self._user_gateway.with_id(command.user_id)
        if not user:
            raise UserDoesNotExistError(command.user_id)

        if command.name.is_set:
            user_with_same_name = await self._user_gateway.with_name(
                name=command.name.value,
            )
            if user_with_same_name:
                raise UserNameIsAlreadyTakenError()
        if command.email.is_set and command.email.value:
            user_with_same_email = await self._user_gateway.with_email(
                email=command.email.value,
            )
            if user_with_same_email:
                raise UserEmailIsAlreadyTakenError()
        if command.telegram.is_set and command.telegram.value:
            user_with_same_telegram = await self._user_gateway.with_telegram(
                telegram=command.telegram.value,
            )
            if user_with_same_telegram:
                raise UserTelegramIsAlreadyTakenError()

        self._update_user(
            user=user,
            name=command.name,
            email=command.email,
            telegram=command.telegram,
            is_active=command.is_active,
        )
        await self._user_gateway.update(user)


class LoggingProcessor:
    def __init__(self, processor: TransactionProcessor):
        self._processor = processor

    async def process(self, command: UpdateUserCommand) -> None:
        command_processing_id = uuid7()

        logger.debug(
            "'Update User' command processing started",
            extra={
                "processing_id": command_processing_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except UserDoesNotExistError as e:
            logger.warning(
                "Unexpected error occurred: User doesn't exist",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except UserNameIsAlreadyTakenError as e:
            logger.warning(
                "Unexpected error occurred: User id is already taken",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except UserEmailIsAlreadyTakenError as e:
            logger.warning(
                "Unexpected error occurred: User email already taken",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except UserTelegramIsAlreadyTakenError as e:
            logger.warning(
                "Unexpected error occurred: User telegram is already taken",
                extra={"processing_id": command_processing_id},
            )
            raise e

        logger.debug(
            "'Update User' command processing completed",
            extra={"processing_id": command_processing_id},
        )

        return result
