import logging

from uuid_extensions import uuid7

from contribution.domain import CreateUser
from contribution.application.common import (
    CommandProcessor,
    TransactionProcessor,
    UserIdIsAlreadyTakenError,
    UserNameIsAlreadyTakenError,
    UserEmailIsAlreadyTakenError,
    UserTelegramIsAlreadyTakenError,
    UserGateway,
    UnitOfWork,
)
from contribution.application.commands import CreateUserCommand


logger = logging.getLogger(__name__)


def create_user_factory(
    create_user: CreateUser,
    user_gateway: UserGateway,
    unit_of_work: UnitOfWork,
) -> CommandProcessor[CreateUserCommand, None]:
    create_user_processor = CreateUserProcessor(
        create_user=create_user,
        user_gateway=user_gateway,
    )
    tx_processor = TransactionProcessor(
        processor=create_user_processor,
        unit_of_work=unit_of_work,
    )
    log_processor = LoggingProcessor(
        processor=tx_processor,
    )

    return log_processor


class CreateUserProcessor:
    def __init__(
        self,
        *,
        create_user: CreateUser,
        user_gateway: UserGateway,
    ):
        self._create_user = create_user
        self._user_gateway = user_gateway

    async def process(self, command: CreateUserCommand) -> None:
        user_with_same_id = await self._user_gateway.with_id(
            id=command.user_id,
        )
        if user_with_same_id:
            raise UserIdIsAlreadyTakenError()

        user_with_same_name = await self._user_gateway.with_name(
            name=command.name,
        )
        if user_with_same_name:
            raise UserNameIsAlreadyTakenError()

        if command.email:
            user_with_same_email = await self._user_gateway.with_email(
                email=command.email,
            )
            if user_with_same_email:
                raise UserEmailIsAlreadyTakenError()

        if command.telegram:
            user_with_same_telegram = await self._user_gateway.with_telegram(
                telegram=command.telegram,
            )
            if user_with_same_telegram:
                raise UserTelegramIsAlreadyTakenError()

        new_user = self._create_user(
            id=command.user_id,
            name=command.name,
            email=command.email,
            telegram=command.telegram,
            is_active=command.is_active,
        )
        await self._user_gateway.save(new_user)


class LoggingProcessor:
    def __init__(self, processor: TransactionProcessor):
        self._processor = processor

    async def process(self, command: CreateUserCommand) -> None:
        command_processing_id = uuid7()

        logger.debug(
            "'Create User' command processing started",
            extra={
                "processing_id": command_processing_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except UserIdIsAlreadyTakenError as e:
            logger.error(
                "Unexpected error occurred: User id is already taken",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except UserNameIsAlreadyTakenError as e:
            logger.error(
                "Unexpected error occurred: User name is already taken",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except UserEmailIsAlreadyTakenError as e:
            logger.error(
                "Unexpected error occurred: User email already taken",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except UserTelegramIsAlreadyTakenError as e:
            logger.error(
                "Unexpected error occurred: User telegram is already taken",
                extra={"processing_id": command_processing_id},
            )
            raise e
        except Exception as e:
            logger.exception(
                "Unexpected error occurred",
                exc_info=e,
                extra={
                    "processing_id": command_processing_id,
                    "error": e,
                },
            )
            raise e

        logger.debug(
            "'Create User' command processing completed",
            extra={"processing_id": command_processing_id},
        )

        return result
