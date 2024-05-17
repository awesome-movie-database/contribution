from typing import Collection

from contribution.domain import WriterId
from .base import ApplicationError


class WritersAlreadyExistError(ApplicationError):
    def __init__(
        self,
        ids_of_existing_writers: Collection[WriterId],
    ):
        self.ids_of_existing_writers = ids_of_existing_writers


class WritersDoNotExistError(ApplicationError):
    def __init__(
        self,
        ids_of_missing_writers: Collection[WriterId],
    ):
        self.ids_of_missing_writers = ids_of_missing_writers
