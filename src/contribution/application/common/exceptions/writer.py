from typing import Collection

from contribution.domain import WriterId
from .base import ApplicationError


class WritersAlreadyExistError(ApplicationError):
    def __init__(self, writer_ids: Collection[WriterId]):
        self.writer_ids = writer_ids


class WritersDoNotExistError(ApplicationError):
    def __init__(
        self,
        writer_ids: Collection[WriterId],
    ):
        self.writer_ids = writer_ids
