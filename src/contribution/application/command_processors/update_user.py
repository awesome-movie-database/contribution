import logging

from contribution.domain import (
    InvalidUserNameError,
    InvalidEmailError,
    InvalidTelegramError,
    UpdateUser,
)
from contribution.application.common import (
    CorrelationId,
    CommandProcessor,
    TransactionProcessor,
    UserNameIsAlreadyTakenError,
    UserEmailIsAlreadyTakenError,
    UserTelegramIsAlreadyTakenError,
    UserDoesNotExistError,
    UserGateway,
    UnitOfWork,
)
from contribution.application.commands import UpdateUserCommand


logger = logging.getLogger(__name__)


def update_user_factory(
    correlation_id: CorrelationId,
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
        correlation_id=correlation_id,
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
        user = await self._user_gateway.by_id(command.user_id)
        if not user:
            raise UserDoesNotExistError()

        if command.name.is_set:
            user_with_same_name = await self._user_gateway.by_name(
                name=command.name.value,
            )
            if user_with_same_name:
                raise UserNameIsAlreadyTakenError()
        if command.email.is_set and command.email.value:
            user_with_same_email = await self._user_gateway.by_email(
                email=command.email.value,
            )
            if user_with_same_email:
                raise UserEmailIsAlreadyTakenError()
        if command.telegram.is_set and command.telegram.value:
            user_with_same_telegram = await self._user_gateway.by_telegram(
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
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        correlation_id: CorrelationId,
    ):
        self._processor = processor
        self._correlation_id = correlation_id

    async def process(self, command: UpdateUserCommand) -> None:
        logger.debug(
            "'Update User' command processing started",
            extra={
                "correlation_id": self._correlation_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except UserDoesNotExistError as e:
            logger.error(
                "Unexpected error occurred: User doesn't exist",
                extra={"correlation_id": self._correlation_id},
            )
            raise e
        except UserNameIsAlreadyTakenError as e:
            logger.error(
                "Unexpected error occurred: User name is already taken",
                extra={"correlation_id": self._correlation_id},
            )
            raise e
        except UserEmailIsAlreadyTakenError as e:
            logger.error(
                "Unexpected error occurred: User email already taken",
                extra={"correlation_id": self._correlation_id},
            )
            raise e
        except UserTelegramIsAlreadyTakenError as e:
            logger.error(
                "Unexpected error occurred: User telegram is already taken",
                extra={"correlation_id": self._correlation_id},
            )
            raise e
        except InvalidUserNameError as e:
            logger.error(
                "Unexpected error occurred: Invalid user name",
                extra={"correlation_id": self._correlation_id},
            )
            raise e
        except InvalidEmailError as e:
            logger.error(
                "Unexpected error occurred: Invalid user email",
                extra={"correlation_id": self._correlation_id},
            )
            raise e
        except InvalidTelegramError as e:
            logger.error(
                "Unexpected error occurred: Invalid user telegram",
                extra={"correlation_id": self._correlation_id},
            )
            raise e
        except Exception as e:
            logger.exception(
                "Unexpected error occurred",
                exc_info=e,
                extra={
                    "correlation_id": self._correlation_id,
                    "error": e,
                },
            )
            raise e

        logger.debug(
            "'Update User' command processing completed",
            extra={"correlation_id": self._correlation_id},
        )

        return result
