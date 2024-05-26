from typing import Optional

from contribution.domain.value_objects import UserId
from contribution.domain.validators import (
    ValidateUserName,
    ValidateEmail,
    ValidateTelegram,
)
from contribution.domain.entities import User


class CreateUser:
    def __init__(
        self,
        validate_user_name: ValidateUserName,
        validate_email: ValidateEmail,
        validate_telegram: ValidateTelegram,
    ):
        self._validate_user_name = validate_user_name
        self._validate_email = validate_email
        self._validate_telegram = validate_telegram

    def __call__(
        self,
        *,
        id: UserId,
        name: str,
        email: Optional[str],
        telegram: Optional[str],
        is_active: bool,
    ) -> User:
        self._validate_user_name(name)

        if email:
            self._validate_email(email)
        if telegram:
            self._validate_telegram(telegram)

        return User(
            id=id,
            name=name,
            email=email,
            telegram=telegram,
            is_active=is_active,
            rating=0,
            accepted_contributions_count=0,
            rejected_contributions_count=0,
        )
