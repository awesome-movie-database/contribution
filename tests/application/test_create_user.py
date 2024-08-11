import pytest
from uuid_extensions import uuid7

from contribution.domain import (
    UserId,
    ValidateUserName,
    ValidateEmail,
    ValidateTelegram,
    CreateUser,
)
from contribution.application import (
    TransactionProcessor,
    UserGateway,
    UnitOfWork,
    CreateUserCommand,
    CreateUserProcessor,
)


@pytest.mark.usefixtures("clear_database")
async def test_create_user(
    user_gateway: UserGateway,
    unit_of_work: UnitOfWork,
):
    command = CreateUserCommand(
        id=UserId(uuid7()),
        name="JohnDoe",
        email="johndoe@gmail.com",
        telegram=None,
        is_active=True,
    )
    create_user = CreateUser(
        validate_user_name=ValidateUserName(),
        validate_email=ValidateEmail(),
        validate_telegram=ValidateTelegram(),
    )
    create_user_processor = CreateUserProcessor(
        create_user=create_user,
        user_gateway=user_gateway,
    )
    tx_processor = TransactionProcessor(
        processor=create_user_processor,
        unit_of_work=unit_of_work,
    )

    await tx_processor.process(command)
