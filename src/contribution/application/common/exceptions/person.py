from typing import Collection

from contribution.domain import PersonId
from .base import ApplicationError


class PersonIdIsAlreadyTakenError(ApplicationError):
    ...


class PersonDoesNotExistError(ApplicationError):
    ...


class PersonsDoNotExistError(ApplicationError):
    def __init__(self, person_ids: Collection[PersonId]):
        self.person_ids = person_ids
