from .base import ApplicationError


class MovieIdIsAlreadyTakenError(ApplicationError):
    ...


class MovieDoesNotExistError(ApplicationError):
    ...
