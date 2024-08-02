import logging

from contribution.domain import (
    InvalidUserNameError,
    InvalidEmailError,
    InvalidTelegramError,
    UpdateUser,
)
from contribution.application.common import (
    OperationId,
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
    operation_id: OperationId,
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
    log_processor = UpdateUserLoggingProcessor(
        processor=tx_processor,
        operation_id=operation_id,
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


class UpdateUserLoggingProcessor:
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        operation_id: OperationId,
    ):
        self._processor = processor
        self._operation_id = operation_id

    async def process(self, command: UpdateUserCommand) -> None:
        logger.debug(
            "'Update User' command processing started",
            extra={
                "operation_id": self._operation_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except UserDoesNotExistError as error:
            logger.error(
                "Unexpected error occurred: User doesn't exist",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except UserNameIsAlreadyTakenError as error:
            logger.error(
                "Unexpected error occurred: User name is already taken",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except UserEmailIsAlreadyTakenError as error:
            logger.error(
                "Unexpected error occurred: User email already taken",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except UserTelegramIsAlreadyTakenError as error:
            logger.error(
                "Unexpected error occurred: User telegram is already taken",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except InvalidUserNameError as error:
            logger.error(
                "Unexpected error occurred: Invalid user name",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except InvalidEmailError as error:
            logger.error(
                "Unexpected error occurred: Invalid user email",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except InvalidTelegramError as error:
            logger.error(
                "Unexpected error occurred: Invalid user telegram",
                extra={"operation_id": self._operation_id},
            )
            raise error
        except Exception as error:
            logger.exception(
                "Unexpected error occurred",
                extra={"operation_id": self._operation_id},
            )
            raise error

        logger.debug(
            "'Update User' command processing completed",
            extra={"operation_id": self._operation_id},
        )

        return result
