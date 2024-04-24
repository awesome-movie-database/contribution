from typing import Optional

from contribution.domain.value_objects import (
    UserId,
    Email,
    Telegram,
)
from contribution.domain.validators import ValidateUserName
from contribution.domain.entities import User


class CreateUser:
    def __init__(
        self,
        validate_user_name: ValidateUserName,
    ):
        self._validate_user_name = validate_user_name

    def __call__(
        self,
        *,
        id: UserId,
        name: str,
        email: Optional[Email],
        telegram: Optional[Telegram],
        is_active: bool,
    ) -> User:
        self._validate_user_name(name)

        return User(
            id=id,
            name=name,
            email=email,
            telegram=telegram,
            is_active=is_active,
            rating=0,
            contributions_count=0,
        )
