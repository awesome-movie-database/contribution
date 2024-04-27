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
    return tx_processor


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
