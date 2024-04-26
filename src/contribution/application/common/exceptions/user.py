from .base import ApplicationError


class UserIdIsAlreadyTakenError(ApplicationError):
    ...


class UserNameIsAlreadyTakenError(ApplicationError):
    ...


class UserEmailIsAlreadyTakenError(ApplicationError):
    ...


class UserTelegramIsAlreadyTakenError(ApplicationError):
    ...
