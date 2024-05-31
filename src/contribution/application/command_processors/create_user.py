import logging

from contribution.domain import (
    InvalidUserNameError,
    InvalidEmailError,
    InvalidTelegramError,
    CreateUser,
)
from contribution.application.common import (
    CorrelationId,
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
    correlation_id: CorrelationId,
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
        correlation_id=correlation_id,
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
        user_with_same_id = await self._user_gateway.by_id(
            id=command.user_id,
        )
        if user_with_same_id:
            raise UserIdIsAlreadyTakenError()

        user_with_same_name = await self._user_gateway.by_name(
            name=command.name,
        )
        if user_with_same_name:
            raise UserNameIsAlreadyTakenError()

        if command.email:
            user_with_same_email = await self._user_gateway.by_email(
                email=command.email,
            )
            if user_with_same_email:
                raise UserEmailIsAlreadyTakenError()
        if command.telegram:
            user_with_same_telegram = await self._user_gateway.by_telegram(
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
    def __init__(
        self,
        *,
        processor: TransactionProcessor,
        correlation_id: CorrelationId,
    ):
        self._processor = processor
        self._correlation_id = correlation_id

    async def process(self, command: CreateUserCommand) -> None:
        logger.debug(
            "'Create User' command processing started",
            extra={
                "correlation_id": self._correlation_id,
                "command": command,
            },
        )

        try:
            result = await self._processor.process(command)
        except UserIdIsAlreadyTakenError as e:
            logger.error(
                "Unexpected error occurred: User id is already taken",
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
            "'Create User' command processing completed",
            extra={"correlation_id": self._correlation_id},
        )

        return result
