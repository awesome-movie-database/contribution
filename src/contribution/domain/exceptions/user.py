from .base import DomainError


class InvalidUserNameError(DomainError):
    ...


class UserIsNotActiveError(DomainError):
    ...
