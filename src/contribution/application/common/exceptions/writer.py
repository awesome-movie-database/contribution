from typing import Sequence

from contribution.domain.value_objects import WriterId
from .base import ApplicationError


class WritersAlreadyExistError(ApplicationError):
    def __init__(
        self,
        ids_of_existing_writers: Sequence[WriterId],
    ):
        self.ids_of_existing_writers = ids_of_existing_writers


class WritersDoNotExistError(ApplicationError):
    def __init__(
        self,
        ids_of_missing_writers: Sequence[WriterId],
    ):
        self.ids_of_missing_writers = ids_of_missing_writers
