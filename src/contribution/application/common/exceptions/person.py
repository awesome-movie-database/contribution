from typing import Collection

from contribution.domain import PersonId
from .base import ApplicationError


class PersonIdIsAlreadyTakenError(ApplicationError):
    ...


class PersonDoesNotExistError(ApplicationError):
    ...


class PersonsDoNotExistError(ApplicationError):
    def __init__(
        self,
        ids_of_missing_persons: Collection[PersonId],
    ):
        self.ids_of_missing_persons = ids_of_missing_persons
