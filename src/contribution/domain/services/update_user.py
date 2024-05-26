from typing import Optional

from contribution.domain.validators import (
    ValidateUserName,
    ValidateEmail,
    ValidateTelegram,
)
from contribution.domain.entities import User
from contribution.domain.maybe import Maybe


class UpdateUser:
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
        user: User,
        *,
        name: Maybe[str],
        email: Maybe[Optional[str]],
        telegram: Maybe[Optional[str]],
        is_active: Maybe[bool],
    ) -> None:
        if name.is_set:
            self._validate_user_name(name.value)
            user.name = name.value
        if email.is_set:
            if email.value:
                self._validate_email(email.value)
            user.email = email.value
        if telegram.is_set:
            if telegram.value:
                self._validate_telegram(telegram.value)
            user.telegram = telegram.value
        if is_active.is_set:
            user.is_active = is_active.value
