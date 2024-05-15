from typing import Union, cast

from contribution.domain import (
    UserId,
    Email,
    Telegram,
)
from .base import ApplicationError


class UserIdIsAlreadyTakenError(ApplicationError):
    ...


class UserNameIsAlreadyTakenError(ApplicationError):
    ...


class UserEmailIsAlreadyTakenError(ApplicationError):
    ...


class UserTelegramIsAlreadyTakenError(ApplicationError):
    ...


Name = str


class UserDoesNotExistError(ApplicationError):
    def __init__(
        self,
        identifier: Union[
            UserId,
            Name,
            Email,
            Telegram,
        ],
    ):
        self.identifier = identifier

    @property
    def id(self) -> UserId:
        return cast(UserId, self.identifier)

    @property
    def name(self) -> Name:
        return cast(Name, self.identifier)

    @property
    def email(self) -> Email:
        return cast(Email, self.identifier)

    @property
    def telegram(self) -> Telegram:
        return cast(Telegram, self.identifier)
