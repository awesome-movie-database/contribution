from contribution.domain.services import CreateUser
from contribution.application.common.command_processors import (
    CommandProcessor,
    TransactionProcessor,
)
from contribution.application.common.exceptions import (
    UserIdIsAlreadyTakenError,
    UserNameIsAlreadyTakenError,
    UserEmailIsAlreadyTakenError,
    UserTelegramIsAlreadyTakenError,
)
from contribution.application.common.gateways import UserGateway
from contribution.application.common.unit_of_work import UnitOfWork
from contribution.application.commands import CreateUserCommand


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
    return tx_processor


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
